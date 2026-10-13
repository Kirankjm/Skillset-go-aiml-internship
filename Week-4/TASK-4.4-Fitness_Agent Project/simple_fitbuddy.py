"""
Simple FitBuddy - No LLM Required!
Uses tools directly without an AI agent
Comprehensive Health Assistant - All Health Perspectives
"""

import sys
from tools.fitness_tools import (
    BMICalculator, 
    CalorieCalculator, 
    MealPlanCalculator, 
    WebSearchTool,
    WaterIntakeCalculator,
    SleepCalculator,
    HeartRateCalculator
)
from rag.knowledge_base import FitnessKnowledgeBase, initialize_knowledge_base


def print_menu():
    """Print the main menu"""
    print("\n" + "="*60)
    print("  HealthBuddy - Comprehensive Health Assistant")
    print("="*60)
    print("\nFITNESS & NUTRITION:")
    print("  1. Calculate BMI")
    print("  2. Calculate Daily Calories")
    print("  3. Calculate Meal Plan Calories")
    print("\nHYDRATION & SLEEP:")
    print("  4. Calculate Water Intake Needs")
    print("  5. Calculate Sleep Requirements")
    print("  6. Calculate Target Heart Rate")
    print("\nKNOWLEDGE BASE:")
    print("  7. Search Health Knowledge Base")
    print("  8. Web Search for Health Info")
    print("\n  9. Exit")
    print("="*60)


def calculate_bmi():
    """Calculate BMI"""
    print("\n--- BMI Calculator ---")
    try:
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        
        result = BMICalculator.calculate(weight, height)
        
        print(f"\nYour BMI: {result['bmi']}")
        print(f"Category: {result['category']}")
        print(f"\nRecommendation: {result['recommendation']}")
    except Exception as e:
        print(f"Error: {e}")


def calculate_calories():
    """Calculate daily calorie needs"""
    print("\n--- Calorie Calculator ---")
    try:
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        age = int(input("Enter your age: "))
        gender = input("Enter your gender (male/female): ").strip().lower()
        activity = input("Enter activity level (sedentary/light/moderate/active/very_active): ").strip().lower()
        goal = input("Enter your goal (lose/maintain/gain): ").strip().lower()
        
        bmr = CalorieCalculator.calculate_bmr(weight, height, age, gender)
        tdee = CalorieCalculator.calculate_tdee(bmr, activity)
        target = CalorieCalculator.calculate_target_calories(tdee, goal)
        
        print(f"\n--- Results ---")
        print(f"BMR (Basal Metabolic Rate): {bmr} calories/day")
        print(f"TDEE (Total Daily Energy Expenditure): {tdee} calories/day")
        print(f"Target calories for {goal}ing weight: {target} calories/day")
    except Exception as e:
        print(f"Error: {e}")


def calculate_meal_plan():
    """Calculate meal plan calories"""
    print("\n--- Meal Plan Calculator ---")
    print("Enter your meals (type 'done' when finished)")
    
    meal_plan = []
    meal_num = 1
    
    while True:
        meal_name = input(f"\nMeal {meal_num} name (or 'done'): ").strip()
        if meal_name.lower() == 'done':
            break
        
        try:
            calories = float(input(f"  Calories: "))
            protein = float(input(f"  Protein (g): "))
            carbs = float(input(f"  Carbs (g): "))
            fat = float(input(f"  Fat (g): "))
            
            meal_plan.append({
                "name": meal_name,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat
            })
            meal_num += 1
        except Exception as e:
            print(f"  Error: {e}. Please try again.")
    
    if meal_plan:
        result = MealPlanCalculator.calculate_meal_calories(meal_plan)
        print(f"\n--- Meal Plan Summary ---")
        print(f"Total Calories: {result['total_calories']}")
        print(f"Total Protein: {result['total_protein']}g")
        print(f"Total Carbs: {result['total_carbs']}g")
        print(f"Total Fat: {result['total_fat']}g")
        print(f"Number of Meals: {result['meal_count']}")
    else:
        print("No meals entered.")


