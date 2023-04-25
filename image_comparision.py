import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import numpy as np

def load_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

def resize_images(image1, image2):
    size = (min(image1.width, image2.width), min(image1.height, image2.height))
    return image1.resize(size), image2.resize(size)

def compare_images(image1, image2):
    # Convert the images to NumPy arrays
    array1 = np.array(image1)
    array2 = np.array(image2)
    
    # Compute the difference between the two images
    diff = np.abs(array1 - array2)
    diff = np.sum(diff, axis=2) / 3  # Convert RGB to grayscale
    
    # Threshold the difference image to highlight the pixels that differ
    threshold = 50  # Adjust this value to change the sensitivity of the comparison
    mask = diff > threshold
    mask = mask.astype(np.uint8) * 255
    
    # Create a composite image showing the two original images and the difference mask
    height, width, _ = array1.shape
    composite = np.zeros((height, width*3, 3), dtype=np.uint8)
    composite[:, :width, :] = array1
    composite[:, width:2*width, :] = array2
    composite[:, 2*width:, :] = np.stack([mask]*3, axis=2)
    
    return Image.fromarray(composite)

st.title('Image Comparison')
st.write('Enter the URLs for the two images you want to compare:')
image_url1 = st.text_input('Enter Image URL 1')
image_url2 = st.text_input('Enter Image URL 2')

if image_url1 and image_url2:
    image1 = load_image(image_url1)
    image2 = load_image(image_url2)
    image1, image2 = resize_images(image1, image2)

if image_url1 and image_url2:
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, use_column_width=True)
    with col2:
        st.image(image2, use_column_width=True)

compare_button = st.button('Compare Images')

if compare_button:
    if image_url1 and image_url2:
        comparison = compare_images(image1, image2)
        if np.array_equal(np.array(image1), np.array(image2)):
            st.success("Same images")
        else:
            st.warning("Not same images")