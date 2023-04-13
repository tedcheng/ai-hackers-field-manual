# You need to set two ENV variables: OPENAI_API_KEY and SERPAPI_API_KEY. 
# You can get an OpenAI API key from https://openai.com/ and a SerpAPI API key from https://serpapi.com/.
# You can run this file with `ruby examples/llm_agents.rb` or `bundle exec ruby examples/llm_agents.rb`.

require 'openai'
require 'google_search_results'

class SerpAPITool
  attr_accessor :name, :description
  def initialize
    @name, @description = 'Google Search', 'Get specific information from a search query. Input should be a question like \'How to add number in Clojure?\'. Result will be the answer to the question.'
  end
  
  def process_response(res)
    raise "Got error from SerpAPI: #{res[:error]}" if res.key?(:error)
    res&.dig(:answer_box, :answer) ||
    res&.dig(:answer_box, :snippet) ||
    res&.dig(:answer_box, :snippet_highlighted_words)&.first ||
    res&.dig(:sports_results, :game_spotlight) ||
    res&.dig(:knowledge_graph, :description) ||
    res&.dig(:organic_results, 0, :snippet) ||
    'No good search result found'
  end

  def use(input_text)
    res = GoogleSearch.new({q: input_text, serp_api_key: ENV['SERPAPI_API_KEY']}).get_hash
    process_response(res)
  end
end

# # # # # # # # # # # # # # # # # # # # # 
# This is not safe for production use!  # 
# # # # # # # # # # # # # # # # # # # # # 
class RubyREPLTool
  attr_accessor :name, :description
  def initialize
    @name, @description = 'Ruby REPL', 'A Ruby shell. Use this to execute Ruby commands. Input should be a valid Ruby command. If you want to see the output of a value, you should print it out with `puts(...)`.'
  end
  
  def use(command)
    result = nil
    Thread.start {
      $SAFE = 2
      result = eval(command)
    }.join
    result
  end
end

class ChatLLM
  def generate(prompt, stop = nil)
    response = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY']).chat(
      parameters: {
        model: 'gpt-3.5-turbo',
        temperature: 0.0,
        messages: [{ "role" => "user", "content" => prompt }],
        stop: stop        
      }
    )
    response.dig("choices", 0, "message", "content")
  end
end

class Agent
  FINAL_ANSWER_TOKEN = "Final Answer:"
  OBSERVATION_TOKEN = "Observation:"
  THOUGHT_TOKEN = "Thought:"
  PROMPT_TEMPLATE = <<~PROMPT
    Today is %{today} and you can use tools to get new information. Answer the question as best as you can using the following tools:
  
    %{tool_description}
  
    Use the following format:
  
    Question: the input question you must answer
    Thought: comment on what you want to do next
    Action: the action to take, exactly one element of [%{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation repeats N times, use it until you are sure of the answer)
    Thought: I now know the final answer
    Final Answer: your final answer to the original input question
  
    Begin!
  
    Question: %{question}
    Thought: %{previous_responses}
  PROMPT
  MAX_LOOPS = 15
  attr_accessor :llm, :tools
  def initialize(llm, tools)
    @llm, @tools = llm, tools
  end

  def tool_description
    tools.map { |tool| "#{tool.name}: #{tool.description}" }.join("\n")
  end

  def tool_names
    tools.map(&:name).join(",")
  end

  def tool_by_names
    tools.map { |tool| [tool.name, tool] }.to_h
  end

  def run(question)
    previous_responses = []
    num_loops = 0
    prompt = PROMPT_TEMPLATE % {
        today: Time.now.strftime("%Y-%m-%d"),
        tool_description: tool_description,
        tool_names: tool_names,
        question: question,
        previous_responses: "%{previous_responses}"
    }
    puts prompt % { previous_responses: '' }
    while num_loops < MAX_LOOPS
      num_loops += 1
      curr_prompt = prompt % { previous_responses: previous_responses.join("\n") }
      generated, tool, tool_input = decide_next_action(curr_prompt)
      return tool_input if tool == 'Final Answer'
      raise ArgumentError, "Unknown tool: #{tool}" if !tool_by_names.has_key?(tool)
      tool_result = tool_by_names[tool].use(tool_input)
      generated += "\n#{OBSERVATION_TOKEN} #{tool_result}\n#{THOUGHT_TOKEN}"
      puts generated
      previous_responses << generated
    end
  end

  def decide_next_action(prompt)
    stop_pattern = ["\n#{OBSERVATION_TOKEN}", "\n\t#{OBSERVATION_TOKEN}"]
    generated = llm.generate(prompt, stop_pattern)
    tool, tool_input = parse(generated)
    return generated, tool, tool_input
  end

  def parse(generated)
    if generated.include?(FINAL_ANSWER_TOKEN)
      return "Final Answer", generated.split(FINAL_ANSWER_TOKEN)[-1].strip
    end
    regex = /Action: [\[]?(.*?)[\]]?[\n]*Action Input:[\s]*(.*)/m
    match = generated.match(regex)
    raise ArgumentError, "Output of LLM is not parsable for next tool use: `#{generated}`" if match.nil?
    tool = match[1].strip
    tool_input = match[2].strip.gsub(/(^"|"$)/, "")
    return tool, tool_input
  end
end

# Startup code
print "Enter a question / task for the agent: "
prompt = gets.chomp
result = Agent.new(ChatLLM.new, [RubyREPLTool.new, SerpAPITool.new]).run(prompt)
puts "Final answer is #{result}"