# ChatGPT Plugin
## Simple Example
OpenAI actually has very detailed [documentation](https://platform.openai.com/docs/plugins/introduction) on how to setup a plugin. Here's an [example](examples/plugin/app.py) app. 

https://user-images.githubusercontent.com/4744549/232259194-c6346ce2-fd8a-4288-937a-9f53245f9adf.mov

Some tips:
- At a high level, a plugin is just an API endpoint that ChatGPT can call. Setting up a plugin requires 3 parts: 1). your api endpoint, 2). a manifest file describing your plugin, and 3). a yaml file describing your endpoint(s). See more details in the [example](examples/plugin/app.py) app. 
- Setting up plugins to run locally may be a bit tricky. Make sure you are setting CORS correctly and explicitly setting a port number. For some reason, the default port number didn't work for me. 
- Make sure your /.well-known/ai-plugin.json and openai.yaml endpoints return with 200 and don't invole any redirects. OpenAI will not follow through the redirects.
- You can use chatgpt to write the manifest files for you. Just give it an example and describe the input and output. It will generate the manifest file scafolidng for you.
- Regarding prompts in the manifest, start with something simple and build on it. You don't need to overthink it in V1. 

## Chaining Calls
🚧 Under Construction


## Flexible Endpoints
🚧 Under Construction


## Memory
🚧 Under Construction