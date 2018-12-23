import requests

CITY_CODE = []
CITY_NAME = []


def city2code(name):
    return CITY_CODE[CITY_NAME.index(name)]


def code2city(code):
    return CITY_NAME[CITY_CODE.index(code)]


__url = r'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9040'


# 获取城市列表
def __get():
    content = requests.get(__url).content.decode('utf8')
    city_code_dict = dict()

    city_list = list(filter(lambda s: s and s.strip(), content.split('@')))[1:]
    for city in city_list:
        city_info = city.split('|')
        city_jane, city_name, city_code, city_pinyin, _, city_num = city_info
        city_code_dict[city_code] = city_name

    return city_code_dict


# 把JSON文件中的城市列表加载到内存里
def load():
    temp = __get()
    global CITY_CODE, CITY_NAME
    CITY_CODE = list(temp.keys())
    CITY_NAME = list(temp.values())


if __name__ == '__main__':
    load()
    print(CITY_NAME)
    print(city2code('北京'))