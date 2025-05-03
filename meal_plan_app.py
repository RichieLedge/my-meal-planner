import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Configuration ----------
load_dotenv()  # Load environment variables from a .env file, if present
api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set via .streamlit/secrets.toml or your environment

if not api_key:
    st.error("OPENAI_API_KEY environment variable not found. Please set it in your environment or in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------- Custom Styles ----------
st.markdown(
    """
    <style>
    /* Page background and text colors */
    .reportview-container, .css-18e3th9 {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Button styling */
    .stButton>button {
        background-color: #FF7700;
        color: #000000;
        border: 2px solid #00FFCC; /* hyper teal accent */
        border-radius: 12px;
        padding: 0.5em 1.5em;
        font-size: 1.1em;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    }
    .stButton>button:hover {
        background-color: #FF8A33;
        border-color: #00E6B8;
    }
    /* Expander header color */
    .css-1v3fvcr {
        background-color: #1A1A1A;
        color: #FF7700;
    }
    /* Link colors */
    a {
        color: #00FFCC;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Prompt Template ----------
BASE_PROMPT = """You are my personal AI meal-planning assistant. Your are a world renowned planner and family Cook with years of Expertise and experience in family cooking.

Your weekly task is to generate a rotating 7-day dinner plan, custom-built for a specific household, based on the following detailed preferences and constraints:

=== FAMILY PROFILE ===
• Household size: 3 people (2 adults + 1 toddler, aged 2).
• Food preferences:
  - Enjoy meals inspired by the following cuisines: Mexican, Italian, vegetarian, and classic pub-style fare. But also open to other ideas
  - Meals must be toddler-friendly (low spice, no strong heat).
  - Comfort food welcome; health-conscious but flexible.
  - Include 1 vegetarian meal every other week.
• Food restrictions:
  - No seafood or fish meat but fish derived products are ok.
  - Dairy is acceptable **except cow’s milk**. Goat and sheep milk products are fine (e.g., goat cheese, sheep yogurt).
  - No deep-fried meals.
• Cook + prep time per meal: 45 minutes maximum.

=== KITCHEN EQUIPMENT AVAILABLE ===
• Air fryer (must be used in at least 2 meals per week).
• Microwave
• Conventional oven
• Kettle
• Blender
• Slow cooker (must be eaten on a Tuesday, Wednesday, Thursday or Friday—label accordingly)

=== INGREDIENT GUIDELINES ===
• Use ingredients commonly available in Australian supermarkets (e.g., Coles, Woolworths).
• Avoid overly exotic ingredients or hard-to-find products.
• Reuse ingredients across meals where practical to minimize waste.
• Focus on simplicity and family appeal over trendiness or novelty.

=== OUTPUT FORMAT ===
Return ONLY the following Markdown table. Do not include any introductions, nutritional data, recipe steps, or additional text. Just the structured table.

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
2. Ingredient lists should be short and practical—just the essentials needed to prepare each dish.
3. Do not repeat any main dish within a rolling 4-week cycle.
4. Use a variety of cooking methods across the week.
5. Focus only on **evening dinners** (no breakfast, lunch, or snacks).
6. The toddler must be able to eat all meals with minimal adjustments.
7. Do not generate anything beyond the Markdown table described.

Each time this prompt is run, generate a fresh and unique meal plan following the above instructions."""

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Weekly Dinner Plan Generator", page_icon="🍲")
st.title("Weekly Dinner Plan Generator")

with st.expander("🔧 Adjust Prompt (optional)"):
    user_prompt = st.text_area("Prompt Text:", BASE_PROMPT, height=500)

if st.button("Generate Meal Plan"):
    with st.spinner("Cooking up your plan..."):
        response = client.chat.completions.create(
            model="o3",
            messages=[{"role": "system", "content": user_prompt}],
        )
        plan = response.choices[0].message.content

    st.markdown("---")
    st.markdown("### Your 7‑Day Meal Plan")
    st.markdown(plan, unsafe_allow_html=True)
    st.success("Done! Feel free to copy or tweak the plan.")
