# Image Generation Patterns

Image generation patterns for Ollama (experimental).

## Prerequisites

- Currently only available on **macOS**
- Requires image generation model (e.g., `x/z-image-turbo`)

## Basic Image Generation

```python
import base64
import ollama

# Generate image
response = ollama.generate(
  model='x/z-image-turbo',
  prompt='a sunset over mountains'
)

# Save the image
with open('output.png', 'wb') as f:
  f.write(base64.b64decode(response.image))

print('Image saved to output.png')
```

## Streaming Progress

```python
import base64
import ollama

for chunk in ollama.generate(
  model='x/z-image-turbo',
  prompt='a futuristic cityscape',
  stream=True
):
  if chunk.image:
    # Final image
    with open('city.png', 'wb') as f:
      f.write(base64.b64decode(chunk.image))
    print('\nImage saved to city.png')
  elif chunk.total:
    # Progress indicator
    percent = (chunk.completed or 0) / chunk.total * 100
    print(f'\rProgress: {percent:.0f}%', end='', flush=True)
```

## Custom Dimensions

```python
import base64
import ollama

response = ollama.generate(
  model='x/z-image-turbo',
  prompt='a portrait of a cat',
  width=512,
  height=768
)

with open('portrait.png', 'wb') as f:
  f.write(base64.b64decode(response.image))
```

## Diffusion Steps

Higher steps = more detail but slower:

```python
import base64
import ollama

response = ollama.generate(
  model='x/z-image-turbo',
  prompt='a detailed landscape painting',
  steps=50,  # More steps for finer detail
  width=1024,
  height=1024
)

with open('landscape.png', 'wb') as f:
  f.write(base64.b64decode(response.image))
```

## Batch Generation

```python
import base64
from pathlib import Path
import ollama

prompts = [
  'a red sports car',
  'a blue sedan',
  'a green truck'
]

output_dir = Path('generated_images')
output_dir.mkdir(exist_ok=True)

for i, prompt in enumerate(prompts):
  print(f'Generating image {i+1}/{len(prompts)}: {prompt}')
  
  response = ollama.generate(
    model='x/z-image-turbo',
    prompt=prompt,
    stream=False
  )
  
  filename = output_dir / f'image_{i+1}.png'
  with open(filename, 'wb') as f:
    f.write(base64.b64decode(response.image))
  
  print(f'  Saved to {filename}')
```

## Error Handling

```python
import base64
import ollama

try:
  response = ollama.generate(
    model='x/z-image-turbo',
    prompt='a beautiful garden',
    stream=False
  )
  
  if response.image:
    with open('garden.png', 'wb') as f:
      f.write(base64.b64decode(response.image))
  else:
    print('No image generated')
    
except ollama.ResponseError as e:
  print(f'Error: {e.error}')
except Exception as e:
  print(f'Unexpected error: {e}')
```

## Integration with Chat

Use generated images in chat:

```python
import base64
import ollama

# Generate an image
gen_response = ollama.generate(
  model='x/z-image-turbo',
  prompt='a diagram showing system architecture',
  stream=False
)

# Save and analyze
with open('diagram.png', 'wb') as f:
  f.write(base64.b64decode(gen_response.image))

# Use vision model to describe
chat_response = ollama.chat(
  model='gemma3',
  messages=[{
    'role': 'user',
    'content': 'What does this diagram show?',
    'images': ['diagram.png']
  }]
)

print(chat_response.message.content)
```

## Notes

1. **Experimental feature** - API may change
2. **macOS only** - Currently limited platform support
3. **Model dependent** - Not all models support image generation
4. **Memory intensive** - Large images require significant VRAM