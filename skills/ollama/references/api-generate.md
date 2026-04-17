# Generate API Reference

Complete reference for ollama.generate() API.

## Function Signature

```python
ollama.generate(
  model: str,
  prompt: str = '',
  *,
  suffix: str = None,
  system: str = None,
  template: str = None,
  context: Sequence[int] = None,
  stream: bool = False,
  think: bool | Literal['low', 'medium', 'high'] = False,
  format: str | dict = None,
  images: Sequence = None,
  options: dict | Options = None,
  keep_alive: str | float = None,
  raw: bool = False,
  logprobs: bool = False,
  top_logprobs: int = None,
  width: int = None,   # Image generation
  height: int = None,  # Image generation
  steps: int = None,   # Image generation
) -> GenerateResponse
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name |
| `prompt` | `str` | Input prompt |
| `suffix` | `str` | Text to append after generation |
| `system` | `str` | System prompt |
| `template` | `str` | Prompt template |
| `context` | `list[int]` | Token array from previous response |
| `stream` | `bool` | Enable streaming |
| `think` | `bool \| str` | Enable thinking trace |
| `format` | `str \| dict` | `"json"` or JSON schema |
| `images` | `Sequence` | Images for multimodal |
| `options` | `dict` | Model parameters |
| `keep_alive` | `str \| float` | VRAM retention |
| `raw` | `bool` | Skip template processing |
| `logprobs` | `bool` | Return log probabilities |
| `top_logprobs` | `int` | Top alternatives per token (0-20) |
| `width` | `int` | Image width (pixels) |
| `height` | `int` | Image height (pixels) |
| `steps` | `int` | Diffusion steps |

## GenerateResponse Object

```python
class GenerateResponse:
  model: str                    # Model name
  created_at: str               # ISO timestamp
  response: str                 # Generated text
  thinking: str                 # Thinking trace
  done: bool                    # Completion status
  done_reason: str              # 'stop', 'length'
  context: Sequence[int]        # Token array for continuity
  
  # Timing (nanoseconds)
  total_duration: int
  load_duration: int
  prompt_eval_count: int
  prompt_eval_duration: int
  eval_count: int
  eval_duration: int
  
  # Logprobs
  logprobs: Sequence[Logprob]
  
  # Image generation
  image: str                    # Base64-encoded image
  completed: int                # Progress: completed steps
  total: int                    # Progress: total steps
```

## Basic Usage

```python
import ollama

response = ollama.generate(
  model='gemma3',
  prompt='Why is the sky blue?'
)

print(response.response)
```

## Multi-Turn with Context

```python
import ollama

# First turn
response1 = ollama.generate(
  model='gemma3',
  prompt='What is Python?'
)

print(response1.response)

# Second turn - continue conversation
response2 = ollama.generate(
  model='gemma3',
  prompt='Tell me more about its features.',
  context=response1.context  # Pass token array
)

print(response2.response)
```

## Streaming

```python
import ollama

stream = ollama.generate(
  model='gemma3',
  prompt='Write a haiku about code',
  stream=True
)

for chunk in stream:
  if chunk.response:
    print(chunk.response, end='', flush=True)

print()
```

## JSON Output

```python
import ollama
import json

response = ollama.generate(
  model='gemma3',
  prompt='List 3 fruits as JSON',
  format='json'
)

data = json.loads(response.response)
print(data)
```

## Structured Output with Schema

```python
from pydantic import BaseModel
import ollama

class Person(BaseModel):
  name: str
  age: int
  occupation: str

response = ollama.generate(
  model='llama3.1',
  prompt='Generate a person profile',
  format=Person.model_json_schema()
)

person = Person.model_validate_json(response.response)
print(person)
```

## Thinking Mode

```python
import ollama

response = ollama.generate(
  model='deepseek-r1',
  prompt='What is 15 * 23?',
  think=True
)

print('Thinking:', response.thinking)
print('Answer:', response.response)
```

## Multimodal with Images

```python
import ollama

response = ollama.generate(
  model='gemma3',
  prompt='Describe this image',
  images=['/path/to/image.png']
)

print(response.response)
```

## Fill-in-the-Middle (FIM)

```python
import ollama

response = ollama.generate(
  model='codellama',
  prompt='def fibonacci(n):',
  suffix='\n  return result'
)

print(response.response)
```

## Log Probabilities

```python
import ollama

response = ollama.generate(
  model='gemma3',
  prompt='Complete: The capital of France is',
  logprobs=True,
  top_logprobs=5
)

for logprob in response.logprobs:
  print(f"Token: {logprob.token}, LogProb: {logprob.logprob:.4f}")
  if logprob.top_logprobs:
    for alt in logprob.top_logprobs:
      print(f"  Alternative: {alt.token} ({alt.logprob:.4f})")
```

## Image Generation (Experimental)

Currently only available on macOS with supported models:

```python
import base64
import ollama

# Stream image generation
for chunk in ollama.generate(
  model='x/z-image-turbo',
  prompt='a sunset over mountains',
  stream=True
):
  if chunk.image:
    # Final result
    with open('output.png', 'wb') as f:
      f.write(base64.b64decode(chunk.image))
    print('Image saved!')
  elif chunk.total:
    # Progress update
    print(f'Progress: {chunk.completed}/{chunk.total}', end='\r')
```

## Custom Parameters

```python
import ollama

response = ollama.generate(
  model='gemma3',
  prompt='Creative writing prompt',
  options={
    'temperature': 0.9,
    'top_p': 0.95,
    'top_k': 40,
    'num_predict': 500,
    'stop': ['\n\n', 'THE END']
  }
)

print(response.response)
```

## System Prompt

```python
import ollama

response = ollama.generate(
  model='gemma3',
  prompt='Hello!',
  system='You are a helpful pirate. Always respond in pirate speak.'
)

print(response.response)
```

## Key Differences from Chat API

| Feature | generate() | chat() |
|---------|------------|-------|
| Input | Single prompt | Message history |
| Context | Token array | Full messages |
| System | Parameter | Message role |
| Use case | Single-shot | Conversation |