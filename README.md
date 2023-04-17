# AI Hackers' Field Manual
📚 Collections of common [[application patterns]](#patterns), [[tools]](#tools), [[models]](#models), and [[research papers]](#papers) for building AI applications. 🔍

🔥 New applications and content updated every week! 📅



## Application Patterns and Examples <a name="patterns"></a>
Have ideas for other patterns? Open an PR and create a new folder under examples. Or simply open an issue and we can discuss it. 

| Name          | Example Description                      | Community Projects        |
|---------------|------------------------------------------|---------------------------|
| [LLM Agent](examples/llm_agents) | Thought, Action, Observation Agent built from scratch | [Microsoft's Jarvis](https://github.com/microsoft/JARVIS), [Google's Palm](https://blog.google/technology/ai/introducing-pathways-next-generation-ai-architecture/), [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)|
| [ChatGPT Plugin](examples/plugin) | A plugin looking up real time Bart schedule | |
| Semantic Search and Q&A Bots | 🚧 Under Construction | |

## Tools <a name="tools"></a>
Common tools you will come across as you explore projects built in the community. 

| Name | Description |
|------|-------------|
| [Flask](https://flask.palletsprojects.com/en/2.1.x/) | A lightweight web framework for Python. Since Python is the language of AI, you might as well use a web framework in Python. Another common option is [FastAPI](https://fastapi.tiangolo.com/). |
| [Next.js](https://nextjs.org/docs) | A popular Javascript framework, often used with Vercel. |
| [Vercel](https://vercel.com) | A cloud platform specialized in hosting Next.js apps. |
| [Tailwindcss](https://tailwindcss.com/docs) | A utility-first CSS framework, which means you will define styling directly with pre-built css classes. |
| [Pinecone](https://www.pinecone.io/docs) | A vector database for AI applications. This is commonly used to store embeddings of data and enable similarity based search (More on this in Q&A bots). Alternatively, you can also use [Milvus](https://milvus.io/), [Faiss](https://github.com/facebookresearch/faiss), [Chroma](https://www.trychroma.com/) and [Weaviate](https://weaviate.io/) and others. |
| [Supabase](https://supabase.com/) | A popular PostgresQL as a service vendor. Works well with NextJS and offers Authentication and storage APIs out of the box. Also has support for storing embeddings (using a Postgres plugin - pgvector) and files. |
| [LlamaIndex](https://github.com/jerryjliu/llama_index) | A library that provides an interface between LLMs and external data by handling data connectors, building indices and querying (e.g., including managing prompt token size, etc.). |
| [LangChain](https://github.com/hwchase17/langchain) | A library that helps you build LLM based complex action chains and agents. |
| [OpenAI API](https://platform.openai.com/docs/api-reference) | Currently the state of the art models. Commonly used APIs include: <ul><li>Whisper - Audio to text. This is also open-sourced, so you can run your own service.</li><li>Embedding - Generate high dimensional representation based on text and can be used for semantic search.</li><li>Text completions and chat completions - The API behind ChatGPT. Multiple models exist. gpt-4 is the state of art, but general use cases can be done on gpt-3.5-turbo (cheaper and faster).</li><li>DALLE - Text to image.</li></ul> |
| [HuggingFace](https://huggingface.co/) | The GitHub for AI models, a platform to build, deploy, and share models across the community. An alternative to OpenAI models. |
| [ElevenLabs](https://beta.elevenlabs.io/) | AI text to speech API. Voice cloning. |

## Current State of Models + Training <a name="models"></a>
🚧 Under Construction

## Key research papers <a name="papers"></a>
🚧 Under Construction