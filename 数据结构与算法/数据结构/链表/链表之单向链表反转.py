'''
需求：实现单向链表的反转
'''

from 链表之单向链表 import LinkList


class RevLinkList(LinkList):

    # 反转整个列表
    def reverse(self):
        if self.isEmpty:
            return None

        self.reverse_node(self.head.next)

    # 反转单个结点
    def reverse_node(self, node):
        # 如果没有下一个结点，那就是最后一个结点。则将head指向该结点，并返回该结点
        if not node.next:
            self.head.next = node
            return node

        # 返回的结点作为当前结点的上一个结点
        pre = self.reverse_node(node.next)

        # 当前结点就作为上一个结点的下一个结点
        pre.next = node

        # 当前结点的下一个结点还不知道是谁，先设置为None，如果递归回到上一层还有结点，那么上一步会给它赋值
        node.next = None

        return node


if __name__ == '__main__':

    seq = RevLinkList()
    seq.add("姚明")
    seq.add("老张")
    seq.add("朱晓明")
    seq.add("好吧睡觉")
    # seq.add(1)
    # seq.add(2)

    # print(seq)
    # print(seq.get(0))
    # print(seq.isEmpty)
    #
    # seq.remove(3)
    # print(seq.get(3))
    # print(seq.items)
    #
    seq.insert(0, "悍匪")
    # # print(seq.items)
    # print(seq.indexOf("姚明"))
    # print(seq.length)
    #
    # seq.clear()
    seq.add("调任新职")

    for i in seq:
        print(i)

    seq.reverse()
    print("-------------")

    for i in seq:
        print(i)
