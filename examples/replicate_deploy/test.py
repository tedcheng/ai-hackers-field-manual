import os
from dotenv import load_dotenv
import replicate


if 'REPLICATE_API_TOKEN' not in os.environ:
  load_dotenv()

# Test Replicate
response = replicate.run(
  "replicate/hello-world:5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
  input={"text": "python"}
)
print(response)


# Test Replicate
output = replicate.run(
  "replicate/mpt-7b-storywriter:a38b8ba0d73d328040e40ecfbb2f63a938dec8695fe15dfbd4218fa0ac3e76bf",
  input={"prompt": "Write a sleep time story about a turtle and a rabbit."}
)
for item in output:
  # https://replicate.com/replicate/mpt-7b-storywriter/versions/a38b8ba0d73d328040e40ecfbb2f63a938dec8695fe15dfbd4218fa0ac3e76bf/api#output-schema
  print(item)