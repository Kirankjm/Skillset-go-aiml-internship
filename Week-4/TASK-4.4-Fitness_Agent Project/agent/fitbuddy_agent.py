"""
FitBuddy AI Agent - Main Agent with RAG, Tool Use, and Multi-step Reasoning
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from rag.knowledge_base import FitnessKnowledgeBase, initialize_knowledge_base
from tools.fitness_tools import (
    BMICalculator, 
    CalorieCalculator, 
    MealPlanCalculator,
    WebSearchTool,
    WaterIntakeCalculator,
    SleepCalculator,
    HeartRateCalculator
)


class FitBuddyAgent:
    """AI Health Helper Agent with RAG and tool use capabilities"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        """
        Initialize the HealthBuddy Agent
        
        Args:
            api_key: API key (if None, loads from environment)
            model: Model to use (if None, auto-detects)
            base_url: Custom base URL (e.g., Groq URL)
        """
        load_dotenv()
        
        # Set up API key - try Groq first, then OpenAI
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key not found. Set GROQ_API_KEY or OPENAI_API_KEY environment variable.")
        
        # Determine provider and model
        if base_url:
            self.base_url = base_url
            provider = "custom"
        elif "gsk-" in self.api_key:
            # Groq API key
            self.base_url = "https://api.groq.com/openai/v1"
            provider = "groq"
            if not model:
                model = "llama3-8b-8192"  # Stable Groq model
        else:
            # OpenAI API key
            self.base_url = None
            provider = "openai"
            if not model:
                model = "gpt-3.5-turbo"
        
        print(f"Using {provider.upper()} with model: {model}")
        
        # Initialize LLM
        if self.base_url:
            self.llm = ChatOpenAI(
                model=model, 
                temperature=0,
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.llm = ChatOpenAI(model=model, temperature=0, api_key=self.api_key)
        
        # Initialize knowledge base (requires OpenAI API key for embeddings)
        print("Initializing health knowledge base...")
        # Use OPENAI_API_KEY for embeddings (RAG needs embeddings even if LLM uses Groq)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.knowledge_base = initialize_knowledge_base(openai_api_key=openai_key)
                print("[OK] Knowledge base loaded successfully")
            except Exception as e:
                print(f"[WARN] Knowledge base unavailable: {e}")
                print("  (Health guides search may not work, but other tools will)")
                self.knowledge_base = None
        else:
            print("[WARN] No OpenAI API key for embeddings")
            print("  (Knowledge base search unavailable, but other tools will work)")
            self.knowledge_base = None
        
        # Set up memory for conversation context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create tools
        self.tools = self._create_tools()
        
        # Create agent
        self.agent = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create the list of available tools for the agent"""
        
        def bmi_tool_func(input_str: str) -> str:
            """Calculate BMI from input string 'weight_kg,height_cm'"""
            try:
                parts = input_str.split(',')
                weight = float(parts[0].strip())
                height = float(parts[1].strip())
                result = BMICalculator.calculate(weight, height)
                return str(result)
            except Exception as e:
                return f"Error calculating BMI: {str(e)}"
        
        def calorie_tool_func(input_str: str) -> str:
            """Calculate daily calories from input string 'weight_kg,height_cm,age,gender,activity_level,goal'"""
            try:
                parts = input_str.split(',')
                weight = float(parts[0].strip())
                height = float(parts[1].strip())
                age = int(parts[2].strip())
                gender = parts[3].strip()
                activity = parts[4].strip()
                goal = parts[5].strip()
                
                bmr = CalorieCalculator.calculate_bmr(weight, height, age, gender)
                tdee = CalorieCalculator.calculate_tdee(bmr, activity)
                target = CalorieCalculator.calculate_target_calories(tdee, goal)
                
                return f"BMR: {bmr} cal, TDEE: {tdee} cal, Target: {target} cal"
            except Exception as e:
                return f"Error calculating calories: {str(e)}"
        
        def meal_calculator_tool_func(input_str: str) -> str:
            """Calculate meal plan calories from JSON-like string"""
            try:
                # Simple parsing for demonstration
                # In production, would use proper JSON parsing
                import json
                meal_plan = json.loads(input_str)
                result = MealPlanCalculator.calculate_meal_calories(meal_plan)
                return str(result)
            except Exception as e:
                return f"Error calculating meal calories: {str(e)}"
        
        def web_search_tool_func(query: str) -> str:
            """Search the web for fitness information"""
            try:
                results = WebSearchTool.search(query, num_results=3)
                return str(results)
            except Exception as e:
                return f"Error searching web: {str(e)}"
        
        def water_intake_tool_func(input_str: str) -> str:
            """Calculate water intake from input string 'weight_kg,activity_level'"""
            try:
                parts = input_str.split(',')
                weight = float(parts[0].strip())
                activity = parts[1].strip()
                result = WaterIntakeCalculator.calculate(weight, activity)
                return str(result)
            except Exception as e:
                return f"Error calculating water intake: {str(e)}"
        
        def sleep_tool_func(input_str: str) -> str:
            """Calculate sleep needs from input string 'age'"""
            try:
                age = int(input_str.strip())
                result = SleepCalculator.calculate(age)
                return str(result)
            except Exception as e:
                return f"Error calculating sleep needs: {str(e)}"
        
        def heart_rate_tool_func(input_str: str) -> str:
            """Calculate target heart rate from input string 'age,intensity'"""
            try:
                parts = input_str.split(',')
                age = int(parts[0].strip())
                intensity = parts[1].strip()
                result = HeartRateCalculator.calculate_target_hr(age, intensity)
                return str(result)
            except Exception as e:
                return f"Error calculating heart rate: {str(e)}"
        
        def knowledge_search_tool_func(query: str) -> str:
            """Search the health knowledge base"""
            if not self.knowledge_base:
                return "Knowledge base not available. Requires OpenAI API key for embeddings. Use Web Search instead."
            try:
                results = self.knowledge_base.search(query, k=3)
                formatted = "\n".join([
                    f"From {r['source']}: {r['content'][:200]}..." 
                    for r in results
                ])
                return formatted
            except Exception as e:
                return f"Error searching knowledge base: {str(e)}"
        
        tools = [
            Tool(
                name="BMI Calculator",
                func=bmi_tool_func,
                description="Calculate BMI and get health recommendations. Input format: 'weight_kg,height_cm' (e.g., '70,175')"
            ),
            Tool(
                name="Calorie Calculator",
                func=calorie_tool_func,
                description="Calculate daily calorie needs. Input format: 'weight_kg,height_cm,age,gender,activity_level,goal' (e.g., '70,175,30,male,moderate,maintain'). Activity levels: sedentary, light, moderate, active, very_active. Goals: lose, maintain, gain"
            ),
            Tool(
                name="Meal Plan Calculator",
                func=meal_calculator_tool_func,
                description="Calculate total calories in a meal plan. Input: JSON array of meals with calories, protein, carbs, fat fields"
            ),
            Tool(
                name="Water Intake Calculator",
                func=water_intake_tool_func,
                description="Calculate daily water intake needs. Input format: 'weight_kg,activity_level' (e.g., '75,moderate'). Activity levels: sedentary, light, moderate, heavy"
            ),
            Tool(
                name="Sleep Calculator",
                func=sleep_tool_func,
                description="Calculate recommended sleep duration. Input format: 'age' (e.g., '25')"
            ),
            Tool(
                name="Heart Rate Calculator",
                func=heart_rate_tool_func,
                description="Calculate target heart rate zone. Input format: 'age,intensity' (e.g., '30,moderate'). Intensity: light, moderate, vigorous"
            ),
            Tool(
                name="Web Search",
                func=web_search_tool_func,
                description="Search the web for health and fitness information. Input: search query string"
            ),
            Tool(
                name="Health Knowledge Base",
                func=knowledge_search_tool_func,
                description="Search the built-in health guides (fitness, nutrition, mental health, sleep, disease prevention, hydration). Input: search query string"
            )
        ]
        
        return tools
    
    def _create_agent(self) -> AgentExecutor:
        """Create the ReAct agent with tools"""
        
        # Define the prompt template
        template = """You are HealthBuddy, a comprehensive AI health assistant. 
You have access to tools to help users with all health perspectives including fitness, nutrition, mental health, sleep, hydration, and disease prevention.

Available tools:
{tools}

Tool names: {tool_names}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        )
        
        # Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        return agent_executor
    
    def query(self, user_input: str) -> str:
        """
        Process a user query through the agent
        
        Args:
            user_input: User's question or request
            
        Returns:
            Agent's response
        """
        try:
            response = self.agent.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def reset_memory(self):
        """Clear the conversation memory"""
        self.memory.clear()


def create_agent(api_key: str = None, model: str = None, base_url: str = None) -> FitBuddyAgent:
    """
    Factory function to create a HealthBuddy agent
    
    Args:
        api_key: API key (if None, auto-detects from environment)
        model: Model to use (if None, auto-detects based on provider)
        base_url: Custom base URL (e.g., Groq URL)
        
    Returns:
        Initialized FitBuddyAgent instance
    """
    return FitBuddyAgent(api_key=api_key, model=model, base_url=base_url)
