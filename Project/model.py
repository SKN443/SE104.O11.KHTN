from imgbeddings import imgbeddings
from PIL import Image
from database import *
import io
import streamlit as st


@st.cache_resource
class Image_embedding:
    def __int__(self):
        self.embedding_model = imgbeddings()

    def get_emb(self, img):
        if type(img) == str:
            img = Image.open(img)
        embedding = self.embedding_model.to_embeddings(img).flatten().tolist()
        return embedding

def byte2img(img):
    pil_img = Image.open(io.BytesIO(img))
    return pil_img

def img2byte(img):
    image_bytes = io.BytesIO()
    img.save(image_bytes, format='JPEG')
    return image_bytes.getvalue()


def pipeline(db, embeding_model, img, limit):
    '''
    inp:
    - img: an image (PIL image) or path to image
    - limit: number of images return
    out:
    - list of images
    '''
    emb = embeding_model.get_emb(img)
    dcts = db.query(emb, limit)
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

def Get_image():

    image_file = st.file_uploader("Upload Images",type=["png", "jpg", "jpeg"])
    img = None
    save_dir = None

    if image_file is not None:
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


def Exist(db, product_id):
        return db.check_exist(product_id=product_id)

def Add_product(db, input_img, product_id, category, embedding_model):
    vector = embedding_model.get_emb(img = input_img)
    db.insert(product_id= product_id, image= input_img, vector = vector, category= category)


def Update(db, product_id, input_img, category, embedding_model):
    vector = None
    if input_img is not None:
        vector = embedding_model.get_emb(img = input_img)
    db.update(product_id,input_img,vector,category)

def Delete(db, product_id):
    db.erase(product_id)

def Get(db, product_id):
    raw_result = db.find(product_id)
    result ={
        'image': byte2img(raw_result['image']),
        'product_id': raw_result['product_id'],
        'category': raw_result['category']
    }
    return result