from imgbeddings import imgbeddings
from PIL import Image
from database import *
import io
import streamlit as st


@st.cache_resource
def init_emb():
    embedding_model = imgbeddings()
    return embedding_model

def get_emb(model, img):
    if type(img) == str:
        img = Image.open(img)
    embedding = model.to_embeddings(img).flatten().tolist()
    return embedding

def byte2img(img):
    pil_img = Image.open(io.BytesIO(img))
    return pil_img

def pipeline(db, embeding_model, img, limit):
    '''
    inp:
    - img: an image (PIL image) or path to image
    - limit: number of images return
    out:
    - list of images
    '''
    emb = get_emb(embeding_model, img)
    dcts = query(db, emb, limit)
    return_imgs = [byte2img(dct['image']) for dct in dcts]
    return return_imgs


def load_image(image_file):
	img = Image.open(image_file)
	return img

def Get_image(get_dir = False):

    image_file = st.file_uploader("Upload Images",
                                  type=["png", "jpg", "jpeg"])
    img = None

    save_dir = None

    if image_file is not None:
        # TO See details
        file_details = {"filename": image_file.name, "filetype": image_file.type,
                        "filesize": image_file.size}
        #st.write(file_details)
        img = load_image(image_file)
        st.image(img, width=250)

        from datetime import datetime
        now = datetime.now()
        save_dir = 'storage/' + now.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg'
        # Saving upload
        img = img.convert('RGB')
        img.save(save_dir)

        st.success("File Saved")

    if get_dir == False:
        return img
    else:
        return save_dir