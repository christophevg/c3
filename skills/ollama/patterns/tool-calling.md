# Tool Calling Patterns

Ollama tool calling patterns for function calling.

## Tool Definition

### Python Function (Auto-Parsed)

```python
def get_weather(city: str, unit: str = 'celsius') -> str:
  """Get the current weather for a city.
  
  Args:
    city: The name of the city
    unit: Temperature unit (celsius or fahrenheit)
  
  Returns:
    The current weather description
  """
  # Implementation
  return f"Weather in {city}: 22°{unit[0].upper()}"
```

The SDK automatically parses:
- Function name from `def`
- Description from docstring
- Parameters from type hints
- Parameter descriptions from Args section

### Explicit Tool Definition

```python
tools = [{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather for a city",
    "parameters": {
      "type": "object",
      "required": ["city"],
      "properties": {
        "city": {
          "type": "string",
          "description": "The name of the city"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature unit"
        }
      }
    }
  }
}]
```

## Basic Tool Calling

```python
import ollama

def add(a: int, b: int) -> int:
  """Add two numbers."""
  return a + b

response = ollama.chat(
  model='qwen3',
  messages=[{'role': 'user', 'content': 'What is 17 + 25?'}],
  tools=[add]
)

if response.message.tool_calls:
  for call in response.message.tool_calls:
    print(f"{call.function.name}({call.function.arguments})")
```

## Tool Execution Pattern

```python
import ollama

# Define tools
def add(a: int, b: int) -> int:
  """Add two numbers."""
  return a + b

def multiply(a: int, b: int) -> int:
  """Multiply two numbers."""
  return a * b

tools = [add, multiply]
available_tools = {t.__name__: t for t in tools}

# Execute tools
def execute_tools(tool_calls: list) -> list:
  results = []
  for call in tool_calls:
    tool_name = call.function.name
    tool_args = dict(call.function.arguments)
    
    try:
      result = available_tools[tool_name](**tool_args)
    except Exception as e:
      result = f"Error: {e}"
    
    results.append({
      'tool_name': tool_name,
      'result': result
    })
  
  return results
```

## Multi-Turn Tool Calling

```python
messages = [{'role': 'user', 'content': 'Calculate (17 + 25) × 3'}]

# First call - may request addition
response = ollama.chat(model='qwen3', messages=messages, tools=tools)

# Execute tools and append results
if response.message.tool_calls:
  messages.append({
    'role': 'assistant',
    'tool_calls': response.message.tool_calls
  })
  
  for call in response.message.tool_calls:
    result = available_tools[call.function.name](**call.function.arguments)
    messages.append({
      'role': 'tool',
      'tool_name': call.function.name,
      'content': str(result)
    })
  
  # Second call - may request multiplication
  response = ollama.chat(model='qwen3', messages=messages, tools=tools)

print(response.message.content)
```

## Streaming Tool Calls

```python
import ollama

messages = [{'role': 'user', 'content': 'Add 10 and 20'}]

stream = ollama.chat(
  model='qwen3',
  messages=messages,
  tools=[add],
  stream=True
)

tool_calls = []
content = ''

for chunk in stream:
  if chunk.message.tool_calls:
    tool_calls.extend(chunk.message.tool_calls)
  if chunk.message.content:
    content += chunk.message.content

# Execute accumulated tool calls
for call in tool_calls:
  result = available_tools[call.function.name](**call.function.arguments)
  messages.append({
    'role': 'tool',
    'tool_name': call.function.name,
    'content': str(result)
  })

# Continue conversation
response = ollama.chat(model='qwen3', messages=messages)
```

## Tool with Complex Types

```python
from typing import List, Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
  title: str
  url: str
  snippet: str

def search_web(query: str, max_results: int = 5) -> List[dict]:
  """Search the web for information.
  
  Args:
    query: The search query
    max_results: Maximum number of results
  
  Returns:
    List of search results with title, url, and snippet
  """
  # Implementation
  return [
    {"title": "Result 1", "url": "https://...", "snippet": "..."},
    {"title": "Result 2", "url": "https://...", "snippet": "..."},
  ]
```

## Tool Error Handling

```python
def safe_tool_execution(call, available_tools: dict) -> str:
  """Execute a tool call safely."""
  tool_name = call.function.name
  
  if tool_name not in available_tools:
    return f"Unknown tool: {tool_name}"
  
  try:
    result = available_tools[tool_name](**call.function.arguments)
    return str(result)
  except TypeError as e:
    return f"Invalid arguments for {tool_name}: {e}"
  except Exception as e:
    return f"Error executing {tool_name}: {e}"

# Usage
for call in tool_calls:
  result = safe_tool_execution(call, available_tools)
  messages.append({
    'role': 'tool',
    'tool_name': call.function.name,
    'content': result
  })
```

## Read File Tool Example

```python
from pathlib import Path

def read_file(name: str) -> str:
  """Read the content of a file.
  
  Args:
    name: The name of the file to read
  
  Returns:
    The content of the file
  """
  try:
    return Path(name).read_text()
  except FileNotFoundError:
    return f"Error: File '{name}' not found"
  except Exception as e:
    return f"Error reading file: {e}"
```

## Key Points

1. **Docstrings matter** - SDK parses them for tool descriptions
2. **Type hints** - Define parameter types
3. **Accumulate tool_calls** when streaming
4. **Return strings** - Tool results must be string-serializable
5. **Handle errors** - Tools can fail, catch exceptions