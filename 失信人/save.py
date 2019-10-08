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


i = 1
while 1:
    i += 1
    if get_one_chinese() == '蚎':
        print(i)
        break



