import random
choice_list = [[],[]]

def check_list():
    if choice_list[0] :
        print('当前备选国家为',[country for country in choice_list[0]])
        print('当前备选类型为',[type for type in choice_list[1]])
    else:
        print('增加清单为空，请先增加')

def add_list():
    while True:
        print('''
        --------------------
            1.增加随机国家
            2.增加随机类型
            q.返回上一级
        --------------------
        ''')
        choice = input('请选择增加清单：').strip()
        if choice == 'q':
            break
        while True:
            if choice == '1':
                inp_country = input('请输入备选国家(输入q退出)：').strip()
                if inp_country == 'q':
                    break
                choice_list[0].append(inp_country)
                continue
            if choice == '2':
                inp_type = input('请输入备选类型：').strip()
                if inp_type == 'q':
                    break
                choice_list[1].append(inp_type)
                continue
            else:
                print('请输入正确的功能编号！')

def make_a_choice():
    if choice_list[0] :
        x = len(choice_list[0]) -1
        country_index = random.randint(0,x)
        y = len(choice_list[1]) -1 
        type_index = random.randint(0,y)
        print(f'帮你决定好了，看{choice_list[0][country_index]}的{choice_list[1][type_index]}片，enjoy your MOVIE NIGHT!')

    else:
        print('选择清单为空，请先增加随机清单')

func_dic = {
    '1':check_list,
    '2':add_list,
    '3':make_a_choice,
}

def run():
    while True:
        print('''
        ************************
                1.查看随机清单
                2.增加随机清单
                3.『帮我选择』
                q.退出
        ************************
        ''')
        choice = input('请输入功能编号：').strip()
        if choice == 'q':
            break
        if choice in func_dic:
            func_dic.get(choice)()
        else:
            print('请输入正确的功能编号！')
    
if __name__ == "__main__":
    print('让我们简单轻松决定MOVIE NIGHT的走向')
    run()