![Screen_Shot_2023-04-12_at_4_35_34_PM](https://user-images.githubusercontent.com/4744549/233222264-2f373e68-8f94-43bc-a743-bc163c6b4c71.png)

# LLM Agent
This is a pattern popularized by AutoGPT & BabyAGI projects. With this pattern, an agent is given a set of tools and is tasked to complete a goal. In each step, the agent uses LLM to iteratively decide which tool to use and solves the problem. Inspired by [LLM Agents](https://github.com/mpaepper/llm_agents/tree/main/llm_agents) and LangChain, here's is a built-from-scratch version in less than [150 lines of ruby] that implements a Thought, Action, Observation, Thought loop agent with access to Google Search and Ruby REPL.  
