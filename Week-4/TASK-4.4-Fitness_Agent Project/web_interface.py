"""
Perfect Fitness Agent - Web Interface
Beautiful Streamlit-based UI for seamless interaction
"""

import streamlit as st
from tools.fitness_tools import (
    BMICalculator,
    CalorieCalculator,
    MealPlanCalculator,
    WaterIntakeCalculator,
    SleepCalculator,
    HeartRateCalculator,
    WebSearchTool
)


def set_page_config():
    """Configure the Streamlit page"""
    st.set_page_config(
        page_title="Perfect Fitness Agent",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def display_header():
    """Display the main header"""
    st.title("💪 Perfect Fitness Agent")
    st.markdown("---")
    st.markdown("### Your AI Health Assistant")
    st.markdown("Calculate health metrics, get personalized recommendations, and search for health information.")
    st.markdown("---")


def bmi_calculator_ui():
    """BMI Calculator UI"""
    st.subheader("📊 BMI Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0, step=1.0)
    
    if st.button("Calculate BMI", key="bmi"):
        result = BMICalculator.calculate(weight_kg=weight, height_cm=height)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"**BMI: {result['bmi']}**")
            st.info(f"**Category: {result['category']}**")
            st.markdown(f"**Recommendation:** {result['recommendation']}")
            
            # Visual indicator
            bmi = result['bmi']
            if bmi < 18.5:
                st.warning("⚠️ You are underweight. Consider consulting a nutritionist.")
            elif 18.5 <= bmi < 25:
                st.success("✅ Your weight is in the healthy range!")
            elif 25 <= bmi < 30:
                st.warning("⚠️ You are slightly overweight. Consider increasing physical activity.")
            else:
                st.error("❌ You are in the obese range. Please consult a healthcare provider.")


def calorie_calculator_ui():
    """Calorie Calculator UI"""
    st.subheader("🔥 Daily Calorie Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0, step=1.0)
    
    with col2:
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary (little or no exercise)",
             "Light (exercise 1-3 days/week)",
             "Moderate (exercise 3-5 days/week)",
             "Active (exercise 6-7 days/week)",
             "Very Active (hard exercise daily)"]
        )
        goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Weight"])
    
    if st.button("Calculate Calories", key="calories"):
        # Map activity levels
        activity_map = {
            "Sedentary (little or no exercise)": "sedentary",
            "Light (exercise 1-3 days/week)": "light",
            "Moderate (exercise 3-5 days/week)": "moderate",
            "Active (exercise 6-7 days/week)": "active",
            "Very Active (hard exercise daily)": "very_active"
        }
        
        # Map goals
        goal_map = {
            "Maintain Weight": "maintain",
            "Lose Weight": "lose",
            "Gain Weight": "gain"
        }
        
        activity = activity_map[activity_level]
        target_goal = goal_map[goal]
        
        # Calculate step by step
        bmr = CalorieCalculator.calculate_bmr(weight_kg=weight, height_cm=height, age=age, gender=gender.lower())
        tdee = CalorieCalculator.calculate_tdee(bmr, activity_level=activity)
        target = CalorieCalculator.calculate_target_calories(tdee, goal=target_goal)
        
        # Display results
        st.markdown("### 📈 Your Calorie Breakdown")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("BMR (Basal Metabolic Rate)", f"{bmr:.0f} cal/day")
        with col2:
            st.metric("TDEE (Total Daily Energy)", f"{tdee:.0f} cal/day")
        with col3:
            st.metric("Target Calories", f"{target:.0f} cal/day")
        
        st.info(f"**To {goal.lower()}, consume approximately {target:.0f} calories per day.**")


def meal_plan_calculator_ui():
    """Meal Plan Calculator UI"""
    st.subheader("🍽️ Meal Plan Calculator")
    
    st.markdown("Add foods to your meal plan:")
    
    # Initialize session state for meal items
    if 'meal_items' not in st.session_state:
        st.session_state.meal_items = []
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        food_name = st.text_input("Food Name", key="food_name")
    with col2:
        calories = st.number_input("Calories", min_value=0, value=100, key="calories")
    with col3:
        protein = st.number_input("Protein (g)", min_value=0, value=0, key="protein")
    with col4:
        carbs = st.number_input("Carbs (g)", min_value=0, value=0, key="carbs")
    with col5:
        fat = st.number_input("Fat (g)", min_value=0, value=0, key="fat")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Food", key="add_food"):
            if food_name:
                st.session_state.meal_items.append({
                    "name": food_name,
                    "calories": calories,
                    "protein": protein,
                    "carbs": carbs,
                    "fat": fat
                })
                st.success(f"Added {food_name}!")
                st.rerun()
    with col2:
        if st.button("Clear Meal Plan", key="clear_meal"):
            st.session_state.meal_items = []
            st.success("Meal plan cleared!")
            st.rerun()
    
    # Display current meal plan
    if st.session_state.meal_items:
        st.markdown("### Current Meal Plan")
        
        # Create dataframe-like display
        for i, item in enumerate(st.session_state.meal_items, 1):
            st.markdown(f"**{i}. {item['name']}** - {item['calories']} cal (P: {item['protein']}g, C: {item['carbs']}g, F: {item['fat']}g)")
        
        # Calculate totals
        result = MealPlanCalculator.calculate_meal_calories(st.session_state.meal_items)
        
        st.markdown("---")
        st.markdown("### 📊 Meal Totals")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Calories", f"{result['total_calories']} cal")
        with col2:
            st.metric("Total Protein", f"{result['total_protein']}g")
        with col3:
            st.metric("Total Carbs", f"{result['total_carbs']}g")
        with col4:
            st.metric("Total Fat", f"{result['total_fat']}g")
    else:
        st.info("No foods added yet. Add foods above to calculate meal totals.")


