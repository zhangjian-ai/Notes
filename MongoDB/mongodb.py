from pymongo import MongoClient


class MongoDb:

    def __init__(self):
        # 创建客户端
        conn = MongoClient('101.43.61.175', 27017)

        # 链接一个数据库，如果数据库不存在，会自动创建
        db = conn.my_db

        # 使用一个集合，没有则自动创建
        self.my_set = db.test_set

    def insert(self):
        my_set = self.my_set

        # 插入一条数据。在新版中，insert和save已不再建议使用
        my_set.insert_one({"name": "zhangjian", "age": 18})
        # my_set.save({"name": "liurushi", "age": 16})

        # 插入多条数据到集合。插入多条数据时，多个字典放到列表中。同时尽量使用insert；insert一次性插入；save则是遍历列表逐条插入，效率较低
        users = [
            {"name": "chenyuanyuan", "age": 16},
            {"name": "suxiaoxiao", "age": 14}
        ]

        my_set.insert_many(users)

    def query(self):
        my_set = self.my_set

        # 更新数据；可以选择更新第一条和更新多条
        my_set.update_many({"name": "zhangjian"}, {"$set": {"age": 26, "height": "180cm"}})
        my_set.update_one({"name": "zhangjian"}, {"$set": {"sex": "male"}})

        # push\pushAll  向集合中，value是列表的值追加元素
        my_set.update_one({"name": "suxiaoxiao"}, {"$push": {"li": {"demo": 666}}})  # 向列表中追加一个值。value被当作整体加到列表中
        my_set.update_one({"name": "suxiaoxiao"},
                          {"$pushAll": {"li": [66, 77]}})  # 向列表中追加一个值。 只允许传入数组列表，把列表中的值遍历追加到目标列表中

        # pop 删除列表元素。1：最后一个； -1：第一个
        # my_set.update_many({"name": "suxiaoxiao"}, {"$pop": {"li": -1}})

        # pull/pullAll 按值删除元素
        my_set.update_many({"name": "suxiaoxiao"}, {"$pull": {"li": 3}})  # 移除单个值
        my_set.update_many({"name": "suxiaoxiao"}, {"$pullAll": {"li": [1, 2, 4]}})  # 移除多个值

        # 多级操作。用链接符'.'链接，列表可直接使用索引；字典直接用key
        my_set.update_one({"name": "suxiaoxiao"}, {"$set": {"li.0.demo": "我被改了呢3"}})

        # 删除数据
        # my_set.remove()  # 删除集合所有数据
        # my_set.delete_one({"name": "zhangjian"})  # 删除第一条数据，必须要有筛选条件

        # 查询数据，如果没有数据则返回None；有数据则返回一个数据库游标对象
        query = my_set.find()  # 查所有

        # query = my_set.find({"name": "zhangjian"})  # 条件查询
        # query = my_set.find({"age": {"$gte": 10}})  # 查询年龄大于等于10的数据
        # query = my_set.find({"name": {"$type": 2}})  # 查询name字段类型时string的数据
        # query = my_set.find({"age": {"$in": (14, 16)}})  # 查询年龄是14或者16的数据
        # query = my_set.find({"$or": [{"name": "zhangjian"}, {"age": 16}]})  # 查询名字是张建或者age是16的数据

        # 通过id来删除数据
        id = my_set.find_one()['_id']
        # my_set.remove(id)  # remove已不再建议使用

        # query.sort([("age", 1), ("name", -1)])  # 查询结果排序。先按年龄升序，再按name降序
        # query.skip(3)  # 跳过前3条数据
        # query.limit(5)  # 只展示查询结果的前5条数据
        #
        # query.skip(1).limit(2)

        # 返回的游标对象是可迭代对象。每次迭代返回一个字典，即插入时的字典，但此时每个字典均被默认添加一个key为 '_id' 的键值对
        for i in query:
            print(i)
            pass


if __name__ == '__main__':
    # MongoDb().insert()

    # MongoDb().query()

    # 创建客户端
    conn = MongoClient('101.43.61.175', 39006, username="xz_test", password="xz_test_pwd")

    # 链接一个数据库，如果数据库不存在，会自动创建
    db = conn.autotest

    # 使用一个集合，没有则自动创建
    my_set = db.tp

    print(my_set)

    from bson.objectid import ObjectId
    # my_set.insert_one({"name": "zhangjian"})
    # my_set.update_one({'_id': ObjectId('6204c1f181de152c57c30d20')}, {'$set': {'origin.height': "178"}})

    for i in my_set.find():
        print(i)

    # print(type(my_set.find_one({'_id': ObjectId('6204c1f181de152c57c30d20')})))

    print()
