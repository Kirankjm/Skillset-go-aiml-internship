# FitBuddy Architecture Documentation

## Overview

FitBuddy is an AI-powered fitness assistant that combines three key AI capabilities:
1. **RAG (Retrieval-Augmented Generation)**: Retrieves relevant information from a knowledge base
2. **Tool Use**: Executes specific calculations and searches
3. **Multi-step Reasoning**: Chains multiple tool calls to solve complex tasks

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                       │
│                          (main.py)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FitBuddy Agent                            │
│              (agent/fitbuddy_agent.py)                       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LangChain ReAct Agent                    │  │
│  │  • Thought-Action-Observation Loop                   │  │
│  │  • Tool Selection & Execution                        │  │
│  │  • Response Synthesis                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│         ┌───────────────┼───────────────┐                 │
│         ▼               ▼               ▼                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │
│  │   RAG System │ │    Tools     │ │  Conversation│      │
│  │              │ │              │ │    Memory    │      │
│  └──────────────┘ └──────────────┘ └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │               │
         ▼               ▼
┌──────────────────┐ ┌──────────────────┐
│  Knowledge Base  │ │  Fitness Tools   │
│  (ChromaDB)      │ │                  │
│                  │ │ • BMI Calculator │
│ • Fitness Guide  │ │ • Calorie Calc   │
│ • Nutrition Guide│ │ • Meal Plan Calc │
│                  │ │ • Web Search     │
└──────────────────┘ └──────────────────┘
```

## Component Details

### 1. RAG System (rag/knowledge_base.py)

**Purpose**: Store and retrieve fitness/nutrition information from documents.

**Technology Stack**:
- **ChromaDB**: Vector database for storing document embeddings
- **OpenAI Embeddings**: Converts text to vector representations
- **LangChain**: Document processing and chunking

**Workflow**:
1. Load text documents from `knowledge_base/` directory
2. Split documents into chunks (500 characters with 50-character overlap)
3. Convert chunks to embeddings using OpenAI's embedding model
4. Store in ChromaDB vector database
5. At query time, perform similarity search to find relevant chunks

**Key Classes**:
- `FitnessKnowledgeBase`: Manages the vector store and search operations
- `initialize_knowledge_base()`: Factory function to create/load the knowledge base

**Example Usage**:
```python
from rag.knowledge_base import initialize_knowledge_base

# Initialize (loads existing or creates new)
kb = initialize_knowledge_base()

# Search for information
results = kb.search("cardio exercises", k=3)
for result in results:
    print(result['content'])
```

### 2. Tools (tools/fitness_tools.py)

**Purpose**: Execute specific fitness-related calculations and searches.

**Available Tools**:

#### BMI Calculator
- **Input**: weight (kg), height (cm)
- **Output**: BMI value, category (Underweight/Normal/Overweight/Obese), health recommendation
- **Formula**: BMI = weight (kg) / height (m)²

#### Calorie Calculator
- **Input**: weight, height, age, gender, activity level, goal
- **Output**: BMR, TDEE, target daily calories
- **Formulas**:
  - BMR (Mifflin-St Jeor): 
    - Male: 10×weight + 6.25×height - 5×age + 5
    - Female: 10×weight + 6.25×height - 5×age - 161
  - TDEE: BMR × activity multiplier (1.2-1.9)
  - Target: TDEE ± 500 calories based on goal

#### Meal Plan Calculator
- **Input**: List of meals with calories and macronutrients
- **Output**: Total calories, protein, carbs, fat
- **Use Case**: Track daily nutritional intake

#### Web Search Tool
- **Input**: Search query
- **Output**: List of web results with title, URL, snippet
- **Implementation**: DuckDuckGo HTML search (no API key required)

**Example Usage**:
```python
from tools.fitness_tools import BMICalculator, CalorieCalculator

# Calculate BMI
result = BMICalculator.calculate(70, 175)
print(f"BMI: {result['bmi']}")

# Calculate calories
bmr = CalorieCalculator.calculate_bmr(70, 175, 30, 'male')
tdee = CalorieCalculator.calculate_tdee(bmr, 'moderate')
```

### 3. AI Agent (agent/fitbuddy_agent.py)

**Purpose**: Orchestrate RAG and tools to answer user queries with multi-step reasoning.

**Technology Stack**:
- **LangChain ReAct Agent**: Framework for reasoning + acting
- **OpenAI GPT**: Language model for understanding and generation
- **ConversationBufferMemory**: Maintains conversation context

**ReAct Pattern**:
The agent follows a Thought-Action-Observation loop:

```
Thought: I need to calculate the user's BMI
Action: BMI Calculator
Action Input: 70,175
Observation: {"bmi": 22.9, "category": "Normal weight", ...}
Thought: Now I can provide the answer
Final Answer: Your BMI is 22.9, which is in the normal weight range...
```

**Tool Registration**:
Each tool is registered with:
- **Name**: Unique identifier
- **Function**: Python function to execute
- **Description**: Natural language description for the LLM to understand when to use it

**Memory Management**:
- Stores conversation history
- Maintains context across multiple queries
- Can be reset to start fresh

**Example Usage**:
```python
from agent.fitbuddy_agent import create_agent

