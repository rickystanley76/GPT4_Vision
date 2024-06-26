import streamlit as st
import requests
import base64
from PIL import Image

# Function to encode the image to base64
def encode_image(image_file):
    _, image_extension = image_file.name.split('.')
    prefix = f"data:image/{image_extension};base64,"
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    return prefix + base64_image

# Streamlit App
st.set_page_config(page_title="Image Content Description with Artificial Intelligence", layout="centered", page_icon=":glass:")

# Load the image
img = Image.open('SmartSearchAI.png')
st.image(img, width=300)

st.subheader("Image Content Description with Artificial Intelligence")


st.info('''Sometimes we have complicated images, like doctors report, technical diagram, flowchart or just an beatiful picture of a nature or city,
            we would like to know more about explannation of image. 
            This Application will just help you with that using the Vision Model of GPT4.
           ''' )

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Your OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

if uploaded_file is not None and api_key:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Encode the uploaded image
    base64_image = encode_image(uploaded_file)

    # Setup the request headers and payload
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the image in detials but using 500 tokens max and in simple English and avoid the technical jargon.."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    # Send the request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response
        response_data = response.json()
        # Assuming the response contains the description in the expected format
        if "choices" in response_data and len(response_data["choices"]) > 0:
            description = response_data["choices"][0].get("message", {}).get("content", "No description found.")
            st.write("Description:", description)
        else:
            st.error("Failed to get a description from the API.")
    else:
        st.error("Error in API response. Status code: " + str(response.status_code))
