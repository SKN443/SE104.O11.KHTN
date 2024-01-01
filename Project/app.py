from PIL import Image
import streamlit as st
from database import *
from model import *

def load_image(image_file):
	img = Image.open(image_file)
	return img

def Get_image():

    image_file = st.file_uploader("Upload Images",
                                  type=["png", "jpg", "jpeg"])
    img = None
    if image_file is not None:
        # TO See details
        file_details = {"filename": image_file.name, "filetype": image_file.type,
                        "filesize": image_file.size}
        st.write(file_details)
        img = load_image(image_file)
        st.image(img, width=250)

        from datetime import datetime
        now = datetime.now()
        save_dir = 'storage/' + now.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg'
        # Saving upload
        img = img.convert('RGB')
        img.save(save_dir)

        st.success("File Saved")
    return img

db = Init()

input_img = Get_image()

for img in pipeline(db, input_img, 20):
    st.image(img, width = 250)