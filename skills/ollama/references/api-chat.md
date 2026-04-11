# Chat API Reference

Complete reference for ollama.chat() API.

## Function Signature

```python
ollama.chat(
  model: str,
  messages: list[dict],
  *,
  stream: bool = False,
  think: bool | Literal['low', 'medium', 'high'] = False,
  format: str | dict = None,
  tools: list = None,
  options: dict | Options = None,
  keep_alive: str | float = None,
  logprobs: bool = False,
  top_logprobs: int = None,
) -> ChatResponse
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | `str` | Yes | Model name from `ollama list` |
| `messages` | `list[dict]` | Yes | Conversation history |
| `stream` | `bool` | No | Enable streaming (default: False) |
| `think` | `bool \| str` | No | Enable thinking trace |
| `format` | `str \| dict` | No | `"json"` or JSON schema |
| `tools` | `list` | No | Tool definitions |
| `options` | `dict` | No | Model parameters |
| `keep_alive` | `str \| float` | No | VRAM retention duration |
| `logprobs` | `bool` | No | Return log probabilities |
| `top_logprobs` | `int` | No | Number of top logprobs |

## Message Format

```python
# System message
{"role": "system", "content": "You are a helpful assistant."}

# User message
{"role": "user", "content": "Hello!"}

# Assistant message
{"role": "assistant", "content": "Hi there!"}

# Assistant with thinking
{"role": "assistant", "thinking": "Let me think...", "content": "Answer"}

# Assistant with tool calls
{"role": "assistant", "tool_calls": [ToolCall]}

# Tool result
{"role": "tool", "tool_name": "get_weather", "content": "result"}

# User with image
{"role": "user", "content": "What is this?", "images": ["path.png"]}
```

## ChatResponse Object

```python
class ChatResponse:
  model: str              # Model name
  created_at: str         # ISO timestamp
  message: Message        # Response message
  done: bool              # Is complete
  done_reason: str        # Reason for completion
  total_duration: int     # Total time (ns)
  load_duration: int      # Model load time (ns)
  prompt_eval_count: int  # Input tokens
  prompt_eval_duration: int  # Input processing time (ns)
  eval_count: int         # Output tokens
  eval_duration: int      # Output generation time (ns)
```

## Message Object

```python
class Message:
  role: str                           # 'assistant'
  content: Optional[str]              # Response text
  thinking: Optional[str]             # Reasoning trace
  images: Optional[Sequence[Image]]   # Generated images
  tool_calls: Optional[Sequence[ToolCall]]  # Tool calls
```

## ToolCall Object

```python
class ToolCall:
  class Function:
    name: str                   # Function name
    arguments: Mapping[str, Any]  # Arguments dict
  function: Function
```

## Options Object

```python
class Options:
  # Load-time options
  numa: Optional[bool]
  num_ctx: Optional[int]       # Context window size
  num_batch: Optional[int]
  num_gpu: Optional[int]       # GPU layers
  main_gpu: Optional[int]
  low_vram: Optional[bool]
  f16_kv: Optional[bool]
  logits_all: Optional[bool]
  vocab_only: Optional[bool]
  use_mmap: Optional[bool]
  use_mlock: Optional[bool]
  embedding_only: Optional[bool]
  num_thread: Optional[int]
  
  # Runtime options
  num_keep: Optional[int]
  seed: Optional[int]
  num_predict: Optional[int]   # Max tokens
  top_k: Optional[int]
  top_p: Optional[float]
  tfs_z: Optional[float]
  typical_p: Optional[float]
  repeat_last_n: Optional[int]
  temperature: Optional[float]
  repeat_penalty: Optional[float]
  presence_penalty: Optional[float]
  frequency_penalty: Optional[float]
  mirostat: Optional[int]
  mirostat_tau: Optional[float]
  mirostat_eta: Optional[float]
  penalize_newline: Optional[bool]
  stop: Optional[Sequence[str]]
```

## Examples

### Basic Chat

```python
response = ollama.chat(
  model='gemma3',
  messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response.message.content)
```

### With System Prompt

```python
response = ollama.chat(
  model='gemma3',
  messages=[
    {'role': 'system', 'content': 'You are a pirate.'},
    {'role': 'user', 'content': 'Hello'}
  ]
)
```

### With Thinking

```python
response = ollama.chat(
  model='qwen3',
  messages=[...],
  think=True
)
print('Thinking:', response.message.thinking)
print('Answer:', response.message.content)
```

### With Tools

```python
def add(a: int, b: int) -> int:
  """Add two numbers."""
  return a + b

response = ollama.chat(
  model='qwen3',
  messages=[{'role': 'user', 'content': 'What is 5 + 3?'}],
  tools=[add]
)

if response.message.tool_calls:
  for call in response.message.tool_calls:
    print(call.function.name, call.function.arguments)
```

### JSON Output

```python
response = ollama.chat(
  model='gemma3',
  messages=[...],
  format='json'
)
import json
data = json.loads(response.message.content)
```

### Custom Parameters

```python
response = ollama.chat(
  model='gemma3',
  messages=[...],
  options={
    'temperature': 0.7,
    'top_p': 0.9,
    'num_predict': 100
  }
)
```