def water_calculator_ui():
    """Water Intake Calculator UI"""
    st.subheader("💧 Water Intake Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=75.0, step=0.5)
    with col2:
        activity_level = st.selectbox(
            "Activity Level",
            ["Sedentary", "Light", "Moderate", "Heavy"]
        )
    
    if st.button("Calculate Water Intake", key="water"):
        result = WaterIntakeCalculator.calculate(weight_kg=weight, activity_level=activity_level)
        
        st.markdown("### 💧 Your Daily Water Intake")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Liters", f"{result['daily_intake_liters']} L")
        with col2:
            st.metric("Milliliters", f"{result['daily_intake_ml']} ml")
        with col3:
            st.metric("Glasses", f"{result['glasses']} glasses")
        
        st.info(f"**💡 Tip:** Drink water throughout the day, not all at once. Aim for {result['glasses']} glasses (250ml each).")


def sleep_calculator_ui():
    """Sleep Calculator UI"""
    st.subheader("😴 Sleep Requirements Calculator")
    
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    
    if st.button("Calculate Sleep Needs", key="sleep"):
        result = SleepCalculator.calculate(age=age)
        
        st.markdown("### 😴 Recommended Sleep Duration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Minimum", f"{result['min_hours']} hours")
        with col2:
            st.metric("Maximum", f"{result['max_hours']} hours")
        
        st.success(f"**Recommended: {result['recommended']} per day**")
        st.info(f"**Category: {result['category']}**")
        
        st.markdown("---")
        st.markdown("### 💡 Sleep Tips")
        st.markdown("""
        - Maintain a consistent sleep schedule
        - Create a relaxing bedtime routine
        - Avoid screens before bed
        - Keep your bedroom cool and dark
        - Limit caffeine and alcohol before bedtime
        """)


def heart_rate_calculator_ui():
    """Heart Rate Calculator UI"""
    st.subheader("❤️ Target Heart Rate Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
    with col2:
        intensity = st.selectbox(
            "Exercise Intensity",
            ["Light", "Moderate", "Vigorous"]
        )
    
    if st.button("Calculate Target Heart Rate", key="heart_rate"):
        result = HeartRateCalculator.calculate_target_hr(age=age, intensity=intensity)
        
        st.markdown("### ❤️ Your Target Heart Rate Zone")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Heart Rate", f"{result['max_heart_rate']} bpm")
        with col2:
            st.metric("Target Zone", f"{result['target_zone']}")
        with col3:
            st.metric("Intensity", result['intensity'].title())
        
        st.info(f"**💡 Tip:** Keep your heart rate between {result['target_min']}-{result['target_max']} bpm during {intensity.lower()} exercise.")


def web_search_ui():
    """Web Search UI"""
    st.subheader("🌐 Web Search for Health Information")
    
    query = st.text_input("Search Query", placeholder="e.g., benefits of morning exercise")
    num_results = st.slider("Number of Results", min_value=1, max_value=10, value=5)
    
    if st.button("Search", key="web_search"):
        if query:
            with st.spinner("Searching..."):
                results = WebSearchTool.search(query, num_results=num_results)
            
            if results and not any("error" in r for r in results):
                st.markdown(f"### 📊 Search Results for: '{query}'")
                
                for i, result in enumerate(results, 1):
                    st.markdown(f"**{i}. {result.get('title', 'No title')}**")
                    st.markdown(f"🔗 {result.get('url', 'No URL')}")
                    st.markdown(f"{result.get('snippet', 'No description')}")
                    st.markdown("---")
            else:
                st.error("Search failed or no results found. Try a different query.")
        else:
            st.warning("Please enter a search query.")


def main():
    """Main application"""
    set_page_config()
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    
    page = st.sidebar.radio(
        "Select a Tool",
        ["BMI Calculator",
         "Calorie Calculator",
         "Meal Plan Calculator",
         "Water Intake Calculator",
         "Sleep Calculator",
         "Heart Rate Calculator",
         "Web Search"]
    )
    
    # Display selected page
    if page == "BMI Calculator":
        bmi_calculator_ui()
    elif page == "Calorie Calculator":
        calorie_calculator_ui()
    elif page == "Meal Plan Calculator":
        meal_plan_calculator_ui()
    elif page == "Water Intake Calculator":
        water_calculator_ui()
    elif page == "Sleep Calculator":
        sleep_calculator_ui()
    elif page == "Heart Rate Calculator":
        heart_rate_calculator_ui()
    elif page == "Web Search":
        web_search_ui()
    
    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Perfect Fitness Agent** is an AI-powered health assistant that demonstrates:
    - **RAG (Retrieval-Augmented Generation)** - Knowledge base with health guides
    - **Tool Use** - 7 intelligent health calculators
    - **Multi-step Reasoning** - Chained calculations for complex queries
    
    **No API key required!** All calculators work completely offline.
    """)
    st.markdown("---")
    st.markdown("💪 *Stay Healthy, Stay Happy!*")


if __name__ == "__main__":
    main()
