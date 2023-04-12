require 'date'
require 'openai'
require 'google_search_results'
require 'debug'

def search(query)
  search = GoogleSearch.new({q: query, serp_api_key: ENV['SERPAPI_API_KEY']})
  res = search.get_hash

  process_response(res)
end

def process_response(res)
  if res.key?(:error)
    raise "Got error from SerpAPI: #{res[:error]}"
  elsif res.key?(:answer_box)
    if res[:answer_box].key?(:answer)
      toret = res[:answer_box][:answer]
    elsif res[:answer_box].key?(:snippet)
      toret = res[:answer_box][:snippet]
    elsif res[:answer_box].key?(:snippet_highlighted_words)
      toret = res[:answer_box][:snippet_highlighted_words][0]
    end
  elsif res.key?(:sports_results) && res[:sports_results].key?(:game_spotlight)
    toret = res[:sports_results][:game_spotlight]
  elsif res.key?(:knowledge_graph) && res[:knowledge_graph].key?(:description)
    toret = res[:knowledge_graph][:description]
  elsif res[:organic_results][0].key?(:snippet)
    toret = res[:organic_results][0][:snippet]
  else
    toret = 'No good search result found'
  end
  toret
end

class SerpAPITool
  attr_accessor :name, :description
  def initialize
    @name = 'Google Search'
    @description = 'Get specific information from a search query. Input should be a question like \'How to add number in Clojure?\'. Result will be the answer to the question.'
  end

  def use(input_text)
    search(input_text)
  end
end

# # # # # # # # # # # # # # # # # # # # # 
# This is not safe for production use!  # 
# # # # # # # # # # # # # # # # # # # # # 
class RubyREPLTool
  attr_accessor :name, :description
  def initialize
    @name = 'Ruby REPL'
    @description = 'A Ruby shell. Use this to execute Ruby commands. Input should be a valid Ruby command. If you want to see the output of a value, you should print it out with `puts(...)`.'
  end

  def safer_eval(expression)
    result = nil
    Thread.start {
      $SAFE = 2
      result = eval(expression)
    }.join
    result
  end
  
  def use(command)
    safer_eval(command)
  end
end

class ChatLLM
  def initialize
    @model = 'gpt-3.5-turbo'
    @temperature = 0.0
    @client = OpenAI::Client.new(access_token: ENV['OPENAI_API_KEY'])
  end

  def generate(prompt, stop = nil)
    response = @client.chat(
      parameters: {
        model: @model,
        messages: [{ "role" => "user", "content" => prompt }],
        temperature: @temperature,
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

  attr_accessor :llm, :tools, :prompt_template, :max_loops, :stop_pattern
  def initialize(llm, tools)
    @llm = llm
    @tools = tools
    @prompt_template = PROMPT_TEMPLATE
    @max_loops = 15
    @stop_pattern = ["\n#{OBSERVATION_TOKEN}", "\n\t#{OBSERVATION_TOKEN}"]
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
    prompt = prompt_template % {
        today: Date.today,
        tool_description: tool_description,
        tool_names: tool_names,
        question: question,
        previous_responses: "%{previous_responses}"
    }
    puts prompt % { previous_responses: '' }
    while num_loops < max_loops
      num_loops += 1
      curr_prompt = prompt % { previous_responses: previous_responses.join("\n") }
      generated, tool, tool_input = decide_next_action(curr_prompt)
      if tool == 'Final Answer'
        return tool_input
      end
      if !tool_by_names.has_key?(tool)
        raise ArgumentError, "Unknown tool: #{tool}"
      end
      tool_result = tool_by_names[tool].use(tool_input)
      generated += "\n#{OBSERVATION_TOKEN} #{tool_result}\n#{THOUGHT_TOKEN}"
      puts generated
      previous_responses << generated
    end
  end

  def decide_next_action(prompt)
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
    if match.nil?
      raise ArgumentError, "Output of LLM is not parsable for next tool use: `#{generated}`"
    end
    tool = match[1].strip
    tool_input = match[2].strip.gsub(/(^"|"$)/, "")
    return tool, tool_input
  end
end

print "Enter a question / task for the agent: "
prompt = gets.chomp

agent = Agent.new(ChatLLM.new, [RubyREPLTool.new, SerpAPITool.new])
result = agent.run(prompt)

puts "Final answer is #{result}"