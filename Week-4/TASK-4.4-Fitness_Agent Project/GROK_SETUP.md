# Using FitBuddy with Grok Cloud (xAI)

This guide explains how to configure FitBuddy to use Grok Cloud (xAI) instead of OpenAI.

## Why Use Grok Cloud?

- **Cost-effective**: Often cheaper than OpenAI
- **OpenAI-compatible**: Easy to switch between providers
- **Grok models**: Access to xAI's Grok models (grok-beta, grok-2, etc.)

## Setup Steps

### 1. Get xAI API Key

1. Go to https://console.x.ai/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `xai-...`)

### 2. Configure .env File

Edit your `.env` file and add:

```
XAI_API_KEY=your_xai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: 
- `XAI_API_KEY`: Used for the LLM (Grok model)
- `OPENAI_API_KEY`: Still needed for embeddings (RAG functionality)

### 3. Run FitBuddy

The application is configured to use Grok by default:

```bash
python main.py
```

## Available Grok Models

- `grok-beta`: Latest Grok model (default)
- `grok-2`: Previous version
- `grok-vision-beta`: For vision tasks

## Switching Between Providers

### Use Grok (xAI):
```python
from agent.fitbuddy_agent import create_agent

agent = create_agent(model="grok-beta")
```

### Use OpenAI:
```python
from agent.fitbuddy_agent import create_agent

agent = create_agent(model="gpt-3.5-turbo")
```

### Custom Base URL:
```python
agent = create_agent(
    model="grok-beta",
    base_url="https://api.x.ai/v1"
)
```

## Model Comparison

| Model | Provider | Cost | Speed | Context |
|-------|----------|------|-------|---------|
| grok-beta | xAI | Lower | Fast | 128K |
| gpt-3.5-turbo | OpenAI | Higher | Fast | 16K |
| gpt-4 | OpenAI | Highest | Slower | 128K |

## Troubleshooting

### "API key not found"
- Make sure `XAI_API_KEY` is set in `.env`
- Check for typos in the key
- Ensure the `.env` file is in the project root

### "Embeddings error"
- Make sure `OPENAI_API_KEY` is also set (needed for RAG)
- Verify your OpenAI key has credit available

### "Model not found"
- Check that the model name is correct
- Try `grok-beta` as the default

## Cost Savings Example

If you run FitBuddy frequently, using Grok can save money:

**OpenAI gpt-3.5-turbo**: ~$0.50 per 1M tokens
**xAI grok-beta**: ~$0.10 per 1M tokens

That's a **80% cost reduction**!

## Notes

- Grok Cloud is OpenAI-compatible, so the code works seamlessly
- Embeddings still use OpenAI (ChromaDB requires OpenAI embeddings)
- You can switch between providers without changing code
- Both providers support the same LangChain interface

## Getting Help

- xAI Documentation: https://docs.x.ai/
- xAI Console: https://console.x.ai/
- OpenAI Documentation: https://platform.openai.com/docs
