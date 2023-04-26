# LLM Agent

![Screen Shot 2023-04-25 at 11 38 54 PM](https://user-images.githubusercontent.com/4744549/234490462-e62904ac-d0c3-4a4a-974f-35459975d184.png)


This is a pattern popularized by AutoGPT & BabyAGI projects. With this pattern, an agent is given a set of tools and is tasked to complete a goal. In each step, the agent uses LLM to iteratively decide which tool to use and solves the problem. Inspired by [LLM Agents](https://github.com/mpaepper/llm_agents/tree/main/llm_agents) and LangChain, here's is a built-from-scratch version in less than [150 lines of ruby] that implements a Thought, Action, Observation, Thought loop agent with access to Google Search and Ruby REPL.  
