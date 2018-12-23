import requests
from json import loads,dumps
import base64
from PIL import Image
from io import BytesIO
from PIL import Image, ImageDraw2, ImageDraw,ImageFont


# 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
center_position = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']


# 自动识别
def auto_recognize(data):
    code_base64 = data
    data = {
        "base64": base64.b64encode(data).decode('ascii')
    }

    # print(dumps(data))
    resp = requests.session().post('http://60.205.200.159/api',
                                   headers={'Content-Type': 'application/json'},
                                   data=dumps(data))
    resp = loads(resp.content)
    if resp['success']:
        check_data = {
            '=': '""',
            'check': resp['check'],
            'img_buf': data['base64'],
            'logon': 1,
            'type': 'D'

        }
        resp = requests.session().post('http://check.huochepiao.360.cn/img_vcode',
                                       headers={'Content-Type': 'text/plain'},
                                       data=dumps(check_data))
        answer = [];
        position = []
        # print('数据',resp.content)
        temp = loads(resp.content)['res'].replace('(', '').replace(')', '').split(',')
        i = 0
        while i < len(temp):
            answer.append(int(temp[i]) // 70 + int(temp[i+1]) // 70 * 4)
            i += 2
        print('识别%s'%answer)
        for pos in answer:
            position.append(center_position[int(pos)])
        # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
        auto_choose(position, code_base64)
        return ','.join(position)


def auto_choose(positions, code_base64):
    img = Image.open(BytesIO(code_base64))
    draw = ImageDraw.Draw(img)
    for pos in positions:
        draw.text((int(pos[0]), int(pos[1])), 'O', (0,0,0), ImageFont.truetype("/Library/Fonts/Arial.ttf",20))
    img.show()
    # Log.v(
    #     """
    #     -----------------
    #     | 0 | 1 | 2 | 3 |
    #     -----------------
    #     | 4 | 5 | 6 | 7 |
    #     ----------------- """)
    # results = input("输入验证码索引(见上图，以','分割）: ")
    img.close()


# 手动识别
def manual_recognize(data):
    with open('img.jpg', 'wb') as f:
        f.write(data)
    # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
    try:
        im = Image.open('img.jpg')
        # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
        im.show()
        # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
        im.close()
    except:
        print
        u'请输入验证码'
    # =======================================================================
    # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,5  70*70
    # ---------------------------------------
    #         |         |         |
    #    0    |    1    |    2    |     3
    #         |         |         |
    # ---------------------------------------
    #         |         |         |
    #    4    |    5    |    6    |     7
    #         |         |         |
    # ---------------------------------------
    # =======================================================================
    answer = input('请输入验证码位置，以","分割[例如2,5]:')
    position = []
    for pos in answer.split(','):
        position.append(center_position[int(pos)])
    # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
    return ','.join(position)
