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
    html, body, [class*="css"]  {font-family: 'Roboto', sans-serif;}
    .reportview-container, .css-18e3th9 { background-color: #000; color: #fff; }
    /* Generate button styling */
    .stButton>button {
        background-color: #FF7700;
        color: #000;
        border: 2px solid #00FFCC;
        border-radius: 16px;
        padding: 1em 2em;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.6);
    }
    /* Remove default hover change */
    .stButton>button:hover {
        background-color: #FF7700;
        border-color: #00FFCC;
    }
    /* Share button styling */
    .share-button {
        background-color: #00FFCC;
        color: #000;
        border: none;
        border-radius: 12px;
        padding: 0.8em 1.8em;
        font-size: 1.1em;
        margin-top: 1em;
    }
    .share-button:active { opacity: 0.8; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Prompt Template ----------
# (BASE_PROMPT remains unchanged)
# ... [omitted for brevity] ...

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

# Note: Keep BASE_PROMPT defined above exactly as before, including the reference meal list.
