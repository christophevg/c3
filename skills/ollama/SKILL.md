---
name: ollama
description: Guide Python ollama library for LLM integration including chat, tool calling, streaming, embeddings, model management, web search, and image generation. Use when user mentions ollama or imports ollama in Python. Examples: "using ollama", "ollama.chat", "from ollama import".
---

# Ollama

Guide Python's ollama library for local LLM integration including chat, tool calling, streaming, embeddings, and model management.

## Overview

| Capability | Description |
|------------|-------------|
| Chat API | Conversational AI with streaming and thinking |
| Tool Calling | Function calling for agentic workflows |
| Generate API | Single prompt generation with structured output |
| Embeddings | Text vectorization |
| Model Management | List, pull, push, create, delete models |
| Vision | Image analysis with multimodal models |
| Image Generation | Experimental image creation (macOS) |
| Web Search/Fetch | Search and fetch web content (cloud API) |
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

### Environment Variables

```bash
# Ollama server address (default: http://127.0.0.1:11434)
export OLLAMA_HOST=http://localhost:11434

# API key for cloud services (web search, cloud models)
export OLLAMA_API_KEY=your_api_key
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

See `references/configuration.md` for full configuration options.

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

### Generate Parameters

| Parameter | Description |
|-----------|-------------|
| `model` | Model name |
| `prompt` | Input prompt |
| `suffix` | Text to append after generation (FIM) |
| `system` | System prompt |
| `context` | Token array from previous response |
| `stream` | Enable streaming |
| `think` | Enable thinking trace |
| `format` | JSON schema for structured output |
| `images` | Images for multimodal input |
| `options` | Model parameters |
| `logprobs` | Return log probabilities |

See `references/api-generate.md` for full reference.

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

# Push model to registry
ollama.push('username/gemma3')

# Delete model
ollama.delete('gemma3')

# Model details
info = ollama.show('gemma3')

# Running models
running = ollama.ps()

# Copy model
ollama.copy('gemma3', 'backup/gemma3')

# Create custom model
ollama.create(
  model='my-assistant',
  from_='gemma3',
  system='You are a helpful assistant.'
)
```

See `references/api-models.md` for full reference.

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

## Web Search/Fetch (Cloud API)

Requires `OLLAMA_API_KEY` environment variable.

```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)

# Search the web
results = client.web_search('Python async best practices', max_results=5)
for result in results.results:
  print(f"{result.title}: {result.url}")

# Fetch a web page
page = client.web_fetch('https://python.org')
print(page.content)
```

See `references/api-web.md` for full reference.

## Image Generation (Experimental)

Currently macOS only.

```python
import base64
import ollama

# Generate image
response = ollama.generate(
  model='x/z-image-turbo',
  prompt='a sunset over mountains'
)

with open('output.png', 'wb') as f:
  f.write(base64.b64decode(response.image))
```

See `patterns/image-generation.md` for patterns.

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
- `patterns/image-generation.md` - Image generation patterns

## Template Files

- `templates/chat-agent.md` - Basic chat agent
- `templates/tool-agent.md` - Agent with tools

## Reference Files

- `references/api-chat.md` - Chat API reference
- `references/api-generate.md` - Generate API reference
- `references/api-models.md` - Model management API
- `references/api-web.md` - Web search/fetch API
- `references/response-objects.md` - Response types
- `references/configuration.md` - Environment variables and client config

## Related Skills

- python - Base skill for Python development
- claude-api - For Anthropic/Claude API usage