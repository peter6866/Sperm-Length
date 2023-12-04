import numpy as np
import gradio as gr
from PIL import Image
from lib.utils import *
from lib.utils_thinning import *
from lib.utils_morphology import *


def crop_image(image, thr):
    ori_img = image["composite"]
    back_img = np.array(Image.fromarray(image["background"]).resize((1024, 1024)))
    temp = back_img.copy()

    roi = get_roi(ori_img)
    img = Image.fromarray(roi).convert("L")
    img_reshaped = np.array(img.resize((1024, 1024)))
    threshold_img = threshold(img_reshaped, thr)

    # get largest components
    res = getKLargestComponents(threshold_img, 2, 0)

    # close image
    res = close_img(res, 1)

    # build cell complex
    cc = buildCC2D(res)

    # thinning
    thined = thin(cc, [[150, 0.8]])

    for i in cc[0]:
        temp[int(i[1]), int(i[0])] = np.array([255, 0, 0])

    val = len(thined[0]) / 3.06
    val = 0.8698 * val + 610.2

    return temp, "Cell length: " + str(round(val, 2)) + "mm"


if __name__ == "__main__":
    demo = gr.Interface(
        fn=crop_image,
        inputs=[
            gr.ImageEditor(interactive=True, sources=["upload"], type="numpy", image_mode="RGB"),
            gr.Slider(0, 255, value=150, step=1, label="Threshold", info="Choose between 0 and 255"),
        ],
        outputs=[gr.Image(), "text"],
        allow_flagging="never"
    )
    demo.launch(show_api=True)
