import numpy as np
import gradio as gr
from PIL import Image
from lib.utils import *


def crop_image(image):
    img = image["composite"]
    roi = get_roi(img)
    return roi


if __name__ == "__main__":
    demo = gr.Interface(
        fn=crop_image,
        inputs=gr.ImageEditor(interactive=True, sources=["upload"], type="numpy", image_mode="RGB"),
        outputs=gr.Image(),
        allow_flagging="never"
    )
    demo.launch(show_api=True)
