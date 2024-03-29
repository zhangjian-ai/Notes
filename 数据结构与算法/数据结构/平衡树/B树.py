"""
B树：首先是一个平衡树。
    B树中允许一个结点包含多个key-value，可以是3个、4个、100个。我们选择一个参数M来表示一个M阶（又叫M个分叉）的B树。具有如下特点：
        - 每个节点最多有M-1个key，并且以升序排列。
        - 每个节点最多具有M个子结点。
        - 若根结点不是叶子结点，则根结点至少有两个子结点。
        - 除根结点和叶子结点外，每个结点至少有 ceil(m/2) 个子结点。
        - 所有的叶子结点都在同一层。因为B树是自底向上生长的。
        - 每个非叶子结点有n个key和n+1个指针组成，其中 [ceil(m/2) - 1] <= n <= m - 1

    B树结点添加逻辑：
        1、每个结点最多保存m-1个key；
        2、当结点的key个数等于m时，那么当前结点 ceil(m/2) 处的key向上加入到父结点中；
        3、同时当前结点 ceil(m/2)（不包含）为分界点，拆分成两个结点；
        4、添加时重复上面的逻辑，从根结点开始对比，按照左小右大的原则，依次往下找，最终插入新的key到叶子结点中。

计算机中磁盘数据的保存就是基于 B树 的，相比较于普通二叉树，B树 的高度远远小于 二叉树，3 层B树可以表示 30 层二叉树，数据的读取速度远远大于二叉树。
"""