# Configuration Reference

Environment variables and client configuration.

## Environment Variables

### OLLAMA_HOST

Configures the Ollama server address.

```bash
# Default
export OLLAMA_HOST=http://127.0.0.1:11434

# Custom port
export OLLAMA_HOST=http://127.0.0.1:11435

# Remote server
export OLLAMA_HOST=http://192.168.1.100:11434

# With path
export OLLAMA_HOST=http://server.com:11434/ollama

# HTTPS
export OLLAMA_HOST=https://ollama.example.com
```

**Usage**:
```python
import ollama

# Uses OLLAMA_HOST environment variable
response = ollama.chat(model='gemma3', messages=[...])

# Or override with Client
from ollama import Client
client = Client(host='http://custom:11434')
```

### OLLAMA_API_KEY

API key for Ollama cloud services.

```bash
export OLLAMA_API_KEY=your_api_key_here
```

**Get your key**: https://ollama.com/settings/keys

**Usage**:
```python
import os
from ollama import Client

# Auto-included if OLLAMA_API_KEY is set
client = Client(host='https://ollama.com')

# Or explicit
client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)
```

## Client Configuration

### Default Client

```python
import ollama

# Uses defaults + OLLAMA_HOST
response = ollama.chat(model='gemma3', messages=[...])
```

### Custom Host

```python
from ollama import Client

client = Client(host='http://localhost:11434')
response = client.chat(model='gemma3', messages=[...])
```

### Custom Headers

```python
from ollama import Client

client = Client(
  host='http://localhost:11434',
  headers={
    'X-Custom-Header': 'value',
    'Authorization': 'Bearer token'
  }
)
```

### Timeout Configuration

```python
from ollama import Client

# No timeout (wait indefinitely)
client = Client(timeout=None)

# Custom timeout in seconds
client = Client(timeout=120.0)
```

### HTTPX Options

All extra kwargs passed to httpx.Client:

```python
from ollama import Client

client = Client(
  host='http://localhost:11434',
  verify=False,          # Disable SSL verification
  proxies='http://proxy:8080',
  follow_redirects=True  # Default
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

# Access cloud models
for chunk in client.chat('gpt-oss:120b-cloud', messages=[...], stream=True):
  print(chunk.message.content, end='')
```

## Async Client Configuration

```python
from ollama import AsyncClient

# Same options as sync Client
client = AsyncClient(
  host='http://localhost:11434',
  headers={'X-Custom': 'value'},
  timeout=60.0
)
```

## Host URL Parsing

The client intelligently parses host URLs:

| Input | Parsed As |
|-------|-----------|
| `None` or `''` | `http://127.0.0.1:11434` |
| `1.2.3.4` | `http://1.2.3.4:11434` |
| `:56789` | `http://127.0.0.1:56789` |
| `1.2.3.4:56789` | `http://1.2.3.4:56789` |
| `http://1.2.3.4` | `http://1.2.3.4:80` |
| `https://1.2.3.4` | `https://1.2.3.4:443` |
| `example.com` | `http://example.com:11434` |
| `example.com:56789` | `http://example.com:56789` |
| `example.com/path` | `http://example.com:11434/path` |

## create_blob() - Upload Large Files

Upload files for use in model creation:

```python
from pathlib import Path
from ollama import Client

client = Client()

# Upload a file
digest = client.create_blob('/path/to/model.gguf')
print(f'Blob digest: {digest}')  # sha256:abc123...

# Use in model creation
client.create(
  model='my-model',
  files={'model.gguf': digest}
)
```

### Async Version

```python
from ollama import AsyncClient

async def upload_file():
  client = AsyncClient()
  digest = await client.create_blob('/path/to/file.bin')
  print(f'Uploaded: {digest}')
```

### Use Cases

1. **Custom models** - Upload GGUF files
2. **Adapters** - Upload LoRA adapters
3. **Large files** - Avoid base64 encoding in request

**Note**: Files are hashed with SHA-256. The digest is returned immediately after upload.

## Error Handling

```python
import ollama

try:
  response = ollama.chat(model='gemma3', messages=[...])
except ConnectionError:
  print('Cannot connect to Ollama')
  print('Make sure Ollama is running: ollama serve')
except ollama.ResponseError as e:
  if e.status_code == 404:
    print(f'Model not found: {e.error}')
    ollama.pull('gemma3')
  else:
    print(f'Error: {e.error} (status: {e.status_code})')
```

## Best Practices

1. **Use environment variables** for deployment flexibility
2. **Set timeouts** for production applications
3. **Handle errors** gracefully (connection, model not found)
4. **Use AsyncClient** for high-throughput applications
5. **Keep API key secret** - Never commit to source control