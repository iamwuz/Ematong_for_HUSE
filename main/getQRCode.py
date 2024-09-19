import qrcode
from PIL import ImageOps, ImageDraw, ImageFont
import json
import requests
import time



def huse_getQRcode():
    with open("../config/info.json", "r") as f:
        info = json.load(f)
        access_token=info['access_token']
    headers = {'Authorization': access_token,
               'mobile': '13789229207'}
    resp = requests.get(
        'https://apppro.zhixiaole.net/v2/vcard/doorQrcode?school_id=14025&provider_code=1003&vcard_no=202206030117',
        headers=headers)
    data = json.loads(resp.text)
    QRstr = data['data']['code']
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3
    )
    qr.add_data(QRstr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 扩展图片边界，增加文本区域
    expanded_img = ImageOps.expand(img, border=(0, 10, 0, 0), fill='white')

    draw = ImageDraw.Draw(expanded_img)
    text1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 计算文本边界框位置
    text_bbox = draw.textbbox((0, 0), text1)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_width, _ = expanded_img.size
    x_position = (img_width - text_width*1.7) / 2
    y_position = 10  # 距离上边界10像素

    # 在图像上方写入时间
    draw.text((x_position, y_position), text1, fill="black",font_size=18)
    expanded_img.save('../pic/'+'pay.png')


if __name__ == '__main__':
    huse_getQRcode()