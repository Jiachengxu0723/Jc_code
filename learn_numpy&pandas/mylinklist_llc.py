'''
实现一个链表（包括链表的节点(包括一个int类型data成员)以及一个链表类)，并实现以下函数（五选三）
a 链表的初始化和访问指定项的data值
b 在指定节点前/后插入新的一个给定节点
c 链表实例的初始化和清除所有节点
d 前后倒置链表
e 在整个链表实例中搜索指定data值

ps. 线性表的第i个元素存储在第i-1的位置

'''


'''
current_node = self 的概念，里面包含头节点和新节点

空链表状态下：
current_node.next = None
current_node.length = 0

有一个节点【node1 = Node(1)】的状态下：
current_node.length = 1
current_node.next = node1
current_node.next.data = 1    ——> node1.data = 1
current_node.next.next = None ——> node1.next = None

有两个节点【node1 = Node(1)、node2 = Node(2)】的状态下：
current_node.length = 2
current_node.next = node1
current_node.next.data = 1       ——> node1.data = 1
current_node.next.next = node2   ——> node1.next = node2
current_node.next.next.data = 2     ——> node2.data = 2
current_node.next.next.next = None  ——> node2.next = None

有三个节点【node1 = Node(1)、node2 = Node(2)、node3 = Node(3)】的状态下：
current_node.length = 3
current_node.next = node1
current_node.next.data = 1       ——> node1.data = 1
current_node.next.next = node2   ——> node1.next = node2
current_node.next.next.data = 2     ——> node2.data = 2
current_node.next.next.next = None  ——> node2.next = node3
current_node.next.next.next.data = 3     ——> node3.data = 3
current_node.next.next.next.next = None  ——> node3.next = None

以此类推....

'''

'''
你这个链表：
表头用一个head, 不要用current_node = self这样不太直观
2.  链表倒置，你可以查一下
等你改了这两个我再跟你沟通下
'''

class Node:
    """节点"""
    def __init__(self, data:int):
        self.data = data   #数据域
        self.next = None   #指针域


class SingleLinkList:
    """单链表"""
    def __init__(self): 
        self.__head = None
        self.length = 0


    def is_empty(self):
        '''判断链表是否为空'''
        return self.__head is None


    def add_in_head(self, data:int):
        '''把新结点插入头节点的后面'''
        new_node = Node(data = data)
        new_node.next = self.__head  # 新节点的下一个节点为旧链表的头结点
        self.__head = new_node  # 新链表的头结点为新节点
        self.length += 1


    def add_in_tail(self, data:int):
        '''把新结点插入终端节点的后面'''
        new_node = Node(data = data)
        if self.is_empty():
            self.__head = new_node
        else:
            cur = self.__head
            while cur.next is not None:
                scur = cur.next
            cur.next = new_node
        self.length += 1
  

    def search_by_index(self, search_index:int):
        '''访问指定索引的数据元素'''
        if search_index >= self.length:
            return False, 'ERROR! index out of the length of the link list'
        else:
            for _ in range(search_index + 1):
                self.__head = self.__head.next
            return True, self.__head.data


    def search_by_data(self, search_data:int):
        '''访问指定数据元素的索引(若数据元素重复,只找出索引最小的那个)'''
        index = 0
        while self.__head.next is not None:
            if self.__head.next.data != search_data:
                self.__head = self.__head.next
                index += 1
                continue
            else:
                return True, index
        return False, 'ERROR! data does not exist'


    def add_data_after_index(self, position_index:int, add_data:int):
        '''在指定索引前插入新的一个给定节点'''
        new_node = Node(data = add_data)
        if position_index >= self.length or position_index < 0:
            return 'ERROR! index out of the length of the link list'
        else:
            for _ in range(position_index + 1):
                self.__head = self.__head.next
            new_node.next = self.__head.next
            self.__head.next = new_node
            self.length += 1
            return 'add successfully'


    def add_data_before_index(self, position_index:int, add_data:int):
        '''在指定索引后插入新的一个给定节点'''
        new_node = Node(data = add_data)
        if position_index > self.length or position_index < 0:
            return 'ERROR! index out of the length of the link list'
        else:
            for _ in range(position_index):
                self.__head = self.__head.next
            new_node.next = self.__head.next
            self.__head.next = new_node
            self.length += 1
            return 'add successfully'


    def add_data_before_data(self, add_data:int, position_data:int):
        '''在指定节点前插入新的一个给定节点'''
        flag, msg_or_index = self.search_by_data(search_data = position_data)
        if flag:
            return self.add_data_before_index(position_index = msg_or_index, add_data = add_data)
        else:
            return msg_or_index


    def add_data_after_data(self, add_data:int, position_data:int):
        '''在指定节点后插入新的一个给定节点'''
        flag, msg_or_index = self.search_by_data(search_data = position_data)
        if flag:
            return self.add_data_after_index(position_index = msg_or_index, add_data = add_data)
        else:
            return msg_or_index


    def delete_by_data(self, data:int):
        '''根据数据元素删除结点(若数据元素重复,只删除索引最小的那个)'''
        while self.__head.next is not None:
            next_node = self.__head.next
            if next_node.data == data:
                self.__head.next = self.__head.next.next
                self.length -= 1
            else:
                self.__head = next_node
        return 'ERROR! data does not exist'


    def delete_by_index(self, delete_index:int):
        '''根据索引删除结点'''
        if delete_index >= self.length or delete_index < 0:
            return 'ERROR! index out of the length of the link list'
        else:
            for _ in range(delete_index):
                self.__head = self.__head.next
            self.__head.next = self.__head.next.next
            self.length -= 1


    def clear_list(self):
        '''清除所有节点'''
        flag = input('You are clearing a link list ,please press「Enter」to CLEAR or press「q」to CANCLE: ')
        if flag == 'Q' or flag == 'q':
            return 0
        self.__init__()


    def print_all_data(self):
        '''打印链表结点'''
        data_list = []
        while self.__head.next is not None:
            data_list.append(self.__head.next.data)
            self.__head = self.__head.next
        return data_list



if __name__ == "__main__":

    # 链表的初始化
    single_link_list = SingleLinkList()

    print(single_link_list.is_empty())

    # 链表实例的初始化
    single_link_list.add_in_tail(data = 2)   # node2 = Node(data = 2)
    print(single_link_list.print_all_data())

    # single_link_list.add_in_head(data = 1)   # node1 = Node(data = 1)
    # single_link_list.add_in_tail(data = 3)   # node3 = Node(data = 3)

    # print(single_link_list.print_all_data())


    # # 访问指定项的data值
    # flag, msg_or_data = single_link_list.search_by_index(search_index = 2)
    # print(msg_or_data)

    # flag, msg_or_data = single_link_list.search_by_index(search_index = 4)
    # print(msg_or_data)

    # # 在指定节点前插入新的一个给定节点
    # single_link_list.add_data_before_data(add_data = 4,position_data = 2)  # 在节点2前插入节点4

    # # 在指定节点后插入新的一个给定节点
    # single_link_list.add_data_after_data(add_data = 5, position_data = 4)  # 在节点4后插入节点5

    # # 在整个链表实例中搜索指定data值
    # flag, msg_or_index = single_link_list.search_by_data(search_data = 3)
    # print(msg_or_index)  

    # flag, msg_or_index = single_link_list.search_by_data(search_data = 6)
    # print(msg_or_index)  

    # result = single_link_list.print_all_data()
    # print(result) 

    # # 清除所有节点 
    # single_link_list.clear_list()

    # result = single_link_list.print_all_data()
    # print(result) 