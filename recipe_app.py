import streamlit as st
import re

# --- Parsing Functions (These break down your pasted text) ---
def parse_ingredients(text):
    ingredients = []
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'^(\d+\.?\d*)\s*([a-zA-Z]+)?\s*(.*)', line)

        quantity_str = None
        unit_str = None
        name_str = line 

        if match:
            quantity_str = match.group(1)
            unit_str = match.group(2) if match.group(2) else ""
            name_str = match.group(3).strip()

            try:
                quantity_float = float(quantity_str)
            except ValueError:
                quantity_float = None

            ingredients.append({
                "original": line,
                "quantity": quantity_float,
                "unit": unit_str if unit_str else None,
                "name": name_str if name_str else line
            })
        else:
            ingredients.append({
                "original": line,
                "quantity": None,
                "unit": None,
                "name": line
            })
    return ingredients

def parse_instructions(text):
    instructions = []
    lines = text.strip().split('\n')
    step_number = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r'^\s*\d+[\.\-\)]?\s*', '', line).strip()
        if line:
            instructions.append(f"{step_number}. {line}")
            step_number += 1
    return instructions

# --- Streamlit UI Code (This designs how your app looks) ---

st.set_page_config(
    page_title="Recipe Card Formatter",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for colors, fonts, and card styling
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8F8F8; /* Very light grey for the overall background */
        font-family: 'Montserrat', sans-serif;
        color: #333;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        color: #4A4A4A; /* Darker grey for headings */
    }
    .main-header {
        font-size: 3em;
        color: #FF6347; /* Tomato Red for main title */
        text-align: center;
        margin-bottom: 0.5em;
        font-weight: 700;
    }
    .subheader {
        color: #555;
        text-align: center;
        margin-bottom: 2em;
    }
    .stButton>button {
        background-color: #6A5ACD; /* Medium Slate Blue for button */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 1.1em;
        transition: background-color 0.3s ease;
        width: 100%;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #483D8B; /* Darker blue on hover */
    }
    .input-container {
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        background-color: white; /* Input container is white */
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .recipe-card {
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        color: #333;
        font-weight: 400;
        line-height: 1.6;
    }
    .ingredients-card {
        background-color: #FFEDD5; /* Soft Peach */
    }
    .instructions-card {
        background-color: #E0F2F7; /* Light Cyan/Teal */
    }
    .card-header {
        font-size: 1.5em;
        font-weight: 700;
        margin-bottom: 15px;
        color: #333;
    }
    .ingredient-item {
        margin-bottom: 5px;
    }
    .instruction-item {
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='main-header'>✨ Recipe Card Designer ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Paste your recipe details and see them transformed into beautiful cards!</p>", unsafe_allow_html=True)

# Input Section Container
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    st.subheader("📝 Input Your Recipe Details")

    recipe_title = st.text_input("**Recipe Title:**", "My Gourmet Creation 🍽️")

    col1, col2 = st.columns(2)
    with col1:
        ingredients_text = st.text_area("**Paste Ingredients (one per line):**", height=250, 
                                        placeholder="e.g.,\n1.5 cups all-purpose flour\n2 large eggs\n1/2 tsp fine sea salt")
    with col2:
        instructions_text = st.text_area("**Paste Instructions (one per line):**", height=250, 
                                        placeholder="e.g.,\n1. Preheat oven to 375°F (190°C).\n2. In a large bowl, whisk together flour and salt.")
    st.markdown("</div>", unsafe_allow_html=True) # Close input-container

st.markdown("---") # Visual separator

# Process and Display button
if st.button("✨ Design My Recipe Cards! ✨"):
    if not ingredients_text and not instructions_text:
        st.warning("Please paste some ingredients or instructions to format! 🧐")
    else:
        st.header(f"✨ Recipe Cards for: {recipe_title}")
        st.markdown("---")

        # Create two columns for the output cards
        output_col1, output_col2 = st.columns(2)

        with output_col1:
            st.markdown("<div class='recipe-card ingredients-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-header'>🛒 Ingredients</h3>", unsafe_allow_html=True)
            parsed_ingredients = parse_ingredients(ingredients_text)
            if not parsed_ingredients:
                st.info("No ingredients provided.")
            else:
                ingredients_markdown = ""
                for item in parsed_ingredients:
                    if item["quantity"] is not None and item["unit"]:
                        ingredients_markdown += f"<div class='ingredient-item'>- **{item['quantity']} {item['unit']}** {item['name']}</div>\n"
                    elif item["quantity"] is not None:
                        ingredients_markdown += f"<div class='ingredient-item'>- **{item['quantity']}** {item['name']}</div>\n"
                    else:
                        ingredients_markdown += f"<div class='ingredient-item'>- {item['name']}</div>\n"
                st.markdown(ingredients_markdown, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True) # Close ingredients-card

        with output_col2:
            st.markdown("<div class='recipe-card instructions-card'>", unsafe_allow_html=True)
            st.markdown("<h3 class='card-header'>🧑‍🍳 Instructions</h3>", unsafe_allow_html=True)
            parsed_instructions = parse_instructions(instructions_text)
            if not parsed_instructions:
                st.info("No instructions provided.")
            else:
                instructions_markdown = ""
                for step in parsed_instructions:
                    instructions_markdown += f"<div class='instruction-item'>{step}</div>\n"
                st.markdown(instructions_markdown, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True) # Close instructions-card

        st.markdown("---")
        st.success("🎉 Your recipe cards are ready! Enjoy your culinary journey!")

st.markdown("---")
st.caption("✨ Crafted with love and Streamlit by your AI Assistant ✨")
