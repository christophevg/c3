# Web Search/Fetch API Reference

Complete reference for ollama web search and fetch APIs.

## Prerequisites

Both `web_search` and `web_fetch` require authentication via Ollama API key:

```bash
export OLLAMA_API_KEY=your_api_key
```

Get your API key from https://ollama.com/settings/keys

## web_search() - Search the Web

```python
response = client.web_search(
  query: str,
  max_results: int = 3
) -> WebSearchResponse
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | Required | Search query |
| `max_results` | `int` | 3 | Maximum results to return |

**Returns**: `WebSearchResponse` with search results.

```python
class WebSearchResponse:
  results: Sequence[WebSearchResult]

class WebSearchResult:
  title: Optional[str]     # Page title
  url: Optional[str]       # Page URL
  content: Optional[str]   # Page snippet
```

**Example**:
```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)

results = client.web_search('Python async best practices', max_results=5)

for result in results.results:
  print(f"Title: {result.title}")
  print(f"URL: {result.url}")
  print(f"Content: {result.content[:100]}...")
  print()
```

## web_fetch() - Fetch Web Page

```python
response = client.web_fetch(
  url: str
) -> WebFetchResponse
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | URL to fetch |

**Returns**: `WebFetchResponse` with page content.

```python
class WebFetchResponse:
  title: Optional[str]          # Page title
  content: Optional[str]       # Main content
  links: Optional[Sequence[str]]  # Extracted links
```

**Example**:
```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)

page = client.web_fetch('https://python.org/doc/')

print(f"Title: {page.title}")
print(f"Content: {page.content[:500]}...")
print(f"Links: {len(page.links)} found")
```

## Using with Chat

Combine web search with chat for research:

```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
)

# Search for information
results = client.web_search('latest Python 3.12 features', max_results=3)

# Build context from results
context = '\n\n'.join(
  f"Source: {r.url}\n{r.content}"
  for r in results.results
)

# Ask about the results
response = client.chat(
  model='gpt-oss:120b-cloud',
  messages=[
    {'role': 'system', 'content': 'Answer based on the provided context.'},
    {'role': 'user', 'content': f'Context:\n{context}\n\nWhat are the key new features?'}
  ]
)

print(response.message.content)
```

## Error Handling

```python
import os
from ollama import Client

client = Client(
  host='https://ollama.com',
  headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)

try:
  results = client.web_search('test query')
except ValueError as e:
  if 'Authorization header' in str(e):
    print('Set OLLAMA_API_KEY environment variable')
  else:
    raise
```

## Important Notes

1. **Requires authentication** - Must set `OLLAMA_API_KEY` or pass Authorization header
2. **Cloud endpoint** - Requests go to `https://ollama.com/api/web_search` and `web_fetch`
3. **Rate limits** - May apply based on your account tier
4. **Local Ollama** - Not available with local-only Ollama (no API key)