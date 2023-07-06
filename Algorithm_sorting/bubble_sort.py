# -*-coding:utf-8-*-
def pop_sort(lst):
    for i in range(len(lst)-1, 1, -1):
        move_max(lst, i)

def move_max(lst, max_index):
    """
    将索引0到max_index这个范围内的最大值移动到max_index位置上
    :param lst:
    :param max_index:
    :return:
    """
    for i in range(max_index):
        if lst[i] > lst[i+1]:
            lst[i], lst[i+1] = lst[i+1], lst[i]

if __name__ == '__main__':
    lst = [100, 200, 7, 1, 4, 2, 3, 6]
    pop_sort(lst)
    print(lst)


