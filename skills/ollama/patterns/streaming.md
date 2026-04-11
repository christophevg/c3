# Streaming Patterns

Ollama streaming patterns for chat and generate.

## Basic Streaming

```python
import ollama

stream = ollama.chat(
  model='gemma3',
  messages=[{'role': 'user', 'content': 'Tell me a story'}],
  stream=True
)

for chunk in stream:
  if chunk.message.content:
    print(chunk.message.content, end='', flush=True)

print()  # Final newline
```

## Streaming with Accumulation

**Critical**: Accumulate partial fields for conversation history.

```python
import ollama

messages = [{'role': 'user', 'content': 'What is 17 × 23?'}]

stream = ollama.chat(model='qwen3', messages=messages, stream=True)

content = ''
for chunk in stream:
  if chunk.message.content:
    content += chunk.message.content
    print(chunk.message.content, end='', flush=True)

print()

# Append to messages for next request
messages.append({'role': 'assistant', 'content': content})
```

## Streaming with Thinking

```python
import ollama

messages = [{'role': 'user', 'content': 'Solve: 17 × 23'}]

stream = ollama.chat(
  model='qwen3',
  messages=messages,
  think=True,
  stream=True
)

thinking = ''
content = ''
in_thinking = False

for chunk in stream:
  if chunk.message.thinking:
    if not in_thinking:
      in_thinking = True
      print('[Thinking]\n', flush=True)
    thinking += chunk.message.thinking
    print(chunk.message.thinking, end='', flush=True)
  
  elif chunk.message.content:
    if in_thinking:
      in_thinking = False
      print('\n\n[Answer]\n', flush=True)
    content += chunk.message.content
    print(chunk.message.content, end='', flush=True)

print()

# Append both fields
messages.append({
  'role': 'assistant',
  'thinking': thinking,
  'content': content
})
```

## Streaming with Tools

```python
import ollama

messages = [{'role': 'user', 'content': 'What is the weather in NYC?'}]

stream = ollama.chat(
  model='qwen3',
  messages=messages,
  tools=[get_weather],
  stream=True
)

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

# Append accumulated fields
messages.append({
  'role': 'assistant',
  'thinking': thinking,
  'content': content,
  'tool_calls': tool_calls
})

# Execute tools if any
for call in tool_calls:
  result = get_weather(**call.function.arguments)
  messages.append({
    'role': 'tool',
    'tool_name': call.function.name,
    'content': str(result)
  })
```

## Generate Streaming

```python
import ollama

stream = ollama.generate(
  model='gemma3',
  prompt='Write a haiku about coding',
  stream=True
)

for chunk in stream:
  if chunk.response:
    print(chunk.response, end='', flush=True)
```

## Pull Model with Progress

```python
import ollama

for progress in ollama.pull('gemma3', stream=True):
  status = progress.get('status', '')
  completed = progress.get('completed', 0)
  total = progress.get('total', 0)
  
  if total > 0:
    percent = (completed / total) * 100
    print(f'\r{status}: {percent:.1f}%', end='', flush=True)

print('\nDone!')
```

## Key Accumulation Pattern

```python
# Initialize accumulators
content = ''
thinking = ''
tool_calls = []
images = []

# Accumulate in stream loop
for chunk in stream:
  if chunk.message.thinking:
    thinking += chunk.message.thinking
  if chunk.message.content:
    content += chunk.message.content
  if chunk.message.tool_calls:
    tool_calls.extend(chunk.message.tool_calls)
  if chunk.message.images:
    images.extend(chunk.message.images)

# Build message for next request
messages.append({
  'role': 'assistant',
  'thinking': thinking or None,
  'content': content or None,
  'tool_calls': tool_calls or None
})
```

## Why Accumulation Matters

When streaming, each chunk contains **partial** fields. For tool calling:
- Model emits thinking, tool_call, and tool result must be passed back
- Without accumulation, subsequent requests will fail

```python
# WRONG: Direct append without accumulation
for chunk in stream:
  messages.append(chunk.message)  # Incomplete!

# CORRECT: Accumulate first
content = ''
for chunk in stream:
  content += chunk.message.content or ''
messages.append({'role': 'assistant', 'content': content})
```