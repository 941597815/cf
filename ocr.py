import time
from utils import game_dict, custom_screenshot, save_image, text_in_str, text_diff
from osd import updata_osd
from OCR.ocr_for_cnocr import getImgText_for_single_line


def worker_ocr(globals_instance):

    bounding_box = game_dict[globals_instance.resolution]["weapon_Identify_box"]
    while True:
        if globals_instance.weapons_identification:
            # img = custom_screenshot(bounding_box)
            # save_image(img)
            # text = getImgText(img)
            # 调用 getImgText 函数识别文字
            text = getImgText_for_single_line(
                custom_screenshot(bounding_box), globals_instance.debug
            )
            if globals_instance.debug:
                updata_osd(globals_instance, text)
                # print(f"识别到文字{text}")
            if text:
                # 判断是否包含“炼狱”
                if text_diff(game_dict["jtl"], text, 1):
                    # print("文本中包含“炼狱”")
                    globals_instance.jtl = True
                    globals_instance.usp = False
                    globals_instance.jujiqiang = False
                    globals_instance.buqiang = False
                elif text_diff(game_dict["usp"], text, 2):
                    # print("文本中包含“usp”")
                    globals_instance.usp = True
                    globals_instance.jtl = False
                    globals_instance.jujiqiang = False
                    globals_instance.buqiang = False
                elif text_diff(game_dict["ju"], text, 3):
                    globals_instance.jujiqiang = True
                    globals_instance.jtl = False
                    globals_instance.usp = False
                    globals_instance.buqiang = False
                else:
                    # print("文本中不包含“炼狱”")
                    globals_instance.jtl = False
                    globals_instance.usp = False
                    globals_instance.jujiqiang = False
                    globals_instance.buqiang = True

                time.sleep(0.3)
            else:
                time.sleep(3)
        else:
            time.sleep(3)


if __name__ == "__main__":
    while True:
        time.sleep(3.5)
        bounding_box = game_dict[1]["weapon_Identify_box"]

        # text = getImgText(custom_screenshot(bounding_box))
        # text = getImgText("./image.png")

        # print(text)
