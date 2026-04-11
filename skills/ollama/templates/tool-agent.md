# Tool Agent Template

Agent with tool calling using ollama.

## Basic Tool Agent

```python
import ollama

# Define tools
def add(a: int, b: int) -> int:
  """Add two numbers.
  
  Args:
    a: First number
    b: Second number
  
  Returns:
    Sum of a and b
  """
  return a + b

def multiply(a: int, b: int) -> int:
  """Multiply two numbers.
  
  Args:
    a: First number
    b: Second number
  
  Returns:
    Product of a and b
  """
  return a * b

tools = [add, multiply]
available_tools = {t.__name__: t for t in tools}

class ToolAgent:
  """Agent with tool calling capabilities."""
  
  def __init__(self, model: str = 'qwen3', tools: list = None):
    self.model = model
    self.tools = tools or []
    self.available_tools = {t.__name__: t for t in self.tools}
    self.messages = []
  
  def system(self, content: str):
    """Set system message."""
    self.messages.append({'role': 'system', 'content': content})
  
  def chat(self, user_input: str) -> str:
    """Chat with tool calling loop."""
    self.messages.append({'role': 'user', 'content': user_input})
    
    while True:
      response = ollama.chat(
        model=self.model,
        messages=self.messages,
        tools=self.tools
      )
      
      # Append assistant response
      self.messages.append({
        'role': 'assistant',
        'content': response.message.content or '',
        'tool_calls': response.message.tool_calls or []
      })
      
      # No more tools to call
      if not response.message.tool_calls:
        return response.message.content
      
      # Execute tools
      for call in response.message.tool_calls:
        tool_name = call.function.name
        tool_args = dict(call.function.arguments)
        
        print(f"[Tool: {tool_name}({tool_args})]")
        
        try:
          result = self.available_tools[tool_name](**tool_args)
        except Exception as e:
          result = f"Error: {e}"
        
        self.messages.append({
          'role': 'tool',
          'tool_name': tool_name,
          'content': str(result)
        })

if __name__ == '__main__':
  agent = ToolAgent(model='qwen3', tools=tools)
  agent.system('You are a math assistant. Use tools to calculate.')
  
  print("Tool agent ready. Type /quit to exit.\n")
  
  while True:
    try:
      user_input = input('> ')
    except EOFError:
      break
    
    if user_input.lower() == '/quit':
      break
    
    response = agent.chat(user_input)
    print(response)
```

## Streaming Tool Agent

```python
import ollama

class StreamingToolAgent:
  """Agent with streaming and tool calling."""
  
  def __init__(self, model: str = 'qwen3', tools: list = None):
    self.model = model
    self.tools = tools or []
    self.available_tools = {t.__name__: t for t in self.tools}
    self.messages = []
  
  def chat(self, user_input: str) -> str:
    self.messages.append({'role': 'user', 'content': user_input})
    
    while True:
      stream = ollama.chat(
        model=self.model,
        messages=self.messages,
        tools=self.tools,
        stream=True
      )
      
      # Accumulate response
      content = ''
      tool_calls = []
      
      for chunk in stream:
        if chunk.message.content:
          content += chunk.message.content
          print(chunk.message.content, end='', flush=True)
        if chunk.message.tool_calls:
          tool_calls.extend(chunk.message.tool_calls)
      
      print()
      
      # Append accumulated response
      self.messages.append({
        'role': 'assistant',
        'content': content,
        'tool_calls': tool_calls
      })
      
      # No tools
      if not tool_calls:
        return content
      
      # Execute tools
      for call in tool_calls:
        tool_name = call.function.name
        tool_args = dict(call.function.arguments)
        
        print(f"[{tool_name}({tool_args})]", end=' ')
        
        try:
          result = self.available_tools[tool_name](**tool_args)
        except Exception as e:
          result = f"Error: {e}"
        
        print(f"→ {result}")
        
        self.messages.append({
          'role': 'tool',
          'tool_name': tool_name,
          'content': str(result)
        })
```

## File Reader Agent

```python
from pathlib import Path
import ollama

def read_file(name: str) -> str:
  """Read file content.
  
  Args:
    name: File name to read
  
  Returns:
    File content
  """
  try:
    return Path(name).read_text()
  except FileNotFoundError:
    return f"File '{name}' not found"

def list_files(directory: str = '.') -> str:
  """List files in directory.
  
  Args:
    directory: Directory path
  
  Returns:
    List of file names
  """
  path = Path(directory)
  files = [f.name for f in path.iterdir() if f.is_file()]
  return '\n'.join(files) or 'No files'

class FileReaderAgent:
  """Agent that can read files."""
  
  def __init__(self, model: str = 'qwen3'):
    self.model = model
    self.tools = [read_file, list_files]
    self.available_tools = {t.__name__: t for t in self.tools}
    self.messages = []
  
  def chat(self, user_input: str) -> str:
    self.messages.append({'role': 'user', 'content': user_input})
    
    while True:
      response = ollama.chat(
        model=self.model,
        messages=self.messages,
        tools=self.tools
      )
      
      self.messages.append({
        'role': 'assistant',
        'content': response.message.content or '',
        'tool_calls': response.message.tool_calls or []
      })
      
      if not response.message.tool_calls:
        return response.message.content
      
      for call in response.message.tool_calls:
        result = self.available_tools[call.function.name](
          **call.function.arguments
        )
        self.messages.append({
          'role': 'tool',
          'tool_name': call.function.name,
          'content': str(result)
        })
```