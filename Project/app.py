from PIL import Image
import streamlit as st
from database import *
from model import *

db = Init()
embedding_model = init_emb()



selection = st.selectbox("Please choose functions", ["Find", "Add", "Edit", "Remove"])


if selection == "Find":

    input_img = Get_image()

    if input_img is not None:
        for img in pipeline(db, embedding_model, input_img, 20):
            st.image(img, width = 250)
