#!/usr/bin/env python3

import math

class Entry:
    """map中存储的单个元素"""
    __key = None
    __value = None
    __next = None

    def __init__(self , key , value , next=None):
        """初始化，设置key、value和next"""
        self.__key = key
        self.__value = value
        self.__next = next

    def getKey(self):
        """获取entry的key"""
        return self.__key

    def getValue(self):
        """获取entry的value"""
        return self.__value

    def setValue(self,value):
        """设置entry的value"""
        self.__value = value

    def getNext(self):
        return self.__next

    def setNext(self , nextEntry):
        """设置entry的下一个元素"""
        self.__next = nextEntry
        pass


class HashMap:

    # 默认长度为16
    DEFAULT_LENGTH = 1 << 4

    # 内容长度
    totalSize = DEFAULT_LENGTH

    # 负载因子，默认为0.75。值太大可能导致过多链表，值太小导致数组空间浪费
    loadFactor = 0.75

    # 默认扩容倍数
    resizeNum = 2

    # 已经使用的大小，usedSize >= totalSize * loadFactor时，扩容数组
    usedSize = 0

    # 存储元素的数组
    table = []

    def __init__(self, size=DEFAULT_LENGTH, factor=0.75):
        self.totalSize = size
        self.loadFactor = factor
        self.usedSize = 0
        # 初始化数组元素
        for i in range(self.totalSize):
            self.table.append(None)

    def put(self,key,value):
        """保存key、value值"""

        # 执行扩容
        if self.size() >= self.totalSize*self.loadFactor:
            self.resize()

        tableIndex = self.getTableIndex(key)

        # 判断元素是否已经存在，如果存在则设置已存在对象的value值
        entry = self.table[tableIndex]
        isExist = False
        while entry is not None and not isExist :
            # 判断元素的key是否相同
            if entry.getKey()==key:
                isExist=True
                break
            else:
                entry=entry.getNext()

        if isExist:
            print("设置链表在位置%d, 已存在entry的value值: %s" % (tableIndex , value))
            entry.setValue(value)
        else:
            newEntry = Entry(key, value)
            # 将已存在元素向后排挤
            if self.table[tableIndex] is not None:
                print("链表在位置%d, 已经存在元素key=%s" % (tableIndex,key))
                newEntry.setNext(self.table[tableIndex])
            else:
                print("链表在位置%d, 新建元素key=%s" % (tableIndex,key))

            # 设置数组当前位置为新插入的元素
            self.table[tableIndex] = newEntry
            # 增加已有元素的长度
            self.usedSize += 1

    def get(self,key):
        """根据key获取对应的value"""
        tableIndex = self.getTableIndex(key)

        entry = self.table[tableIndex]
        isExist = False
        while entry is not None and not isExist:
            # 判断元素的key是否相同
            if entry.getKey() == key:
                isExist = True
                break
            else:
                entry = entry.getNext()

        if isExist:
            return entry.getValue()
        else:
            return None

    def getTableIndex(self,key):
        """获取key在数组中的位置，算法：
        1、根据key原有的hash值，重新执行散列算法（计算出的值散列分布效果更好）
        2、和（数组长度-1）进行与操作，保证散列值不超过数组存储边界
        """
        return self.hash(key) & (self.totalSize-1)

    def hash(self,key):
        """重新计算key的hash值，算法：后32位和前32位进行异或运算"""
        return key.__hash__() ^ (key.__hash__() >> 32)

    def size(self):
        return self.usedSize

    def resize(self):
        """扩容"""
        print("================执行扩容，扩容后大小=%d"%(math.ceil(self.totalSize * self.resizeNum)))
        # 新创建数组，指定大小为原有数组的两倍
        newtable=[]
        for i in range( math.ceil(self.totalSize * self.resizeNum) ):
            newtable.append(None)

        # 保存老数组数据，创建新数组并初始化相关属性
        oldTable = self.table
        self.table = newtable
        self.totalSize = len(self.table)
        self.usedSize = 0

        for item in oldTable:
            while item is not None:
                print("扩容存放元素: %s"%(item.getKey()))
                self.put(item.getKey(),item.getValue())
                # 链表的下一个元素
                item = item.getNext()

    def entrySet(self):
        """获取map的entry集合"""
        print("================获取entryset")
        entryTable = []
        for index,item in enumerate(self.table):
            entrySize=0
            while item is not None:
                entrySize += 1
                entryTable.append(item)
                # 链表的下一个元素
                item = item.getNext()
            if entrySize>1:
                print("%d位置链表大小%d" % (index , entrySize))

        return entryTable


if __name__=="__main__":
    myMap = HashMap()

    for i in range(14):
        myMap.put("testkey" + str(i), "testvalue" + str(i))

    print("已经使用的大小=%d" % (myMap.size()))

    print("查找value=%s" % (myMap.get("testkey1")))

    entryTable = myMap.entrySet()

    print("entryTable实际大小=%d" % (len(entryTable)))
