import streamlit as st
import requests
from PIL import Image
import io

# Local Imports
from components.sidebar import sidebar_component
from components.charts import plot_macros, plot_calories_gauge
from utils import draw_bounding_boxes

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
API_URL = "http://127.0.0.1:8000/analyze"
st.set_page_config(page_title="NutriLens AI", layout="wide")

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
user_profile = sidebar_component()

# ---------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------
st.title("🍽️ NutriLens AI")
st.markdown("### Snap a photo. Track your nutrition. Reach your goals.")

# Layout: Two columns (Upload/Image vs Results)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Meal")
    uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file is not None:
        # Display the uploaded image immediately
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Meal", use_column_width=True)
        
        # Analyze Button
        if st.button("🔍 Analyze Nutrition", type="primary"):
            with st.spinner("🤖 AI is detecting food items and calculating macros..."):
                try:
                    # Reset pointer to beginning of file
                    uploaded_file.seek(0)
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    # Call Backend API
                    response = requests.post(API_URL, files=files)
                    
                    if response.status_code == 200:
                        st.success("Analysis Complete!")
                        st.session_state['analysis_result'] = response.json()
                        st.session_state['uploaded_image'] = image 
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error. Is the backend running? {e}")

# ---------------------------------------------------------
# RESULTS SECTION
# ---------------------------------------------------------
with col2:
    st.subheader("2. Nutritional Insights")
    
    if 'analysis_result' in st.session_state:
        data = st.session_state['analysis_result']
        img = st.session_state['uploaded_image']
        
        # 1. VISUALIZATION (Draw Bounding Boxes)
        annotated_img = draw_bounding_boxes(img, data.get('foods', []))
        st.image(annotated_img, caption="AI Detection Results", use_column_width=True)
        
        # 2. MACROS & CALORIES
        total_cals = data.get('total_calories', 0)
        
        # Calculate total macros from list
        total_protein = sum(item.get('protein', 0) for item in data.get('foods', []))
        total_carbs = sum(item.get('carbs', 0) for item in data.get('foods', []))
        total_fat = sum(item.get('fat', 0) for item in data.get('foods', []))
        
        # Display Key Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Calories", f"{total_cals} kcal")
        m2.metric("Protein", f"{total_protein}g")
        m3.metric("Carbs", f"{total_carbs}g")
        m4.metric("Fat", f"{total_fat}g")
        
        # 3. CHARTS
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_macros(total_protein, total_carbs, total_fat), use_container_width=True)
        with c2:
            st.plotly_chart(plot_calories_gauge(total_cals, user_profile['target_calories'] / 3), use_container_width=True)
        
        # 4. FOOD ITEM BREAKDOWN
        st.divider()
        st.subheader("Item Breakdown")
        for item in data.get('foods', []):
            with st.expander(f"📍 {item['name']} ({item.get('weight_g', 0)}g)"):
                st.write(f"**Calories:** {item.get('calories')} | **P:** {item.get('protein')}g | **C:** {item.get('carbs')}g | **F:** {item.get('fat')}g")
        
        # 5. HEALTH TIP
        if data.get('health_tip'):
            st.info(f"💡 **AI Tip:** {data['health_tip']}")

    else:
        st.info("Upload an image and click Analyze to see results here.")