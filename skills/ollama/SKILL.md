---
name: ollama
description: Guide Python ollama library for LLM integration including chat, tool calling, streaming, embeddings, and model management. Use when user mentions ollama or llm in Python context. Primary use case: agentic loops with tool calling.
---

# Ollama

Guide Python's ollama library for local LLM integration including chat, tool calling, streaming, embeddings, and model management.

## Overview

| Capability | Description |
|------------|-------------|
| Chat API | Conversational AI with streaming and thinking |
| Tool Calling | Function calling for agentic workflows |
| Generate API | Single prompt generation |
| Embeddings | Text vectorization |
| Model Management | List, pull, push, create, delete models |
| Vision | Image analysis with multimodal models |
| Cloud Models | Access cloud-hosted models via ollama.com |

## When to Use This Skill

Use this skill when:
- User mentions "ollama" or "llm" in Python context
- Code imports `ollama` or `from ollama import`
- Building agents with tool calling
- Need local/self-hosted LLM integration

## Client Initialization

### Default (Module-Level)

```python
import ollama

response = ollama.chat(model='gemma3', messages=[...])
```

### Custom Client

```python
from ollama import Client

client = Client(
  host='http://localhost:11434',
  headers={'x-custom': 'value'}
)
```

### Cloud API Client

```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)
```

### Async Client

```python
from ollama import AsyncClient

async def main():
  client = AsyncClient()
  response = await client.chat(model='gemma3', messages=[...])
```

## Chat API

### Basic Chat

```python
response = ollama.chat(
  model='gemma3',
  messages=[
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'Hello!'},
  ]
)
print(response.message.content)
```

### Streaming Chat

```python
stream = ollama.chat(
  model='gemma3',
  messages=[...],
  stream=True
)

for chunk in stream:
  if chunk.message.content:
    print(chunk.message.content, end='', flush=True)
```

### Chat Parameters

| Parameter | Description |
|-----------|-------------|
| `model` | Model name (from `ollama list`) |
| `messages` | Conversation history |
| `stream` | Enable streaming (default: False) |
| `think` | Enable thinking/reasoning trace |
| `format` | `"json"` or JSON schema for structured output |
| `tools` | Tool definitions for function calling |
| `options` | Model parameters (temperature, etc.) |
| `keep_alive` | VRAM retention (e.g., `"5m"`, `"0"`) |

## Tool Calling

### Define Tools

```python
# Python function (SDK auto-parses docstring)
def get_weather(city: str) -> str:
  """Get the current weather for a city.
  Args:
    city: The name of the city
  Returns:
    The current weather description
  """
  # Implementation
  return f"Weather in {city}: Sunny"

# Or explicit tool definition
tools = [{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get weather for a city",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {"type": "string"}
      },
      "required": ["city"]
    }
  }
}]
```

### Handle Tool Calls

```python
response = ollama.chat(model='qwen3', messages=messages, tools=[get_weather])

if response.message.tool_calls:
  for call in response.message.tool_calls:
    result = execute_tool(call.function.name, **call.function.arguments)
    messages.append({
      'role': 'tool',
      'tool_name': call.function.name,
      'content': str(result)
    })
```

See `patterns/tool-calling.md` for detailed patterns.

## Agentic Loop

```python
while True:
  response = client.chat(model='qwen3', messages=messages, tools=tools)
  
  if not response.message.tool_calls:
    break  # Done
  
  for call in response.message.tool_calls:
    result = available_tools[call.function.name](**call.function.arguments)
    messages.append({
      'role': 'tool',
      'tool_name': call.function.name,
      'content': str(result)
    })

# Final response
print(response.message.content)
```

See `patterns/agentic-loop.md` for streaming version.

## Streaming with Accumulation

**Critical**: Always accumulate partial fields for conversation history.

```python
content = ''
thinking = ''
tool_calls = []

for chunk in stream:
  if chunk.message.thinking:
    thinking += chunk.message.thinking
  if chunk.message.content:
    content += chunk.message.content
  if chunk.message.tool_calls:
    tool_calls.extend(chunk.message.tool_calls)

# Append accumulated fields for next request
messages.append({
  'role': 'assistant',
  'thinking': thinking,
  'content': content,
  'tool_calls': tool_calls
})
```

## Generate API

```python
response = ollama.generate(
  model='gemma3',
  prompt='Why is the sky blue?'
)
print(response.response)
```

## Embeddings

```python
# Single input
response = ollama.embed(model='nomic-embed-text', input='text to embed')
vector = response.embeddings[0]

# Batch
response = ollama.embed(model='nomic-embed-text', input=['text1', 'text2'])
```

## Model Management

```python
# List models
models = ollama.list()

# Pull model
ollama.pull('gemma3')

# Delete model
ollama.delete('gemma3')

# Model details
info = ollama.show('gemma3')

# Running models
running = ollama.ps()
```

## Vision/Multimodal

```python
response = ollama.chat(
  model='gemma3',
  messages=[{
    'role': 'user',
    'content': 'What is in this image?',
    'images': ['/path/to/image.png']
  }]
)
```

## Error Handling

```python
import ollama

try:
  response = ollama.chat(model='gemma3', messages=[...])
except ollama.ResponseError as e:
  print(f'Error: {e.error} (status: {e.status_code})')
  if e.status_code == 404:
    ollama.pull('gemma3')
except ollama.RequestError as e:
  print(f'Request error: {e.error}')
except ConnectionError:
  print('Cannot connect to Ollama. Run: ollama serve')
```

## Pattern Files

- `patterns/agentic-loop.md` - Agent loop with streaming
- `patterns/streaming.md` - Streaming patterns
- `patterns/tool-calling.md` - Tool calling patterns

## Template Files

- `templates/chat-agent.md` - Basic chat agent
- `templates/tool-agent.md` - Agent with tools

## Reference Files

- `references/api-chat.md` - Chat API reference
- `references/api-models.md` - Model management API
- `references/response-objects.md` - Response types

## Related Skills

- python - Base skill for Python development
- claude-api - For Anthropic/Claude API usage