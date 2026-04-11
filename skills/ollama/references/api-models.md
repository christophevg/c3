# Model Management API Reference

Complete reference for ollama model management.

## list() - List Models

```python
response = ollama.list()
models = response['models']
```

**Returns**: `ListResponse` with `models: list[Model]`

```python
class Model:
  model: str           # Model name
  modified_at: datetime  # Last modified
  digest: str          # Content hash
  size: int            # Size in bytes
  details: ModelDetails
```

**Example**:
```python
for model in ollama.list()['models']:
  print(f"{model['model']}: {model['size'] / 1e9:.1f} GB")
```

## pull() - Download Model

```python
ollama.pull(model: str, *, stream: bool = False)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name |
| `stream` | `bool` | Stream progress |

**Example**:
```python
# Non-streaming
ollama.pull('gemma3')

# Streaming progress
for progress in ollama.pull('gemma3', stream=True):
  print(f"{progress['status']}: {progress.get('completed', 0)}/{progress.get('total', '?')}")
```

## push() - Upload Model

```python
ollama.push(model: str, *, stream: bool = False)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | Model name (must have user prefix) |
| `stream` | `bool` | Stream progress |

**Example**:
```python
ollama.push('username/gemma3')
```

## create() - Create Custom Model

```python
ollama.create(
  model: str,
  *,
  from_: str = None,
  quantize: str = None,
  files: Dict[str, str] = None,
  adapters: Dict[str, str] = None,
  template: str = None,
  license: str | List[str] = None,
  system: str = None,
  parameters: dict = None,
  messages: list = None,
  stream: bool = False
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | `str` | New model name |
| `from_` | `str` | Base model |
| `quantize` | `str` | Quantization method |
| `files` | `dict` | Training files |
| `adapters` | `dict` | Adapter files |
| `template` | `str` | Prompt template |
| `license` | `str \| list` | License info |
| `system` | `str` | System prompt |
| `parameters` | `dict` | Model parameters |
| `messages` | `list` | Example messages |
| `stream` | `bool` | Stream progress |

**Example**:
```python
ollama.create(
  model='my-assistant',
  from_='gemma3',
  system='You are a helpful coding assistant.',
  parameters={'temperature': 0.7}
)
```

## delete() - Remove Model

```python
ollama.delete(model: str)
```

**Example**:
```python
ollama.delete('gemma3')
```

## show() - Model Details

```python
response = ollama.show(model: str)
```

**Returns**:
```python
{
  'modelfile': str,
  'parameters': str,
  'template': str,
  'details': ModelDetails,
  'license': str,
  'capabilities': list
}
```

**Example**:
```python
info = ollama.show('gemma3')
print(info['modelfile'])
print(info['details'])
```

## copy() - Copy Model

```python
ollama.copy(source: str, destination: str)
```

**Example**:
```python
ollama.copy('gemma3', 'backup/gemma3')
```

## ps() - Running Models

```python
response = ollama.ps()
running = response['models']
```

**Returns**: List of running models with:
```python
{
  'model': str,
  'name': str,
  'digest': str,
  'expires_at': datetime,
  'size': int,
  'size_vram': int,
  'details': ModelDetails
}
```

**Example**:
```python
for model in ollama.ps()['models']:
  print(f"{model['model']}: expires in {model['expires_at']}")
```

## ModelDetails Object

```python
class ModelDetails:
  parent_model: str
  format: str
  family: str
  families: Optional[List[str]]
  parameter_size: str
  quantization_level: str
```

## Common Patterns

### Check Model Exists

```python
def model_exists(name: str) -> bool:
  models = [m['model'] for m in ollama.list()['models']]
  return name in models

if not model_exists('gemma3'):
  ollama.pull('gemma3')
```

### Get Model Size

```python
def get_model_size(name: str) -> int:
  for model in ollama.list()['models']:
    if model['model'] == name:
      return model['size']
  return 0

size_gb = get_model_size('gemma3') / 1e9
```

### Clean Up Old Models

```python
models_to_keep = {'gemma3', 'qwen3'}

for model in ollama.list()['models']:
  if model['model'] not in models_to_keep:
    print(f"Deleting {model['model']}")
    ollama.delete(model['model'])
```