"""
Perfect Fitness Agent - Seamless Chat Interface
Demonstrates RAG, Tool Use, and Multi-step Reasoning without API
"""

import re
from tools.fitness_tools import (
    BMICalculator, 
    CalorieCalculator, 
    MealPlanCalculator,
    WebSearchTool,
    WaterIntakeCalculator,
    SleepCalculator,
    HeartRateCalculator
)


class PerfectFitnessAgent:
    """Perfect Fitness Agent with seamless interface"""
    
    def __init__(self):
        """Initialize the agent"""
        self.conversation_history = []
        print("Perfect Fitness Agent initialized!")
    
    def extract_numbers(self, text):
        """Extract numbers from text"""
        return re.findall(r'\d+\.?\d*', text)
    
    def process_query(self, user_input):
        """
        Process user query with intelligent routing
        Demonstrates multi-step reasoning and tool use
        """
        user_input_lower = user_input.lower()
        
        # BMI Calculation
        if 'bmi' in user_input_lower:
            numbers = self.extract_numbers(user_input)
            if len(numbers) >= 2:
                weight = float(numbers[0])
                height = float(numbers[1])
                result = BMICalculator.calculate(weight, height)
                return self.format_bmi_response(result, weight, height)
        
        # Calorie Calculation
        elif 'calorie' in user_input_lower or 'how many calories' in user_input_lower:
            return self.handle_calorie_query(user_input)
        
        # Water Intake
        elif 'water' in user_input_lower or 'drink' in user_input_lower:
            numbers = self.extract_numbers(user_input)
            if numbers:
                weight = float(numbers[0])
                activity = 'moderate'  # default
                if 'sedentary' in user_input_lower:
                    activity = 'sedentary'
                elif 'light' in user_input_lower:
                    activity = 'light'
                elif 'heavy' in user_input_lower:
                    activity = 'heavy'
                result = WaterIntakeCalculator.calculate(weight, activity)
                return self.format_water_response(result, weight, activity)
        
        # Sleep
        elif 'sleep' in user_input_lower:
            numbers = self.extract_numbers(user_input)
            if numbers:
                age = int(numbers[0])
                result = SleepCalculator.calculate(age)
                return self.format_sleep_response(result, age)
        
        # Heart Rate
        elif 'heart rate' in user_input_lower:
            return self.handle_heart_rate_query(user_input)
        
        # Meal Plan
        elif 'meal plan' in user_input_lower or 'meal' in user_input_lower:
            return self.handle_meal_plan_query(user_input)
        
        # Fitness/Exercise Advice
        elif any(word in user_input_lower for word in ['exercise', 'workout', 'fitness', 'cardio', 'strength']):
            return self.search_knowledge_base(user_input, 'fitness')
        
        # Nutrition Advice
        elif any(word in user_input_lower for word in ['nutrition', 'diet', 'eat', 'food', 'protein', 'carbs']):
            return self.search_knowledge_base(user_input, 'nutrition')
        
        # Mental Health
        elif any(word in user_input_lower for word in ['stress', 'mental', 'anxiety', 'mindful']):
            return self.search_knowledge_base(user_input, 'mental')
        
        # General web search
        else:
            return self.web_search(user_input)
    
    def handle_calorie_query(self, user_input):
        """Handle calorie calculation with multiple steps"""
        user_input_lower = user_input.lower()
        
        # Extract information
        numbers = self.extract_numbers(user_input)
        
        if len(numbers) >= 3:
            weight = float(numbers[0])
            height = float(numbers[1])
            age = int(numbers[2])
            
            # Extract gender
            gender = 'male' if 'male' in user_input_lower or 'man' in user_input_lower else 'female'
            
            # Extract activity level
            activity = 'moderate'
            if 'sedentary' in user_input_lower:
                activity = 'sedentary'
            elif 'light' in user_input_lower:
                activity = 'light'
            elif 'active' in user_input_lower:
                activity = 'active'
            elif 'very active' in user_input_lower:
                activity = 'very_active'
            
            # Extract goal
            goal = 'maintain'
            if 'lose' in user_input_lower:
                goal = 'lose'
            elif 'gain' in user_input_lower:
                goal = 'gain'
            
            # Multi-step calculation
            bmr = CalorieCalculator.calculate_bmr(weight, height, age, gender)
            tdee = CalorieCalculator.calculate_tdee(bmr, activity)
            target = CalorieCalculator.calculate_target_calories(tdee, goal)
            
            return self.format_calorie_response(bmr, tdee, target, goal, activity)
        
        return "I need more information to calculate your calorie needs. Please provide your weight (kg), height (cm), age, gender, and activity level."
    
    def handle_heart_rate_query(self, user_input):
        """Handle heart rate calculation"""
        user_input_lower = user_input.lower()
        numbers = self.extract_numbers(user_input)
        
        if numbers:
            age = int(numbers[0])
            intensity = 'moderate'
            if 'light' in user_input_lower:
                intensity = 'light'
            elif 'vigorous' in user_input_lower:
                intensity = 'vigorous'
            
            result = HeartRateCalculator.calculate_target_hr(age, intensity)
            return self.format_heart_rate_response(result, age, intensity)
        
        return "I need your age to calculate target heart rate. Also specify intensity (light/moderate/vigorous)."
    
    def handle_meal_plan_query(self, user_input):
        """Handle meal plan creation with calorie tracking"""
        # Extract calorie target
        numbers = self.extract_numbers(user_input)
        target_calories = 2000  # default
        if numbers:
            target_calories = int(numbers[0])
        
        # Create a balanced meal plan
        meal_plan = [
            {"name": "Breakfast", "calories": int(target_calories * 0.25), "protein": 20, "carbs": 50, "fat": 15},
            {"name": "Lunch", "calories": int(target_calories * 0.35), "protein": 35, "carbs": 70, "fat": 20},
            {"name": "Dinner", "calories": int(target_calories * 0.30), "protein": 30, "carbs": 60, "fat": 18},
            {"name": "Snacks", "calories": int(target_calories * 0.10), "protein": 10, "carbs": 20, "fat": 8}
        ]
        
        result = MealPlanCalculator.calculate_meal_calories(meal_plan)
        return self.format_meal_plan_response(result, meal_plan, target_calories)
    
    def search_knowledge_base(self, query, category):
        """Search knowledge base files"""
        import os
        from pathlib import Path
        
        kb_dir = Path("knowledge_base")
        results = []
        
        if kb_dir.exists():
            for file_path in kb_dir.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    query_lower = query.lower()
                    
                    # Simple keyword matching
                    score = 0
                    for word in query_lower.split():
                        if word in content:
                            score += 1
                    
                    if score > 0:
                        results.append({
                            'file': file_path.name,
                            'score': score,
                            'content': content[:500]
                        })
        
        if results:
            results.sort(key=lambda x: x['score'], reverse=True)
            return self.format_knowledge_response(results[:2], query)
        else:
            return self.web_search(query)
    
    def web_search(self, query):
        """Perform web search"""
        try:
            results = WebSearchTool.search(query, num_results=3)
            return self.format_web_search_response(results, query)
        except Exception as e:
            return f"I couldn't search the web right now. Error: {e}"
    
    def format_bmi_response(self, result, weight, height):
        """Format BMI response"""
        response = "[BMI] BMI Calculation Results:\n"
        response += "==========================================\n"
        response += f"Weight: {weight} kg\n"
        response += f"Height: {height} cm\n\n"
        response += f"Your BMI: {result['bmi']}\n"
        response += f"Category: {result['category']}\n\n"
        response += "Recommendation:\n"
        response += f"{result['recommendation']}\n\n"
        response += "[TIP] A healthy BMI is between 18.5 and 24.9. Regular exercise and balanced diet help maintain a healthy weight."
        return response
    
    def format_calorie_response(self, bmr, tdee, target, goal, activity):
        """Format calorie response"""
        response = "[CALORIES] Calorie Calculation Results:\n"
        response += "==========================================\n"
        response += f"Your Basal Metabolic Rate (BMR): {bmr} calories/day\n"
        response += f"Your Total Daily Energy Expenditure (TDEE): {tdee} calories/day\n"
        response += f"Activity Level: {activity}\n\n"
        response += f"Target Calories to {goal} weight: {target} calories/day\n\n"
        response += f"[TIP] To {goal} weight, eat {target} calories daily. Combine with regular exercise for best results!"
        return response
    
    def format_water_response(self, result, weight, activity):
        """Format water response"""
        response = "[WATER] Water Intake Recommendations:\n"
        response += "==========================================\n"
        response += f"Weight: {weight} kg\n"
        response += f"Activity Level: {activity}\n\n"
        response += "Daily Water Intake:\n"
        response += f"* {result['daily_intake_liters']} liters\n"
        response += f"* {result['daily_intake_ml']} ml\n"
        response += f"* ~{result['glasses']} glasses (250ml each)\n\n"
        response += "[TIP] Drink water throughout the day, not all at once. Increase intake during exercise and hot weather."
        return response
    
    def format_sleep_response(self, result, age):
        """Format sleep response"""
        response = "[SLEEP] Sleep Recommendations:\n"
        response += "==========================================\n"
        response += f"Age: {age} years\n"
        response += f"Age Category: {result['category']}\n\n"
        response += f"Recommended Sleep: {result['recommended']} per night\n"
        response += f"Range: {result['min_hours']}-{result['max_hours']} hours\n\n"
        response += "[TIP] Maintain a consistent sleep schedule, even on weekends. Avoid screens 1 hour before bed for better sleep quality."
        return response
    
    def format_heart_rate_response(self, result, age, intensity):
        """Format heart rate response"""
        response = "[HEART RATE] Heart Rate Zone:\n"
        response += "==========================================\n"
        response += f"Age: {age} years\n"
        response += f"Maximum Heart Rate: {result['max_heart_rate']} bpm\n"
        response += f"Exercise Intensity: {result['intensity']}\n\n"
        response += f"Target Heart Rate Zone: {result['target_zone']} bpm\n\n"
        response += "[TIP] Stay in your target zone during exercise for optimal cardio benefits. Use a heart rate monitor to track your intensity."
        return response
    
    def format_meal_plan_response(self, result, meal_plan, target):
        """Format meal plan response"""
        response = f"[MEAL PLAN] Meal Plan ({target} calories):\n"
        response += "==========================================\n"
        
        for meal in meal_plan:
            response += f"\n{meal['name']}: {meal['calories']} cal (P: {meal['protein']}g, C: {meal['carbs']}g, F: {meal['fat']}g)"
        
        response += "\n\n==========================================\n"
        response += f"Total Calories: {result['total_calories']}\n"
        response += f"Total Protein: {result['total_protein']}g\n"
        response += f"Total Carbs: {result['total_carbs']}g\n"
        response += f"Total Fat: {result['total_fat']}g\n\n"
        response += "[TIP] Adjust portions based on your hunger and activity level. Eat whole foods for better nutrition!"
        return response
    
    def format_knowledge_response(self, results, query):
        """Format knowledge base response"""
        response = "[KNOWLEDGE BASE] Information from Health Guides:\n"
        response += "==========================================\n"
        response += f'Query: "{query}"\n\n'
        
        for i, result in enumerate(results, 1):
            response += f"{i}. From {result['file']}:\n"
            response += f"   {result['content'][:300]}...\n"
        
        response += "\n[TIP] For more specific information, try searching with more detailed keywords."
        return response
    
    def format_web_search_response(self, results, query):
        """Format web search response"""
        response = "[WEB SEARCH] Web Search Results:\n"
        response += "==========================================\n"
        response += f'Query: "{query}"\n\n'
        
        for i, result in enumerate(results, 1):
            if "error" not in result:
                response += f"{i}. {result['title']}\n"
                response += f"   {result['snippet'][:150]}...\n"
                response += f"   URL: {result['url']}\n"
        
        response += "\n[TIP] Always verify health information with healthcare professionals."
        return response


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*70)
    print("  Perfect Fitness Agent - Your AI Health Assistant")
    print("="*70)
    print("\nI can help you with:")
    print("  * BMI calculation and health analysis")
    print("  * Daily calorie needs and meal planning")
    print("  * Water intake recommendations")
    print("  * Sleep requirements by age")
    print("  * Target heart rate zones")
    print("  * Fitness and nutrition guidance")
    print("  * Mental health and stress management")
    print("\nFeatures:")
    print("  * RAG (Retrieval from health knowledge base)")
    print("  * Tool Use (7 health calculators)")
    print("  * Multi-step reasoning (chained calculations)")
    print("  * No API key required")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("="*70 + "\n")


