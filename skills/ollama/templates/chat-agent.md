# Chat Agent Template

Basic chat agent using ollama.

## Simple Chat Agent

```python
import ollama

def chat(prompt: str, model: str = 'gemma3') -> str:
  """Simple chat with ollama."""
  response = ollama.chat(
    model=model,
    messages=[{'role': 'user', 'content': prompt}]
  )
  return response.message.content

if __name__ == '__main__':
  while True:
    try:
      user_input = input('> ')
    except EOFError:
      break
    
    if user_input.lower() == '/quit':
      break
    
    response = chat(user_input)
    print(response)
```

## Chat Agent with History

```python
import ollama

class ChatAgent:
  """Chat agent with conversation history."""
  
  def __init__(self, model: str = 'gemma3', system: str = None):
    self.model = model
    self.messages = []
    
    if system:
      self.messages.append({'role': 'system', 'content': system})
  
  def chat(self, user_input: str) -> str:
    """Send message and get response."""
    self.messages.append({'role': 'user', 'content': user_input})
    
    response = ollama.chat(
      model=self.model,
      messages=self.messages
    )
    
    self.messages.append({
      'role': 'assistant',
      'content': response.message.content
    })
    
    return response.message.content
  
  def clear(self):
    """Clear conversation history (keep system message)."""
    self.messages = [m for m in self.messages if m['role'] == 'system']

if __name__ == '__main__':
  agent = ChatAgent(
    model='gemma3',
    system='You are a helpful assistant.'
  )
  
  print("Chat agent ready. Type /quit to exit.\n")
  
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

## Streaming Chat Agent

```python
import ollama

class StreamingChatAgent:
  """Chat agent with streaming output."""
  
  def __init__(self, model: str = 'gemma3', system: str = None):
    self.model = model
    self.messages = []
    
    if system:
      self.messages.append({'role': 'system', 'content': system})
  
  def chat(self, user_input: str) -> str:
    """Stream response and return full content."""
    self.messages.append({'role': 'user', 'content': user_input})
    
    stream = ollama.chat(
      model=self.model,
      messages=self.messages,
      stream=True
    )
    
    content = ''
    for chunk in stream:
      if chunk.message.content:
        content += chunk.message.content
        print(chunk.message.content, end='', flush=True)
    
    print()  # Newline
    
    self.messages.append({'role': 'assistant', 'content': content})
    return content

if __name__ == '__main__':
  agent = StreamingChatAgent(model='gemma3')
  
  print("Streaming chat ready. Type /quit to exit.\n")
  
  while True:
    try:
      user_input = input('> ')
    except EOFError:
      break
    
    if user_input.lower() == '/quit':
      break
    
    agent.chat(user_input)
```

## Cloud API Chat Agent

```python
import os
from ollama import Client

class CloudChatAgent:
  """Chat agent using ollama.com cloud API."""
  
  def __init__(self, model: str = 'gpt-oss:120b'):
    self.client = Client(
      host='https://ollama.com',
      headers={'Authorization': 'Bearer ' + os.environ['OLLAMA_API_KEY']}
    )
    self.model = model
    self.messages = []
  
  def chat(self, user_input: str) -> str:
    self.messages.append({'role': 'user', 'content': user_input})
    
    response = self.client.chat(
      model=self.model,
      messages=self.messages
    )
    
    self.messages.append({
      'role': 'assistant',
      'content': response.message.content
    })
    
    return response.message.content
```