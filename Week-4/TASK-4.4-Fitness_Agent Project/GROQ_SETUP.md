# Using FitBuddy with Groq

This guide explains how to configure FitBuddy to use Groq instead of OpenAI or xAI.

## Why Use Groq?

- **Ultra-fast inference**: Groq's LPU (Language Processing Unit) is incredibly fast
- **Cost-effective**: Often free or very low cost
- **OpenAI-compatible**: Easy to switch between providers
- **Great models**: Access to Llama, Mixtral, Gemma, and more

## Setup Steps

### 1. Get Groq API Key

1. Go to https://console.groq.com/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk-...`)

### 2. Configure .env File

Edit your `.env` file and add:

```
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: 
- `GROQ_API_KEY`: Used for the LLM (Groq models)
- `OPENAI_API_KEY`: Still needed for embeddings (RAG functionality)

### 3. Run FitBuddy

The application is configured to use Groq by default:

```bash
python main.py
```

## Available Groq Models

- `llama3-70b-8192`: Best all-around model (default)
- `llama3-8b-8192`: Very fast for simple tasks
- `mixtral-8x7b-32768`: Excellent for complex reasoning
- `gemma-7b-it`: Lightweight, fast model

**Note**: Check https://console.groq.com/docs for the latest available models as Groq updates their offerings frequently.

## Switching Between Providers

### Use Groq (default):
```python
from agent.fitbuddy_agent import create_agent

agent = create_agent(model="llama3-70b-8192")
```

### Use OpenAI:
```python
from agent.fitbuddy_agent import create_agent

agent = create_agent(model="gpt-3.5-turbo")
```

### Custom Base URL:
```python
agent = create_agent(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1"
)
```

## Model Comparison

| Model | Provider | Cost | Speed | Context |
|-------|----------|------|-------|---------|
| llama3-70b-8192 | Groq | Free/Low | Ultra-fast | 8K |
| mixtral-8x7b-32768 | Groq | Free/Low | Ultra-fast | 32K |
| gpt-3.5-turbo | OpenAI | Higher | Fast | 16K |
| gpt-4 | OpenAI | Highest | Slower | 128K |

## Troubleshooting

### "API key not found"
- Make sure `GROQ_API_KEY` is set in `.env`
- Check for typos in the key
- Ensure the `.env` file is in the project root

### "Embeddings error"
- Make sure `OPENAI_API_KEY` is also set (needed for RAG)
- Verify your OpenAI key has credit available

### "Model not found" or "Model decommissioned"
- Check that the model name is correct
- Try `llama3-70b-8192` as the default
- Check Groq console for available models at https://console.groq.com/
- Check deprecation notices at https://console.groq.com/docs/deprecations

## Cost Savings Example

If you run FitBuddy frequently, using Groq can save money:

**OpenAI gpt-3.5-turbo**: ~$0.50 per 1M tokens
**Groq llama-3.3-70b**: ~$0.00 per 1M tokens (free tier)

That's **100% cost reduction** on the free tier!

## Notes

- Groq is OpenAI-compatible, so the code works seamlessly
- Embeddings still use OpenAI (ChromaDB requires OpenAI embeddings)
- You can switch between providers without changing code
- Both providers support the same LangChain interface
- Groq's speed is significantly faster than traditional GPU-based inference

## Getting Help

- Groq Documentation: https://console.groq.com/docs
- Groq Console: https://console.groq.com/
- OpenAI Documentation: https://platform.openai.com/docs
