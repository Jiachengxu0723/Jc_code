# -*-coding:utf-8-*-
def partition(lst,start,end):
    """
    用lst[start] 做基准值，在start到end这个范围进行分区
    """
    pivot = lst[start]

    while start < end :
        while start < end and lst[end] >= pivot:
            end -= 1
        lst[start] = lst[end]

        while start < end and lst[start] <= pivot:
            start += 1
        lst[end] = lst[start]

    lst[start] = pivot
    return start

def my_quick_sort(lst,start,end):
    if start>= end:
        return

    index = partition(lst,start,end)
    my_quick_sort(lst,start,index-1)
    my_quick_sort(lst,index+1,end)

if __name__ == '__main__':
    lst = [4,3,2,4,1,5,7,2]
    my_quick_sort(lst,0,len(lst)-1)
    print(lst)