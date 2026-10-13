"""
Examples demonstrating individual components of FitBuddy
Run these examples to understand each component separately
"""

from tools.fitness_tools import BMICalculator, CalorieCalculator, MealPlanCalculator, WebSearchTool
from rag.knowledge_base import FitnessKnowledgeBase, initialize_knowledge_base


def example_bmi_calculator():
    """Example: Calculate BMI"""
    print("="*60)
    print("Example 1: BMI Calculator")
    print("="*60)
    
    result = BMICalculator.calculate(weight_kg=70, height_cm=175)
    print(f"Weight: 70kg, Height: 175cm")
    print(f"BMI: {result['bmi']}")
    print(f"Category: {result['category']}")
    print(f"Recommendation: {result['recommendation']}")
    print()


def example_calorie_calculator():
    """Example: Calculate daily calorie needs"""
    print("="*60)
    print("Example 2: Calorie Calculator")
    print("="*60)
    
    # Calculate BMR
    bmr = CalorieCalculator.calculate_bmr(
        weight_kg=70, 
        height_cm=175, 
        age=30, 
        gender='male'
    )
    print(f"BMR (Basal Metabolic Rate): {bmr} calories")
    
    # Calculate TDEE for moderate activity
    tdee = CalorieCalculator.calculate_tdee(bmr, 'moderate')
    print(f"TDEE (Total Daily Energy Expenditure): {tdee} calories")
    
    # Calculate target calories for weight loss
    target_loss = CalorieCalculator.calculate_target_calories(tdee, 'lose')
    print(f"Target calories for weight loss: {target_loss} calories")
    
    # Calculate target calories for weight gain
    target_gain = CalorieCalculator.calculate_target_calories(tdee, 'gain')
    print(f"Target calories for weight gain: {target_gain} calories")
    print()


def example_meal_plan_calculator():
    """Example: Calculate meal plan calories"""
    print("="*60)
    print("Example 3: Meal Plan Calculator")
    print("="*60)
    
    meal_plan = [
        {"name": "Breakfast", "calories": 400, "protein": 20, "carbs": 50, "fat": 15},
        {"name": "Lunch", "calories": 600, "protein": 35, "carbs": 70, "fat": 20},
        {"name": "Dinner", "calories": 500, "protein": 30, "carbs": 60, "fat": 18},
        {"name": "Snack", "calories": 200, "protein": 10, "carbs": 25, "fat": 8}
    ]
    
    result = MealPlanCalculator.calculate_meal_calories(meal_plan)
    print("Meal Plan:")
    for meal in meal_plan:
        print(f"  {meal['name']}: {meal['calories']} cal")
    print(f"\nTotal Calories: {result['total_calories']}")
    print(f"Total Protein: {result['total_protein']}g")
    print(f"Total Carbs: {result['total_carbs']}g")
    print(f"Total Fat: {result['total_fat']}g")
    print()


def example_knowledge_base_search():
    """Example: Search the fitness knowledge base"""
    print("="*60)
    print("Example 4: Knowledge Base Search")
    print("="*60)
    
    try:
        # Initialize knowledge base
        kb = initialize_knowledge_base()
        
        # Search for cardio exercises
        query = "cardio exercises for beginners"
        print(f"Search Query: '{query}'")
        print("\nResults:")
        
        results = kb.search(query, k=2)
        for i, result in enumerate(results, 1):
            print(f"\n{i. Source: {result['source']}")
            print(f"   Content: {result['content'][:200]}...")
            print(f"   Relevance Score: {result['relevance_score']:.4f}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set up your OPENAI_API_KEY in .env file")
        print()


def example_web_search():
    """Example: Web search for fitness information"""
    print("="*60)
    print("Example 5: Web Search")
    print("="*60)
    
    query = "beginner workout routine"
    print(f"Search Query: '{query}'")
    print("\nResults:")
    
    results = WebSearchTool.search(query, num_results=3)
    for i, result in enumerate(results, 1):
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\n{i. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Snippet: {result['snippet'][:100]}...")
    
    print()


def example_multi_step_task():
    """Example: Multi-step task using multiple tools"""
    print("="*60)
    print("Example 6: Multi-step Task")
    print("="*60)
    
    print("Task: Create a personalized nutrition plan")
    print("\nStep 1: Calculate BMI")
    bmi_result = BMICalculator.calculate(weight_kg=75, height_cm=180)
    print(f"  BMI: {bmi_result['bmi']} ({bmi_result['category']})")
    
    print("\nStep 2: Calculate daily calorie needs")
    bmr = CalorieCalculator.calculate_bmr(75, 180, 28, 'male')
    tdee = CalorieCalculator.calculate_tdee(bmr, 'moderate')
    target = CalorieCalculator.calculate_target_calories(tdee, 'maintain')
    print(f"  Daily target: {target} calories")
    
    print("\nStep 3: Create sample meal plan")
    meal_plan = [
        {"name": "Breakfast", "calories": int(target * 0.25), "protein": 25, "carbs": 60, "fat": 15},
        {"name": "Lunch", "calories": int(target * 0.35), "protein": 35, "carbs": 80, "fat": 20},
        {"name": "Dinner", "calories": int(target * 0.30), "protein": 30, "carbs": 70, "fat": 18},
        {"name": "Snacks", "calories": int(target * 0.10), "protein": 10, "carbs": 20, "fat": 8}
    ]
    
    meal_result = MealPlanCalculator.calculate_meal_calories(meal_plan)
    print(f"  Total calories: {meal_result['total_calories']}")
    print(f"  Total protein: {meal_result['total_protein']}g")
    print(f"  Total carbs: {meal_result['total_carbs']}g")
    print(f"  Total fat: {meal_result['total_fat']}g")
    
    print("\nConclusion: Personalized nutrition plan created successfully!")
    print()


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("FitBuddy Component Examples")
    print("="*60 + "\n")
    
    # Run examples
    example_bmi_calculator()
    example_calorie_calculator()
    example_meal_plan_calculator()
    example_knowledge_base_search()
    example_web_search()
    example_multi_step_task()
    
    print("="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
