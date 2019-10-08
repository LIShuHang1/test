import requests as r
import json

import utils.tools as tools
import utils.db_tools as DB

# 设置文件指针的初始值
pointer = 1


def get_one_chinese():
    chinese_world = ''
    try:
        f = open('gbk.csv', 'r', encoding="utf-8")
        # 先设置文件指针的位置
        global pointer
        chinese_world = f.read()[pointer]
        # 获得当前的文件指针--存在文件或者数据库中
        pointer += 1
    except Exception as tip:
        print(tip)
    finally:
        # 关闭资源
        try:
            f.close()
        except:
            return False
    return chinese_world


url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
# pn = 0
# count = 0
area = ['北京', '广东', '山东', '江苏', '河南', '上海', '河北', '浙江', '陕西', '湖南', '重庆', '福建', '天津', '云南', '四川', '安徽', '海南', '江西', '湖北', '山西', '辽宁', '台湾', '黑龙江', '贵州', '甘肃', '青海', '新疆', '西藏', '吉林']
headers = {
    'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&oq=%25E5%25A4%25B1%25E4%25BF%25A1%25E4%25BA%25BA&rsv_pq=d6b2860b004920a9&rsv_t=95c71iPQlqmv%2BhG7GQ%2Bu3haZAm7hlycZXa5Ij3YQnUf00Ecgtw7pyPoFo2g&rqlang=cn&rsv_enter=0&rsv_dl=tb',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}


def main(area):
    count = 50
    # global pn
    # global count
    kw = get_one_chinese()
    print(kw)

    data = tools.format_colon_string('''
    resource_id: 6899
    query: 失信被执行人名单
    cardNum: 
    iname: %s
    areaName: %s
    ie: utf-8
    oe: utf-8
    format: json
    t: 1565872207460
    cb: jQuery1102015406695143133042_1565871919723
    _: 1565871919725
    ''' % (kw, area))

    res = r.get(url=url, params=data, headers=headers)
    print(str(res.text[47:-2]))
    datas = json.loads(str(res.text[47:-2]))
    peoples = datas['data'][0]['result']
    db = DB.DBTools.creater()
    for i in peoples:
        # i:每一个失信人信息
        name = i['iname']
        age = i['age']
        card_id = i['cardNum']
        card_num = i['caseCode']
        court_name = i['courtName']
        disrupt_type_name = i['disruptTypeName']
        duty = i['duty']
        date = i['regDate']
        gender = i['sexy']
        print(name, age, card_id, card_num, court_name, disrupt_type_name, duty, date, gender)
        count += 1
        print(count)
        # 入库
        try:
            db.setSQL('insert into shixinren(name, age, card_id, card_num, court_name, disrupt_type_name, duty, date, gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)')
            db.excute((name, age, card_id, card_num, court_name, disrupt_type_name, duty, date, gender))
        except:
            pass

        # 分页
        # pn += 50
    db.close()


if __name__ == '__main__':
    while 1:
        try:
            for i in area:
                main(i)
        except:
            pass