def search_knowledge_base(kb):
    """Search the health knowledge base"""
    print("\n--- Health Knowledge Base Search ---")
    print("Topics available: Fitness, Nutrition, Mental Health, Sleep,")
    print("                 Disease Prevention, Hydration")
    query = input("Enter your search query: ").strip()
    
    if query:
        try:
            results = kb.search(query, k=3)
            print(f"\n--- Results for '{query}' ---")
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Source: {result['source']}")
                print(f"   Content: {result['content']}")
                print(f"   Relevance: {result['relevance_score']:.4f}")
        except Exception as e:
            print(f"Error: {e}")
            print("Note: Knowledge base requires OpenAI API key for embeddings.")
            print("If you don't have one, try the Web Search option instead.")


def web_search():
    """Search the web for fitness information"""
    print("\n--- Web Search ---")
    query = input("Enter your search query: ").strip()
    
    if query:
        try:
            results = WebSearchTool.search(query, num_results=5)
            print(f"\n--- Results for '{query}' ---")
            
            for i, result in enumerate(results, 1):
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"\n{i}. {result['title']}")
                    print(f"   URL: {result['url']}")
                    print(f"   {result['snippet'][:150]}...")
        except Exception as e:
            print(f"Error: {e}")


def calculate_water_intake():
    """Calculate daily water intake needs"""
    print("\n--- Water Intake Calculator ---")
    try:
        weight = float(input("Enter your weight (kg): "))
        activity = input("Enter activity level (sedentary/light/moderate/heavy): ").strip().lower()
        
        result = WaterIntakeCalculator.calculate(weight, activity)
        
        print(f"\n--- Results ---")
        print(f"Daily water intake: {result['daily_intake_liters']} liters")
        print(f"                    {result['daily_intake_ml']} ml")
        print(f"                    ~{result['glasses']} glasses (250ml each)")
        print(f"Activity level: {result['activity_level']}")
        print(f"\nTip: Drink water throughout the day, not all at once.")
    except Exception as e:
        print(f"Error: {e}")


def calculate_sleep():
    """Calculate sleep requirements"""
    print("\n--- Sleep Calculator ---")
    try:
        age = int(input("Enter your age: "))
        
        result = SleepCalculator.calculate(age)
        
        print(f"\n--- Results ---")
        print(f"Age category: {result['category']}")
        print(f"Recommended sleep: {result['recommended']} per night")
        print(f"Range: {result['min_hours']}-{result['max_hours']} hours")
        print(f"\nTip: Maintain consistent sleep schedule for best results.")
    except Exception as e:
        print(f"Error: {e}")


def calculate_heart_rate():
    """Calculate target heart rate"""
    print("\n--- Heart Rate Calculator ---")
    try:
        age = int(input("Enter your age: "))
        intensity = input("Enter exercise intensity (light/moderate/vigorous): ").strip().lower()
        
        result = HeartRateCalculator.calculate_target_hr(age, intensity)
        
        print(f"\n--- Results ---")
        print(f"Maximum heart rate: {result['max_heart_rate']} bpm")
        print(f"Target heart rate zone: {result['target_zone']}")
        print(f"Intensity: {result['intensity']}")
        print(f"\nTip: Use heart rate monitor during exercise to stay in target zone.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main application loop"""
    print("\n" + "="*60)
    print("  HealthBuddy - Comprehensive Health Assistant")
    print("="*60)
    print("\nYour all-in-one health guide covering:")
    print("  • Fitness & Nutrition")
    print("  • Hydration & Sleep")
    print("  • Mental Health")
    print("  • Disease Prevention")
    print("  • Wellness Knowledge Base")
    print("\nNo API key required!")
    print()
    
    # Try to initialize knowledge base (may fail without OpenAI key)
    kb = None
    try:
        print("Initializing health knowledge base...")
        kb = initialize_knowledge_base()
        print("Knowledge base loaded successfully!")
    except Exception as e:
        print(f"Knowledge base unavailable: {e}")
        print("(This is normal without an OpenAI API key)")
        print("Use Web Search instead for information.")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            calculate_bmi()
        elif choice == '2':
            calculate_calories()
        elif choice == '3':
            calculate_meal_plan()
        elif choice == '4':
            calculate_water_intake()
        elif choice == '5':
            calculate_sleep()
        elif choice == '6':
            calculate_heart_rate()
        elif choice == '7':
            if kb:
                search_knowledge_base(kb)
            else:
                print("\nKnowledge base not available (requires OpenAI API key).")
                print("Use Web Search (option 8) instead.")
        elif choice == '8':
            web_search()
        elif choice == '9':
            print("\nThank you for using HealthBuddy! Stay healthy! 💪")
            break
        else:
            print("\nInvalid choice. Please enter 1-9.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
