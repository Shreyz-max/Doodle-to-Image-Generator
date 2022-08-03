import os.path

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import test
from PIL import Image
import gdown


st.set_page_config(layout="wide")

# Specify canvas parameters in application
drawing_object = st.sidebar.selectbox(
    "Object:", ("sea", "cloud", "bush", "grass", "mountain", "sky", "snow",
                "tree", "flower", "road")
)
drawing_object_dict = {"sea": "rgb(56,79,131)", "cloud": "rgb(239,239,239)",
                       "bush": "rgb(93,110,50)", "grass": "rgb(183,210,78)",
                       "mountain": "rgb(60,59,75)", "snow": "rgb(250,250,250)",
                       "sky": "rgb(117,158,223)", "tree": "rgb(53, 38, 19)",
                       "flower": "rgb(230,112,182)",
                       "road": "rgb(152, 126, 106)"}

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)

stroke_color = drawing_object_dict[drawing_object]


col1, col2 = st.columns(2)
with col1:
    # Create a canvas component with different parameters
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="rgb(117,158,223)",
        background_image=None,
        height=512,
        width=512,
        drawing_mode="freedraw",
        point_display_radius=0,
        key="canvas",
    )
    if canvas_result.image_data is not None:
        pass


@st.cache
def download_model():
    f_checkpoint = os.path.join("latest_net_G.pth")
    if not os.path.exists(f_checkpoint):
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            url = 'https://drive.google.com/uc?id=15VSa2m2F6Ch0NpewDR7mkKAcXlMgDi5F'
            output = 'latest_net_G.pth'
            gdown.download(url, output, quiet=False)


if st.button('generate'):
    download_model()
    image = Image.fromarray(canvas_result.image_data)
    s = test.semantic(image)
    image = test.evaluate(s)
    image = test.to_image(image)
    with col2:
        st.image(image, clamp=True, width=512)


st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 120px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
