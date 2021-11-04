class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        p1 = 0
        p2 = 0
        l1 = len(s)
        l2 = len(p)
        temp = []

        # 找出每个p中每个*号在对应的索引区间
        while p1 < l1 and p2 < l2:
            if p[p2] == ".":
                p1 += 1
                p2 += 1
                continue
            if p[p2] == '*':
                head = p[p2 - 1]
                start = p1
                while p1 < l1 and p2 < l2:
                    if s[p1] == p[p2 + 1]:
                        end = p1
                    p1 += 1


        return True


if __name__ == '__main__':
    s = Solution()
    print(s.isMatch("aaa", "a*a"))
