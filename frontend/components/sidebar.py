import streamlit as st

def sidebar_component():
    """
    Renders the sidebar for user inputs and returns the profile data.
    """
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3075/3075977.png", width=100)
        st.title("NutriLens Profile")
        
        st.header("Your Stats")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
        
        st.header("Your Goal")
        goal = st.selectbox(
            "Objective", 
            ["Maintain Weight", "Lose Weight (Cut)", "Gain Muscle (Bulk)"]
        )
        
        activity_level = st.select_slider(
            "Activity Level",
            options=["Sedentary", "Light", "Moderate", "Active", "Athlete"]
        )
        
        # Calculate BMR (Mifflin-St Jeor Equation) - Simplified
        # In a real app, we'd check gender. Assuming Male for this simplified logic.
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        
        # TDEE Multipliers
        multipliers = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Athlete": 1.9
        }
        tdee = bmr * multipliers[activity_level]
        
        # Adjust for Goal
        if "Lose" in goal:
            target_calories = tdee - 500
        elif "Gain" in goal:
            target_calories = tdee + 400
        else:
            target_calories = tdee
            
        st.metric("Daily Calorie Target", f"{int(target_calories)} kcal")
        
        return {
            "age": age,
            "weight": weight,
            "height": height,
            "goal": goal,
            "target_calories": int(target_calories)
        }