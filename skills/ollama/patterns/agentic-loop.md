# Agentic Loop Pattern

Agent loop with tool calling and streaming.

## Basic Agent Loop

```python
import ollama

def run_agent(prompt: str, tools: list) -> str:
  messages = [{'role': 'user', 'content': prompt}]
  available_tools = {t.__name__: t for t in tools}
  
  while True:
    response = ollama.chat(
      model='qwen3',
      messages=messages,
      tools=tools
    )
    
    # Append assistant response
    messages.append({
      'role': 'assistant',
      'content': response.message.content or '',
      'tool_calls': response.message.tool_calls or []
    })
    
    # No more tools to call
    if not response.message.tool_calls:
      return response.message.content
    
    # Execute tools and append results
    for call in response.message.tool_calls:
      tool_name = call.function.name
      tool_args = call.function.arguments
      
      result = available_tools[tool_name](**tool_args)
      
      messages.append({
        'role': 'tool',
        'tool_name': tool_name,
        'content': str(result)
      })
```

## Streaming Agent Loop

```python
import ollama

def run_streaming_agent(prompt: str, tools: list) -> str:
  messages = [{'role': 'user', 'content': prompt}]
  available_tools = {t.__name__: t for t in tools}
  
  while True:
    stream = ollama.chat(
      model='qwen3',
      messages=messages,
      tools=tools,
      stream=True,
      think=True
    )
    
    # Accumulate partial fields
    content = ''
    thinking = ''
    tool_calls = []
    
    in_thinking = False
    
    for chunk in stream:
      # Handle thinking
      if chunk.message.thinking:
        if not in_thinking:
          in_thinking = True
          print('\n[Thinking]\n', flush=True)
        thinking += chunk.message.thinking
        print(chunk.message.thinking, end='', flush=True)
      
      # Handle content
      if chunk.message.content:
        if in_thinking:
          in_thinking = False
          print('\n\n[Response]\n', flush=True)
        content += chunk.message.content
        print(chunk.message.content, end='', flush=True)
      
      # Handle tool calls
      if chunk.message.tool_calls:
        tool_calls.extend(chunk.message.tool_calls)
    
    print()  # Newline
    
    # Append accumulated response
    messages.append({
      'role': 'assistant',
      'thinking': thinking,
      'content': content,
      'tool_calls': tool_calls
    })
    
    # No more tools
    if not tool_calls:
      return content
    
    # Execute tools
    print('\n[Tool Calls]\n')
    for call in tool_calls:
      tool_name = call.function.name
      tool_args = dict(call.function.arguments)
      
      print(f'  {tool_name}({tool_args})')
      result = available_tools[tool_name](**tool_args)
      print(f'  → {result}')
      
      messages.append({
        'role': 'tool',
        'tool_name': tool_name,
        'content': str(result)
      })
```

## Agent with Conversation History

```python
class Agent:
  def __init__(self, model: str, tools: list = None):
    self.model = model
    self.tools = tools or []
    self.available_tools = {t.__name__: t for t in self.tools}
    self.messages = []
  
  def system(self, content: str):
    self.messages.append({'role': 'system', 'content': content})
  
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
  
  def history(self):
    return self.messages
```

## Error Handling in Agent Loop

```python
import ollama

def safe_agent_loop(model: str, messages: list, tools: list, max_iterations: int = 10):
  available_tools = {t.__name__: t for t in tools}
  
  for iteration in range(max_iterations):
    try:
      response = ollama.chat(model=model, messages=messages, tools=tools)
    except ollama.ResponseError as e:
      if e.status_code == 404:
        ollama.pull(model)
        continue
      raise
    
    messages.append({
      'role': 'assistant',
      'content': response.message.content or '',
      'tool_calls': response.message.tool_calls or []
    })
    
    if not response.message.tool_calls:
      return response.message.content, messages
    
    for call in response.message.tool_calls:
      try:
        result = available_tools[call.function.name](**call.function.arguments)
      except Exception as e:
        result = f"Error executing {call.function.name}: {e}"
      
      messages.append({
        'role': 'tool',
        'tool_name': call.function.name,
        'content': str(result)
      })
  
  return "Max iterations reached", messages
```

## Key Points

1. **Always accumulate partial fields** when streaming
2. **Loop until no tool_calls** in response
3. **Execute tools and append results** to messages
4. **Handle errors** for missing models and tool execution
5. **Set max iterations** to prevent infinite loops