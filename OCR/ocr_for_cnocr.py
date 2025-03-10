from cnocr import CnOcr
import time

ocr = CnOcr()


def getImgText_for_single_line(img, return_score=False):
    out = ocr.ocr_for_single_line(img)
    text = out["text"]
    if not text:
        return None
    if return_score:
        text = out["text"] + str(out["score"])
    return text


if __name__ == "__main__":
    img_fp = "./image.png"
    while True:
        time.sleep(0.3)
        text = getImgText_for_single_line(img_fp, True)
        print(text)
