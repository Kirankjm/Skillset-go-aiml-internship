# FitBuddy Quick Start Guide

Get started with FitBuddy in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Groq API key (recommended) OR OpenAI API key
  - Get Groq key at https://console.groq.com/
  - Get OpenAI key at https://platform.openai.com/api-keys

## Installation

### Option 1: Automated Setup (Recommended)

```bash
python setup.py
```

This will:
- Check Python version
- Install dependencies
- Create .env file
- Verify setup

### Option 2: Manual Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
```

3. **Edit .env file** and add your API key:

**For Groq (Recommended):**
```
GROQ_API_KEY=gsk-your-actual-api-key-here
```

**For OpenAI:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Note**: If using Groq, you still need OPENAI_API_KEY for embeddings (RAG functionality).

## Running FitBuddy

### Interactive Mode

```bash
python main.py
```

You'll see a welcome message with example queries. Try these:

```
What's my BMI if I weigh 70kg and am 175cm tall?
```

```
How many calories should I eat to lose weight? I'm 30 years old, male, 70kg, 175cm, moderately active.
```

```
What are some good cardio exercises for beginners?
```

### Run Examples

To see individual components in action:

```bash
python examples.py
```

This will demonstrate:
- BMI Calculator
- Calorie Calculator
- Meal Plan Calculator
- Knowledge Base Search
- Web Search
- Multi-step Task

## Common Issues

### "OpenAI API key not found"
- Make sure you've created a `.env` file
- Add your API key in the format: `OPENAI_API_KEY=sk-...`
- Don't include quotes around the key

### "Module not found" errors
- Make sure you've installed dependencies: `pip install -r requirements.txt`
- Try using a virtual environment

### Vector store errors
- Delete the `chroma_db` directory if it exists
- Restart the application to rebuild the vector store

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Customize the knowledge base by adding more documents to `knowledge_base/`
- Add new tools in `tools/fitness_tools.py`

## Tips for Best Results

1. **Be specific**: Provide details like weight, height, age, and activity level for personalized advice
2. **Ask follow-up questions**: The agent remembers context across the conversation
3. **Use web search**: For the latest information, ask the agent to search the web
4. **Combine tools**: Ask complex questions that require multiple calculations

## Example Session

```
You: What's my BMI if I weigh 75kg and am 180cm tall?

FitBuddy: [Calculates BMI] Your BMI is 23.1, which is in the normal weight range. 
This is a healthy weight for your height. Continue with balanced diet and regular exercise.

You: How many calories should I eat to maintain this weight? I'm moderately active.

FitBuddy: [Calculates calories] Based on your details, your BMR is 1676 calories and 
your TDEE is 2598 calories. To maintain your current weight, aim for approximately 2600 calories daily.

You: What should I eat before a workout?

FitBuddy: [Searches knowledge base] Eat a meal 1-2 hours before exercise with carbohydrates 
for energy and moderate protein. Good options include: banana with peanut butter, Greek yogurt 
with fruit, or whole grain toast with eggs.
```

## Support

For issues or questions:
- Check the [README.md](README.md) for detailed documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Run `python examples.py` to verify each component works

Enjoy using FitBuddy! 💪
