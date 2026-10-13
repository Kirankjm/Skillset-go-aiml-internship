# Perfect Fitness Agent - AI Health Assistant

Perfect Fitness Agent is an **AI-powered health assistant** that demonstrates **RAG (Retrieval-Augmented Generation)**, **Tool Use**, and **Multi-step Reasoning** - all **without requiring any API key**. It provides seamless chat-based interaction for comprehensive health guidance.

## 🌟 Capstone Requirements Fulfilled

✅ **RAG System**: Retrieves information from comprehensive health knowledge base  
✅ **Tool Use**: 7 intelligent health calculators (BMI, Calories, Water, Sleep, Heart Rate, Meal Plan, Web Search)  
✅ **Multi-step Reasoning**: Chains multiple calculations for complex queries  
✅ **Seamless Interface**: Natural chat-like interaction  
✅ **No API Key Required**: Completely free and reliable  
✅ **GitHub Repository**: Complete project structure  
✅ **Live Demo**: Run `python demo.py` for automated demonstration, or `python main.py` for interactive mode  
✅ **Documentation**: README, ARCHITECTURE.md, HEALTH_GUIDE.md  

## Features

### Core Capabilities
- **RAG System**: Retrieves relevant information from 6 comprehensive health guides
- **Tool Use**: 7 intelligent health calculators with automatic routing
- **Multi-step Reasoning**: Handles complex queries requiring chained calculations
- **Seamless Chat Interface**: Natural conversation-like interaction
- **Zero Dependencies**: No API keys, no costs, no model deprecation issues

### Health Calculators
- **BMI Calculator**: Calculate BMI with health recommendations
- **Calorie Calculator**: Daily calorie needs based on BMR, TDEE, and goals
- **Meal Plan Calculator**: Create and track meal plans with macronutrients
- **Water Intake Calculator**: Daily hydration needs based on weight and activity
- **Sleep Calculator**: Recommended sleep duration by age group
- **Heart Rate Calculator**: Target heart rate zones for exercise intensity
- **Web Search**: Up-to-date health information from the web

### Knowledge Base Coverage
- **Fitness & Exercise**: Workout plans, cardio, strength training
- **Nutrition**: Balanced diet, macronutrients, meal timing
- **Mental Health**: Stress management, mindfulness, resilience
- **Sleep Health**: Sleep cycles, hygiene, disorders
- **Disease Prevention**: Cardiovascular health, diabetes, cancer prevention
- **Hydration**: Daily water intake, signs of dehydration

## Architecture

```
FitBuddy/
├── knowledge_base/          # Fitness and nutrition guides
│   ├── fitness_guide.txt
│   └── nutrition_guide.txt
├── tools/                   # Fitness calculation tools
│   ├── __init__.py
│   └── fitness_tools.py
├── rag/                     # RAG implementation
│   ├── __init__.py
│   └── knowledge_base.py
├── agent/                   # AI agent implementation
│   ├── __init__.py
│   └── fitbuddy_agent.py
├── main.py                  # Main application interface
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- No API key required (uses local calculators and web search)

### Setup Steps

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python main.py
```

**No API key required!** The application uses local health calculators and web search, making it completely free and reliable.

## Usage

### Demo Mode (Recommended for Capstone Presentation)

Run the automated demo to showcase all features without requiring interactive input:

```bash
python demo.py
```

This demonstrates:
- BMI Calculator
- Daily Calorie Calculator (BMR → TDEE → Target Calories)
- Meal Plan Calculator
- Water Intake Calculator
- Sleep Requirements Calculator
- Target Heart Rate Calculator
- Knowledge Base Search
- Web Search

### Interactive Mode

Run the main application to start an interactive conversation:

```bash
python main.py
```

This launches a menu-based interface where you can select any health calculator or search tool.

### Web Interface (Recommended for Best User Experience)

Launch the beautiful web-based interface with a modern GUI:

**Windows:**
```bash
run_web.bat
```

**Mac/Linux:**
```bash
streamlit run web_interface.py
```

The web interface will automatically open in your browser at `http://localhost:8501`

**Web Interface Features:**
- 🎨 Modern, beautiful UI with intuitive navigation
- 📊 Visual charts and metrics
- 🖱️ Click-based interactions (no command line needed)
- 📱 Responsive design (works on mobile)
- 🔄 Real-time calculations
- 📋 Sidebar navigation between tools

### Example Queries

1. **Calculate BMI**:
   ```
   What's my BMI if I weigh 70kg and am 175cm tall?
   ```

