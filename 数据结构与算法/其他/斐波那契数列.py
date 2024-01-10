class Fibonacci:
    a = 0
    b = 1

    @classmethod
    def impl1(cls, n):
        """
        循环输出
        时间复杂度 O(n)
        空间复杂度 O(1)
        """

        while n > 0:
            res = cls.a + cls.b
            print(res)

            cls.a = cls.b
            cls.b = res

            n -= 1

    @classmethod
    def impl2(cls, n):
        """
        递归实现
        时间复杂度 O(n)
        空间复杂度 O(n)
        """
        if n == 0:
            print(cls.a + cls.b)
            return cls.a, cls.b

        cls.a, cls.b = cls.impl2(n - 1)
        print(cls.a + cls.b)

        return cls.b, cls.a + cls.b
