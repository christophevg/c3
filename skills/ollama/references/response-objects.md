# Response Objects Reference

Complete reference for ollama response types.

## ChatResponse

```python
class ChatResponse:
  model: str                    # Model name
  created_at: str               # ISO timestamp
  message: Message              # Response message
  done: bool                    # Completion status
  done_reason: str              # 'stop', 'length', 'tool_call'
  
  # Timing metrics (nanoseconds)
  total_duration: int           # Total processing time
  load_duration: int            # Model loading time
  prompt_eval_count: int        # Input tokens processed
  prompt_eval_duration: int     # Input processing time
  eval_count: int               # Output tokens generated
  eval_duration: int            # Output generation time
```

## Message

```python
class Message:
  role: str                           # 'assistant'
  content: Optional[str]              # Response text
  thinking: Optional[str]             # Reasoning trace (if think=True)
  images: Optional[Sequence[Image]]   # Generated images
  tool_calls: Optional[Sequence[ToolCall]]  # Function calls
  tool_name: Optional[str]            # For tool role messages
```

## GenerateResponse

```python
class GenerateResponse:
  model: str                    # Model name
  created_at: str               # ISO timestamp
  response: str                 # Generated text
  thinking: str                 # Reasoning trace (if think=True)
  done: bool                    # Completion status
  context: list[int]             # Token array for continuity
  
  # Timing metrics
  total_duration: int
  load_duration: int
  prompt_eval_count: int
  prompt_eval_duration: int
  eval_count: int
  eval_duration: int
```

## EmbedResponse

```python
class EmbedResponse:
  embeddings: Sequence[Sequence[float]]  # List of vectors
```

## ToolCall

```python
class ToolCall:
  class Function:
    name: str                        # Function name
    arguments: Mapping[str, Any]      # Arguments as dict
  function: Function
```

**Accessing**:
```python
for call in response.message.tool_calls:
  name = call.function.name
  args = dict(call.function.arguments)
  result = execute(name, **args)
```

## Model (from list)

```python
class Model:
  model: str               # Model name
  modified_at: datetime     # Last modified timestamp
  digest: str              # Content hash
  size: int                # Size in bytes
  details: ModelDetails    # Model metadata
```

## ModelDetails

```python
class ModelDetails:
  parent_model: str
  format: str              # 'gguf'
  family: str              # Model family
  families: Optional[List[str]]
  parameter_size: str      # '7B', '13B', etc.
  quantization_level: str  # 'Q4_0', 'Q8_0', etc.
```

## Options

```python
class Options:
  # Load-time options
  numa: Optional[bool]             # NUMA support
  num_ctx: Optional[int]           # Context window (default: 2048)
  num_batch: Optional[int]         # Batch size
  num_gpu: Optional[int]           # GPU layers (-1 = all)
  main_gpu: Optional[int]          # Primary GPU
  low_vram: Optional[bool]         # Low VRAM mode
  f16_kv: Optional[bool]           # FP16 key/value
  logits_all: Optional[bool]       # Return all logits
  vocab_only: Optional[bool]       # Vocab only
  use_mmap: Optional[bool]          # Memory-mapped file
  use_mlock: Optional[bool]        # Lock memory
  embedding_only: Optional[bool]   # Embedding mode
  num_thread: Optional[int]        # CPU threads
  
  # Runtime options
  num_keep: Optional[int]          # Tokens to keep
  seed: Optional[int]              # Random seed
  num_predict: Optional[int]       # Max tokens (-1 = infinite)
  top_k: Optional[int]             # Top-k sampling (default: 40)
  top_p: Optional[float]           # Top-p sampling (default: 0.9)
  tfs_z: Optional[float]           # Tail-free sampling
  typical_p: Optional[float]       # Typical sampling
  repeat_last_n: Optional[int]     # Repeat window
  temperature: Optional[float]     # Temperature (default: 0.8)
  repeat_penalty: Optional[float]  # Repeat penalty (default: 1.1)
  presence_penalty: Optional[float]
  frequency_penalty: Optional[float]
  mirostat: Optional[int]          # Mirostat version (0, 1, 2)
  mirostat_tau: Optional[float]    # Mirostat target
  mirostat_eta: Optional[float]   # Mirostat learning rate
  penalize_newline: Optional[bool]
  stop: Optional[Sequence[str]]   # Stop sequences
```

## ProgressResponse (pull/push)

```python
class ProgressResponse:
  status: str              # 'pulling', 'pushing', 'complete'
  digest: str              # Layer digest
  total: Optional[int]     # Total bytes
  completed: Optional[int] # Completed bytes
```

## ShowResponse

```python
class ShowResponse:
  modelfile: str           # Modelfile content
  parameters: str          # Parameters section
  template: str            # Prompt template
  details: ModelDetails    # Model metadata
  license: str             # License text
  capabilities: list       # ['completion', 'chat', 'vision']
```

## ListResponse

```python
class ListResponse:
  models: Sequence[Model]  # Available models
```

## RunningModel (from ps)

```python
class RunningModel:
  model: str               # Model name
  name: str                # Display name
  digest: str              # Content hash
  expires_at: datetime     # Expiration time
  size: int                # Total size (bytes)
  size_vram: int           # VRAM usage (bytes)
  details: ModelDetails
```

## Error Types

```python
class RequestError(Exception):
  error: str               # Error message

class ResponseError(Exception):
  error: str               # Error message
  status_code: int         # HTTP status code (-1 if unknown)
```

## Usage Examples

### Check Token Usage

```python
response = ollama.chat(model='gemma3', messages=[...])

input_tokens = response.prompt_eval_count
output_tokens = response.eval_count
total_time_ms = response.total_duration / 1e6

print(f"Tokens: {input_tokens} in, {output_tokens} out")
print(f"Time: {total_time_ms:.1f}ms")
```

### Handle Done Reason

```python
response = ollama.chat(model='gemma3', messages=[...])

if response.done_reason == 'length':
  print("Response truncated")
elif response.done_reason == 'tool_call':
  print("Tool call requested")
elif response.done_reason == 'stop':
  print("Natural end")
```

### Get Embedding Dimensions

```python
response = ollama.embed(model='nomic-embed-text', input='text')
dims = len(response.embeddings[0])
print(f"Embedding dimension: {dims}")
```