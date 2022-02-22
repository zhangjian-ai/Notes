class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


#
# @param head ListNode类 the head
# @return bool布尔型
#
class Solution:
    def LCS(self, s1, s2):
        # 动态规划用一个二维数组记录当前长度的字符串中的最长子序列
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m):
            for j in range(n):
                dp[i + 1][j + 1] = dp[i][j] + 1 if s1[i] == s2[j] else max(dp[i][j + 1], dp[i + 1][j])

        if dp[m][n] == 0:
            return -1

        m -= 1
        n -= 1
        string = ""
        # 从字符串结尾开始往前找
        while m >= 0 and n >= 0:
            print(m, n, s1[m], s2[n])
            if s1[m] == s2[n]:
                string = s1[m] + string
                m -= 1
                n -= 1
            # 通过记录的子序列长度，来判断查找的方向
            elif dp[m][n + 1] > dp[m + 1][n]:
                m -= 1
            else:
                n -= 1

        return string


if __name__ == '__main__':
    s = Solution()
    print(s.LCS("1a1a31", "1a231"))
