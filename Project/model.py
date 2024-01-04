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
    dcts = list(dcts)
    #st.text(dcts[0].keys())
    for dct in dcts:
        dct['image'] = byte2img(dct['image'])
        for key in ['vector', '_id', 'flag', 'path']:
          dct.pop(key, None)
    return dcts


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


def Exist(db, product_id):
        return check_exist(db, product_id)

def Add_product(db, input_img, product_id, category, embedding_model):
    vector = get_emb(model = embedding_model, img = input_img)
    insert(db = db, product_id= product_id, image= input_img, vector = vector, category= category)


def Update(db, product_id, input_img, category, embedding_model):
    vector = None
    if input_img is not None:
        vector = get_emb(model = embedding_model, img = input_img)
    update(db,product_id,input_img,vector,category)

def Delete(db, product_id):
    erase(db, product_id)

def Get(db, product_id):
    raw_result = find(db, product_id)
    result ={
        'image': byte2img(raw_result['image']),
        'product_id': raw_result['product_id'],
        'category': raw_result['category']
    }
    return result