import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import random

# ---------- Streamlit Page Configuration ----------
st.set_page_config(page_title="Weekly Dinner Plan Generator", page_icon="🍲")

# ---------- Configuration ----------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY environment variable not found. Please set it in your environment or in Streamlit Secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ---------- Slogans ----------
slogans = [
    "Turning veggies into giggles!",
    "Because cereal can't be dinner. 😉",
    "Your toddler-approved gourmet gambit!",
    "Meal planning: downgraded to pure delight.",
    "Where goat cheese dreams come true!",
]

# ---------- Custom Styles ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
    .reportview-container, .css-18e3th9 { background-color: #000; color: #fff; }
    .stButton>button { background-color: #FF7700; color: #000; border: 2px solid #00FFCC; border-radius: 16px; padding: 1em 2em; font-size: 1.2em; font-weight: bold; box-shadow: 3px 3px 8px rgba(0,0,0,0.6); }
    .stButton>button:hover { background-color: #FF7700; border-color: #00FFCC; }
    .share-button { background-color: #00FFCC; color: #000; border: none; border-radius: 12px; padding: 0.8em 1.8em; font-size: 1.1em; margin-top: 1em; }
    .share-button:active { opacity: 0.8; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Prompt Template ----------
BASE_PROMPT = """
You are my personal AI meal-planning assistant. You are a world-renowned planner and family cook with years of expertise in family cooking.

Your weekly task is to generate a rotating 7-day dinner plan, custom-built for a specific household, based on the following detailed preferences and constraints:

=== FAMILY PROFILE ===
• Household size: 3 people (2 adults + 1 toddler, aged 2).
• Food preferences:
  - Enjoy meals inspired by Mexican, Italian, vegetarian, and classic pub-style fare, but also open to other ideas.
  - Meals must be toddler-friendly (low spice, no strong heat).
  - Comfort food is welcome; health-conscious but flexible.
  - Include 1 vegetarian meal every other week.
• Food restrictions:
  - No seafood or fish meat, but fish-derived products are ok.
  - Dairy is acceptable except cow’s milk (goat and sheep milk products OK).
  - No deep-fried meals.
• Cook + prep time per meal: ≤ 45 minutes.

=== KITCHEN EQUIPMENT AVAILABLE ===
• Air fryer (must be used in at least 2 meals per week).
• Microwave
• Conventional oven
• Kettle
• Blender
• Slow cooker (must be eaten on a Tuesday, Wednesday, Thursday, or Friday—label accordingly)

=== INGREDIENT GUIDELINES ===
• Use ingredients commonly available in Australian supermarkets (e.g., Coles, Woolworths).
• Avoid overly exotic or hard-to-find items.
• Reuse ingredients across meals to minimize waste.
• Focus on simplicity and family appeal over trendiness.

=== INSPIRATION MEALS (REFERENCE ONLY) ===
You may use the following list as a guide for meal types, but do NOT limit suggestions to just these:

50 Healthy, Protein-Forward Dinner Ideas
• Chicken and Veggie Curry
• Beef and Sweet Potato Shepherd’s Pie
• Lentil and Spinach Tomato Pasta
• Egg and Veggie Fried Rice
• Slow Cooker Lamb and Root Veg Stew
• Chicken Alfredo Pasta with Goat Cheese
• Chickpea and Veggie Quesadillas
• Turkey Meatball Marinara Rice Bowl
• Beef and Broccoli Stir-Fry
• Pumpkin and Black Bean Chili
• Air-Fryer Chicken Parmesan
• Beef Lasagna with Ricotta and Spinach
• Veggie Omelette with Goat Cheese
• Lamb Kofta with Rice and Cucumber Yogurt
• Black Bean Burrito Bowls
• Chicken and Vegetable Stir-Fry Noodles
• Beef Stuffed Bell Peppers
• Lentil and Carrot Cottage Pie
• Chicken and Corn Chowder
• Eggplant and Chickpea Masala
• Beef Taco Rice Skillet
• Chicken and Brown Rice Pilaf
• Butter Chicken with Sweet Peas
• Spinach and Ricotta Stuffed Pasta Shells
• Bone Broth Beef and Vegetable Soup
• Pumpkin Mac and Cheese with Chickpea Pasta
• Chicken and Veggie Skewers with Rice
• Beef Stroganoff with Mushrooms
• Quinoa, Black Bean, and Corn Salad
• Chicken and Broccoli Alfredo Bake
• Slow Cooker Beef and Lentil Stew
• Veggie Loaded Frittata
• BBQ Chicken Drumsticks with Roast Veggies
• Beef and Kidney Bean Taco Bake
• Chickpea and Vegetable Tagine with Couscous
• Pasta e Fagioli
• Baked Turkey and Sweet Potato Meatballs
• Chicken and Spinach Risotto
• Beef and Vegetable Goulash
• Lentil Sloppy Joes on Wholemeal Rolls
• Chicken Tikka Masala with Rice
• Shepherd’s Pie with Lentils and Beef
• Broccoli and Cheddar Egg Muffins
• Beef and Vegetable Ragu over Polenta
• Chicken Noodle Stir-Fry with Snow Peas
• Red Lentil Dahl with Rice
• Beef and Pumpkin Curry
• Chicken and Black Bean Enchiladas
• Pasta Primavera with Goat Cheese
• Baked Falafel Pitas with Hummus

=== OUTPUT FORMAT ===
Return ONLY the following Markdown table. Do NOT include any introductions or additional text:

| Day       | Dish Name (with labels)             | Ingredients (bullet list only)             |
|-----------|--------------------------------------|---------------------------------------------|
| Monday    | …                                    | • …                                          |
| Tuesday   | …                                    | • …                                          |
| Wednesday | …                                    | • …                                          |
| Thursday  | …                                    | • …                                          |
| Friday    | …                                    | • …                                          |
| Saturday  | …                                    | • …                                          |
| Sunday    | …                                    | • …                                          |

=== RULES ===
1. Tag slow cooker meals with “(SC)” and air fryer meals with “(AF)” in the Dish Name column.
2. Ingredients lists should be concise—just the essentials.
3. Do NOT repeat any main dish within a rolling 4-week cycle.
4. Use a variety of cooking methods throughout the week.
5. Focus only on evening dinners (no breakfast, lunch, or snacks).
6. All meals must be toddler-friendly.
7. Do NOT generate anything beyond the Markdown table above.

Generate a fresh and unique meal plan each time, drawing inspiration from—but not limited to—the list above.
"""

# ---------- Streamlit UI ----------
st.title("Weekly Dinner Plan Generator")

with st.expander("🔧 Adjust Prompt (optional)"):
    user_prompt = st.text_area("Prompt Text:", BASE_PROMPT, height=600)

if st.button("Generate Meal Plan"):
    with st.spinner("Cooking up your plan..."):
        response = client.chat.completions.create(
            model="o3",
            messages=[{"role": "system", "content": user_prompt}],
        )
        plan = response.choices[0].message.content

    st.markdown("---")
    st.markdown("### Your 7-Day Meal Plan")
    st.markdown(plan, unsafe_allow_html=True)
    st.success("Done! Feel free to copy or tweak the plan.")

    # Display a rotating slogan
    slogan = random.choice(slogans)
    st.markdown(f"**{slogan}**")

    # Mobile-friendly Share button using Web Share API
    share_html = f"""
    <button class='share-button' onclick="
      if (navigator.share) {{
        navigator.share({{ title: 'My Weekly Meal Plan', text: 'Check out my AI-generated meal plan!', url: window.location.href }});
      }} else {{
        alert('Sharing not supported on this browser.');
      }}
    ">Share Your Plan</button>
    """
    st.components.v1.html(share_html, height=80)
