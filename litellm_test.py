from litellm import completion
import os

## set ENV variables

response = completion(
  model="claude-3-opus-20240229", 
  messages=[{ "content": "Hello, how are you?","role": "user"}]
)