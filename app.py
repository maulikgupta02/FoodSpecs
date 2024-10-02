import streamlit as st
import requests
from PIL import Image
import io

# Define the API URL
API_URL = "http://localhost:5000"  # Change this to your Flask API URL if it's different

def fetch_product_info(ingredients):
    response = requests.get(f"{API_URL}/product_info", params={"ingredients": ingredients})
    return response.json()

def fetch_claim_check(ingredients, claim):
    response = requests.get(f"{API_URL}/claim_check", params={"ingredients": ingredients, "claim": claim})
    return response.json()

def fetch_diet_compliance(ingredients, diet):
    response = requests.get(f"{API_URL}/diet_compliance", params={"ingredients": ingredients, "diet": diet})
    return response.json()


# Streamlit application layout
st.title("Packaged Food Insights")

st.sidebar.header("Input Parameters")

# Input for ingredients
ingredients_input = st.sidebar.text_area("Enter Ingredients (comma-separated)", "water, sugar, salt")

# Section for Product Information
if st.sidebar.button("Get Product Info"):
    with st.spinner("Fetching product information..."):
        product_info = fetch_product_info(ingredients_input)
        st.success("Product Information Retrieved")
        st.json(product_info)

# Section for Claim Check
claim_input = st.sidebar.text_input("Enter Claim", "Is this product gluten-free?")
if st.sidebar.button("Check Claim"):
    with st.spinner("Checking claim..."):
        claim_info = fetch_claim_check(ingredients_input, claim_input)
        st.success("Claim Check Complete")
        st.json(claim_info)

# Section for Diet Compliance
diet_input = st.sidebar.text_input("Enter Diet Type", "vegan")
if st.sidebar.button("Check Diet Compliance"):
    with st.spinner("Checking diet compliance..."):
        diet_info = fetch_diet_compliance(ingredients_input, diet_input)
        st.success("Diet Compliance Checked")
        st.text(diet_info)



st.sidebar.markdown("""
    ### About
    AI-enabled smart label reader that helps consumers understand the health impact of packaged food products and nudges them to make better choices.
""")
