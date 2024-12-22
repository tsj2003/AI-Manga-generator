import streamlit as st
import requests

# Replace with your actual tokens
PHI3_TOKEN = "AEulafWZQ1xhIkeLgjcp5nhL7d0cLPWiXAU34DTVvXI"  
FLUX_TOKEN = "calm-bold-tree-bd1b1c8bc141403231e7f0a8"  
PHI3_URL = "https://cu-vertical-dimensional-continuity.trycloudflare.com/phi3/generate"
FLUX_URL = "https://maintained-thai-filter-four.trycloudflare.com/imagine/generate"

# Custom CSS for background color
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f0f5;  /* Change this to your desired background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add Intel Hackathon logo

def generate_story_outline(prompt):
    headers = {
        "Authorization": f"Bearer {PHI3_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": f"<|system|>\nYou are a creative manga story writer.<|end|>\n<|user|>\n{prompt}<|end|>\n<|assistant|>",
        "parameters": {"max_new_tokens": 300}
    }
    response = requests.post(PHI3_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("generated_text", "").split("\n")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return []

def generate_image(description):
    headers = {
        "Authorization": f"Bearer {FLUX_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": description[:200],  # Max 200 characters for prompt
        "img_size": 512,
        "guidance_scale": 7.5,
        "num_inference_steps": 50
    }
    response = requests.post(FLUX_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Streamlit UI
st.title("AI Manga Generator")
st.write("Enter a prompt to generate a manga story and images.")

# This text area allows users to input any prompt they want
prompt = st.text_area("Story Prompt", "Enter your story prompt here...")  # Updated placeholder text

if st.button("Generate"):
    with st.spinner("Generating story outline..."):
        story_outline = generate_story_outline(prompt)

    if story_outline:
        st.write("### Story Outline:")
        for i, scene in enumerate(story_outline):
            if scene.strip():
                st.write(f"**Scene {i + 1}:** {scene}")
                image_data = generate_image(scene)
                if image_data:
                    st.image(image_data, caption=f"Scene {i + 1}", use_container_width=True)
            else:
                st.write(f"**Scene {i + 1}:** ")