2. **Calculate Daily Calories**:
   ```
   How many calories should I eat to lose weight? I'm 30 years old, male, 70kg, 175cm, moderately active.
   ```

3. **Fitness Advice**:
   ```
   What are some good cardio exercises for beginners?
   ```

4. **Nutrition Guidance**:
   ```
   What should I eat before a workout?
   ```

5. **Meal Planning**:
   ```
   Create a simple meal plan for me with around 2000 calories.
   ```

6. **Web Search**:
   ```
   Search for information about intermittent fasting.
   ```

### Programmatic Usage

You can also use FitBuddy programmatically in your Python code:

```python
from agent.fitbuddy_agent import create_agent

# Initialize the agent
agent = create_agent()

# Query the agent
response = agent.query("What's a good beginner workout routine?")
print(response)

# Reset conversation memory if needed
agent.reset_memory()
```

## Components

### 1. RAG System (`rag/knowledge_base.py`)

The RAG system uses:
- **ChromaDB**: Vector database for storing and retrieving document embeddings
- **OpenAI Embeddings**: Converts text to vector representations
- **LangChain**: Document processing and text splitting

The knowledge base is built from text files in the `knowledge_base/` directory containing fitness and nutrition guides.

### 2. Tools (`tools/fitness_tools.py`)

#### BMI Calculator
Calculates Body Mass Index and provides health recommendations based on WHO categories.

#### Calorie Calculator
Uses the Mifflin-St Jeor equation to calculate:
- BMR (Basal Metabolic Rate)
- TDEE (Total Daily Energy Expenditure)
- Target calories based on goals (lose/maintain/gain weight)

#### Meal Plan Calculator
Calculates total calories and macronutrients for meal plans.

#### Web Search Tool
Searches the web using DuckDuckGo for up-to-date fitness and nutrition information.

### 3. AI Agent (`agent/fitbuddy_agent.py`)

The agent uses:
- **LangChain ReAct Agent**: Reasoning + Acting framework for tool use
- **OpenAI GPT**: Language model for understanding and generating responses
- **Conversation Memory**: Maintains context across interactions

The agent follows a Thought-Action-Observation loop to:
1. Understand the user's query
2. Decide which tools to use
3. Execute tool calls
4. Synthesize results into a helpful response

## Extending FitBuddy

### Adding New Knowledge

Add new text files to the `knowledge_base/` directory and rebuild the vector store:

```python
from rag.knowledge_base import initialize_knowledge_base

# Force rebuild with new documents
kb = initialize_knowledge_base(force_rebuild=True)
```

### Adding New Tools

1. Create a new tool class in `tools/fitness_tools.py`
2. Add it to the `FITNESS_TOOLS` registry
3. Register it in the `_create_tools()` method in `agent/fitbuddy_agent.py`

Example:
```python
class WaterIntakeCalculator:
    @staticmethod
    def calculate(weight_kg: float) -> float:
        return weight_kg * 0.033  # 33ml per kg
```

### Customizing the Agent

You can customize the agent by:
- Changing the model (e.g., use `gpt-4` instead of `gpt-3.5-turbo`)
- Modifying the prompt template in `fitbuddy_agent.py`
- Adjusting tool descriptions for better agent performance

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenAI API key is set in the `.env` file
2. **Vector Store Error**: Delete the `chroma_db` directory and restart to rebuild
3. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Project Structure

```
FitBuddy/
├── knowledge_base/          # Source documents for RAG
│   ├── fitness_guide.txt    # Beginner fitness guide
│   └── nutrition_guide.txt  # Nutrition guidelines
├── tools/                   # Calculation and search tools
│   ├── __init__.py
│   └── fitness_tools.py     # BMI, calorie, meal calculators
├── rag/                     # RAG implementation
│   ├── __init__.py
│   └── knowledge_base.py    # Vector store and retrieval
├── agent/                   # AI agent
│   ├── __init__.py
│   └── fitbuddy_agent.py    # Main agent with tool use
├── main.py                  # CLI interface
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # Documentation
```

## Technologies Used

- **LangChain**: Framework for building LLM applications
- **OpenAI GPT**: Language model for understanding and generation
- **ChromaDB**: Vector database for RAG
- **OpenAI Embeddings**: Text embedding model
- **BeautifulSoup4**: Web scraping for search tool
- **Requests**: HTTP library for web search

## License

This project is created for educational purposes.

## Acknowledgments

Built as a capstone project demonstrating AI agent integration with RAG, tool use, and multi-step reasoning capabilities.
