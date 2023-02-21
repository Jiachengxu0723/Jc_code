import os
from typing import List

def read_txt(file_path):
    products = []
    if os.path.isfile(file_path):
        with open(file_path,'r') as file:
            for line in file:
                name, price = line.strip().split(',')
                price = int(price)
                products.append([name,price])
    else:
        print('inexistent')
    print(products)
    return products

def user_input(products):
    while True:
        name = input('请输入商品: ')
        if name == 'q':
            break
        price = int(input('请输入价格： '))
        products.append([name,price])
    print(products)
    return products

def write_txt(file_path,products):
    with open(file_path,'w+') as f:
        for p in products:
            f.write(p[0] + ',' + str(p[1]) + '\n')


if __name__ == '__main__':
    file_path = ('test.txt')
    products = read_txt(file_path)
    products = user_input(products)
    write_txt(file_path,products)