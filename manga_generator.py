import requests
from PIL import Image, ImageDraw, ImageFont

# Replace with your actual tokens
PHI3_TOKEN = "AEulafWZQ1xhIkeLgjcp5nhL7d0cLPWiXAU34DTVvXI"  
FLUX_TOKEN = "calm-bold-tree-bd1b1c8bc141403231e7f0a8"  
PHI3_URL = "https://cu-vertical-dimensional-continuity.trycloudflare.com/phi3/generate"
FLUX_URL = "https://maintained-thai-filter-four.trycloudflare.com/imagine/generate"

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
        print(f"Error: {response.status_code}, {response.text}")
        return []

def generate_image(description, output_file):
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
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Image saved to {output_file}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def create_manga_page(image_file, text):
    img = Image.open(image_file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), text, fill="white", font=font)
    img.save(f"final_{image_file}")

# Example usage
prompt = "A doggy detective discovers they have supernatural abilities while navigating a noir-inspired world of secrets, danger, and high-stakes mysteries in a rain-soaked city"
story_outline = generate_story_outline(prompt)

# Generate images for each scene
for i, scene in enumerate(story_outline):
    if scene.strip():  # Check if the scene is not empty
        generate_image(scene, f"scene_{i + 1}.png")
    else:
        print(f"Skipping empty scene at index {i}.")

# Create final pages
for i in range(len(story_outline)):
    if story_outline[i].strip():  # Check if the scene is not empty
        create_manga_page(f"scene_{i + 1}.png", story_outline[i])