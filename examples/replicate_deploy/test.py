import os
from dotenv import load_dotenv
import replicate

load_dotenv()

response = replicate.run(
  "replicate/hello-world:5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
  input={"text": "python"}
)

print(response)