agent = create_agent()
response = agent.query("What's my BMI if I weigh 70kg and am 175cm?")
print(response)
```

### 4. Main Interface (main.py)

**Purpose**: Provide a user-friendly command-line interface.

**Features**:
- Welcome message with usage instructions
- Example queries for users to try
- Interactive conversation loop
- Error handling and graceful exit

**User Flow**:
1. Display welcome message and examples
2. Initialize FitBuddy agent
3. Enter conversation loop:
   - Get user input
   - Process through agent
   - Display response
   - Repeat until user quits

## Data Flow

### Example: "How many calories should I eat to lose weight?"

```
User Query
    ↓
FitBuddy Agent receives query
    ↓
LangChain LLM analyzes query
    ↓
Thought: User wants calorie calculation for weight loss
    ↓
Action: Calorie Calculator
    ↓
Action Input: Extracts/asks for weight, height, age, gender, activity level
    ↓
Observation: Receives calculated target calories
    ↓
Thought: Also provide context from knowledge base
    ↓
Action: Fitness Knowledge Base
    ↓
Action Input: "weight loss nutrition tips"
    ↓
Observation: Receives relevant nutrition guidelines
    ↓
Thought: Now I have all information needed
    ↓
Final Answer: Synthesizes calculator results + knowledge base info
    ↓
Response to User
```

## Multi-step Reasoning Example

**Task**: "Create a meal plan for me with around 2000 calories"

**Agent Execution**:
1. **Thought**: Need to understand user's calorie needs first
2. **Action**: Ask for user's physical details (weight, height, age, gender, activity level)
3. **Observation**: User provides details
4. **Thought**: Calculate their actual calorie needs
5. **Action**: Calorie Calculator
6. **Observation**: TDEE = 2200 calories
7. **Thought**: 2000 calories is reasonable for weight loss
8. **Action**: Fitness Knowledge Base (search for "meal planning")
9. **Observation**: Gets meal timing and portion guidelines
10. **Thought**: Create a balanced meal plan
11. **Action**: Meal Plan Calculator (with calculated meals)
12. **Observation**: Total = 2000 calories, balanced macros
13. **Thought**: Verify the plan
14. **Final Answer**: Present the complete meal plan with explanation

## Extending the System

### Adding New Knowledge

1. Add text files to `knowledge_base/` directory
2. Rebuild vector store:
```python
kb = initialize_knowledge_base(force_rebuild=True)
```

### Adding New Tools

1. Create tool class in `tools/fitness_tools.py`:
```python
class NewTool:
    @staticmethod
    def calculate(param1, param2):
        # Implementation
        return result
```

2. Register in `FITNESS_TOOLS` dictionary

3. Add tool in `agent/fitbuddy_agent.py`:
```python
Tool(
    name="New Tool",
    func=new_tool_func,
    description="Description for LLM"
)
```

### Customizing the Agent

- **Change Model**: Use GPT-4 for better reasoning
- **Modify Prompt**: Edit the prompt template in `fitbuddy_agent.py`
- **Adjust Memory**: Change memory type or capacity
- **Add Constraints**: Limit tool usage or add safety checks

## Performance Considerations

### Vector Database
- Chunk size: 500 characters (balance between context and specificity)
- Overlap: 50 characters (maintain context across chunks)
- Embeddings: OpenAI text-embedding-ada-002 (fast and accurate)

### Tool Execution
- Timeout: 10 seconds for web search
- Error handling: Graceful fallback on tool failures
- Caching: Vector store persists to disk for faster reloads

### LLM Configuration
- Temperature: 0 (deterministic, consistent responses)
- Max iterations: 10 (prevent infinite loops)
- Model: gpt-3.5-turbo (cost-effective, good performance)

## Security & Privacy

- API keys stored in environment variables (not in code)
- No user data persisted beyond conversation memory
- Web search uses public DuckDuckGo (no authentication required)
- Vector database stored locally (no cloud dependencies)

## Limitations

- Requires OpenAI API key (cost associated with usage)
- Knowledge base limited to provided documents
- Web search results may not always be relevant
- No user authentication or multi-user support
- No persistent user profiles or history

## Future Enhancements

1. **User Profiles**: Store user data for personalized recommendations
2. **More Tools**: Workout generator, progress tracker, recipe finder
3. **Enhanced RAG**: Support for PDFs, images, and structured data
4. **Multi-modal**: Support voice input and image recognition
5. **Integration**: Connect to fitness apps and wearables
6. **Deployment**: Web interface, mobile app, or chatbot integration
