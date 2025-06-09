import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import random

# ---------- Streamlit Page Configuration ----------
st.set_page_config(page_title="Meal Planner", layout="wide")

# ---------- Configuration ----------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY environment variable not found. Please set it in Streamlit Secrets.")
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

# ---------- Base Prompt ----------
BASE_PROMPT = "<FULL_PROMPT_WITH_REFERENCE_MEALS>"

# ---------- Layout ----------
# Import Tailwind CSS via HTML component
tailwind = '''<script src="https://cdn.tailwindcss.com"></script>'''
st.markdown(tailwind, unsafe_allow_html=True)

# Header
with st.container():
    c1, c2 = st.columns([8,1])
    with c1:
        st.markdown("<h2 class='text-lg font-bold text-gray-900 text-center'>Meal Planner</h2>", unsafe_allow_html=True)
    with c2:
        if st.button("<svg xmlns='http://www.w3.org/2000/svg' class='h-6 w-6 text-gray-900' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path d='M12 . . .'/></svg>", key='share_top', help='Share'):
            st.write('Sharing is not supported.')

# "This Week" Section
title = st.markdown("<h2 class='text-2xl font-bold text-gray-900 px-4'>This Week</h2>", unsafe_allow_html=True)
with st.container():
    img_url = "https://..."
    col1, col2 = st.columns([3,2])
    col1.markdown(f"<div class='aspect-video bg-cover rounded-xl' style='background-image:url({img_url});'></div>", unsafe_allow_html=True)
    col2.markdown(
        """
        <p class='text-xl font-bold'>Family Meal Plan</p>
        <p class='text-green-600'>A balanced and delicious meal plan for the whole family.</p>
        <p class='text-green-600'>7 recipes</p>
        """, unsafe_allow_html=True)

# Generate Button
generate_clicked = st.button("Generate New Plan", key='generate', help='Click to generate a new weekly plan')
if generate_clicked:
    response = client.chat.completions.create(
        model="o3",
        messages=[{"role":"system","content":BASE_PROMPT}],
    )
    plan = response.choices[0].message.content
    st.markdown("---")
    st.markdown("### Your 7-Day Meal Plan")
    st.markdown(plan, unsafe_allow_html=True)
    slogan = random.choice(slogans)
    st.markdown(f"**{slogan}**")

# Share Section
st.markdown("<h2 class='text-2xl font-bold px-4 pt-5'>Share</h2>", unsafe_allow_html=True)
with st.container():
    if st.button("Share with Friends & Family", key='share_bottom'):
        st.write("Sharing not supported on this platform.")

# Bottom Navigation
nav = st.container()
with nav:
    cols = st.columns(5)
    icons = ['House','BookOpen','Calendar','ListBullets','User']
    labels = ['Home','Recipes','Meal Plan','Grocery List','Profile']
    for col, icon, label in zip(cols, icons, labels):
        col.markdown(f"<div class='flex flex-col items-center'><svg class='h-6 w-6 text-green-600'></svg><p class='text-xs text-green-600'>{label}</p></div>", unsafe_allow_html=True)
