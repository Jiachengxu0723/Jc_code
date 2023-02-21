def is_leap():
    year = input('请输入一个年份:').strip()
    if year == 'q':
        return False,'已退出判断'
    else:
        if year.isdigit():
            year = int(year)
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 ==0 and year % 3200 != 0):
                return True,f'{year}年是润年'
            else:
                return True,f'{year}年是平年'
        else:
            return True,'请输入正确的年份'

if __name__ == '__main__':
    print('输入一个年份，按「Enter」来判断是不是润年份,按「q」退出判断')
    while True:
        flag, msg = is_leap()
        if flag:
            print(msg)
        else:
            print(msg)
            break