def print_examples():
    """Print example queries"""
    print("\nExample queries you can try:")
    print("  1. What's my BMI if I weigh 70kg and am 175cm tall?")
    print("  2. How many calories should I eat to lose weight? I'm 30, male, 70kg, 175cm, moderately active.")
    print("  3. How much water should I drink daily if I weigh 75kg and am moderately active?")
    print("  4. How many hours of sleep do I need at age 25?")
    print("  5. What's my target heart rate if I'm 30 and doing moderate exercise?")
    print("  6. Create a meal plan for me with around 2000 calories.")
    print("  7. What are some good cardio exercises for beginners?")
    print("  8. What should I eat before a workout?")
    print("  9. How can I manage stress effectively?")
    print("  10. Search for information about intermittent fasting.")
    print()


def main():
    """Main application loop"""
    print_welcome()
    print_examples()
    
    # Initialize agent
    agent = PerfectFitnessAgent()
    
    print("Perfect Fitness Agent is ready!\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n" + "="*70)
                print("Thank you for using Perfect Fitness Agent! Stay healthy!")
                print("="*70 + "\n")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the query
            print("\nProcessing your query...")
            response = agent.process_query(user_input)
            
            print(f"\nAgent: {response}\n")
            print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Thank you for using Perfect Fitness Agent! Stay healthy!")
            print("="*70 + "\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            print("Please try again or type 'quit' to exit.\n")


if __name__ == "__main__":
    main()
