# 理解 DevOps 

DevOps（Development和Operations的组合词）是一种重视“软件开发人员（Dev）”和“IT运维技术人员（Ops）”之间沟通合作的文化、运动或惯例。

**DevOps 强调的是高效组织团队之间如何通过自动化的工具协作和沟通来完成软件的生命周期管理，从而更快、更频繁地交付更稳定的软件**。

DevOps 的三大支柱之中，即人（People）、流程（Process）和平台（Platform）。这里重点介绍 搭建平台 的工具。



# Jenkins





# Git

`git`有四个工作区域，分别是：

- 工作目录（`Workspace`）
- 暂存区（`Index/Stage`）
- 本地仓库（`Repository`）
- 远程仓库（`Remote`）

日常使用最多的应该是下图的6个命令，下图也反映出四个工作区域的关联关系。

<img src="./images/git_001.png" style="width: 70%; float: left;">



> 本文使用 GitHub 上的一个示例仓库 Repo 作为常用命令的示例。



## 常用命令

### git init

`git init`命令的作用是在当前目录中初始化仓库，并且创建一个名为`.git`的子目录，该目录含有你初始化的`git`仓库中所有的必须文件。



### git remote

`git remote`命令的作用主要是管理远程仓库。

1. 查看关联的远程仓库的名称：`git remote`
2. 查看关联的远程仓库的详细信息：`git remote -v`
3. 添加远程仓库的关联：`git remote add <远程仓库名称> <远程仓库地址>`
4. 删除远程仓库的关联：`git remote remove <远程仓库名称>`
5. 修改远程仓库的关联：`git remote set-url <远程仓库名称> <新的远程仓库地址>`
6. 更新远程仓库的分支：`git remote update <远程仓库名称> --prune`



### git clone

`git clone` 克隆远程仓库到本地。拷贝完成后，Git 会在当前目录下生成一个本地项目目录。 通常就是该 URL 最后一个 / 之后的项目名称。当然，也可以在 URL 后面跟上一个你想要的目录名称。

语法：

```shell
git clone [-b <分支名>] url [自定义本地项目目录名称]
```

示例：

```shell
# 克隆一个空的仓库到本地
zhangjian@zhangjiandeMacBook-Pro PycharmProjects % git clone git@github.com:zhangjian-ai/Repo.git
Cloning into 'Repo'...
warning: You appear to have cloned an empty repository.

# 当前目录已创建了一个本地目录
zhangjian@zhangjiandeMacBook-Pro PycharmProjects % ls
AutoTest_MeiDuo		AutomationTestPlat	Repo			automation_test		jmeter_ant		pypi

# 通常克隆时，建议只克隆master分支，其他远程分支不需要克隆
git clone -b master git@github.com:zhangjian-ai/Repo.git
```



### git status

`git status`命令的作用是查看工作区文件状态，**红色表示工作目录的文件被修改但还没有提交到暂存区，绿色表示已经提交到暂存区。**

`git status`命令主要是查看 工作区 文件的修改状态。

以极简的方式显示文件状态：`git status -s`

- `A`：本地新增的文件（服务器上没有）
- `C`：文件的一个新拷贝
- `D`：本地删除的文件（服务器上还在）
- `M`：红色为修改过未被添加进暂存区的，绿色为已经添加进暂存区的
- `R`：文件名被修改
- `T`：文件的类型被修改
- `U`：文件没有被合并(你需要完成合并才能进行提交)
- `X`：未知状态(很可能是遇到`git`的`bug`了，你可以向`git`提交`bug report`)
- `??`：未被`git`进行管理，可以使用`git add fileName`把文件添加进来进行管理

> 已经被修改但还没提交到暂存区的文件，可以通过命令`git checkout -- fileName`撤销更改。



### git log

`git log`命令的作用是查看历史 提交 记录，即 暂存区 的 commit 记录。

1. 查看历史提交记录：`git log`
2. 将每条历史提交记录展示成一行：`git log --oneline`，也可以使用`git log --pretty=oneline`
3. 查看某个人的提交记录：`git log --author="name"`
4. 显示`ASCII`图形表示的分支合并历史：`git log --graph`
5. 显示前`n`条记录：`git log -n`
6. 显示某个日期之后的记录：`git log --after="2018-10-1"`，包含2018年10月1号的记录
7. 显示某个日期之前的记录：`git log --after="2018-10-1`，包含2018年10月1号的记录
8. 显示某两个日期之间的记录：`git log --after="2018-10-1" --before="2018-10-7"`



### git reset

`git reset`命令的作用是撤销暂存区的修改或本地仓库的提交。

1. 撤销已经提交到暂存区的文件（已经`git add`但还未`git commit`）：
   - 撤销已经提交到暂存区的文件：`git reset HEAD fileName`或`git reset --mixed HEAD fileName`
   - 撤销所有提交：`git reset HEAD .`或`git reset --mixed HEAD .`
2. 对已经提交到本地仓库做撤销（已经`git commit`但还未`git push`）：
   - 将头指针恢复，已经提交到暂存区以及工作区的内容都不变：`git reset --soft commit-id`或`git reset --soft HEAD~1`
   - 将头指针恢复并且撤销暂存区的提交，但是工作区的内容不变：`git reset --mixed commit-id`或`git reset --mixed HEAD~1`
   - 将所有内容恢复到指定版本：`git reset --hard commit-id`或`git reset --hard HEAD~1`

注意：`commit id`可通过`git log`查看（取前六位即可）。

> **HEAD 说明：**
>
> - HEAD 表示当前版本
>
> - HEAD^ 上一个版本
>
> - HEAD^^ 上上一个版本
>
> - HEAD^^^ 上上上一个版本
>
> - 以此类推...
>
>   
>
> 可以使用 ～数字 表示：
>
> - HEAD~0 表示当前版本
> - HEAD~1 上一个版本
> - HEAD^2 上上一个版本
> - HEAD^3 上上上一个版本
> - 以此类推...



### git add

`git add`命令的作用是将文件从工作目录添加至暂存区。

1. 把所有修改的信息添加到暂存区：`git add .`
2. 把指定文件的信息添加到暂存区：`git add filename`
3. 把所有跟踪文件中被修改过或已删除的文件信息添加至暂存区：`git add -u`或`git add --update`，它不会处理那些没有被跟踪的文件
4. 把所有跟踪文件中被修改过或已删除文件和所有未跟踪的文件信息添加到暂存区：`git add -A`或`git add --all`



**注意：**`git add .`和`git add -A`在`2.x`版本中提交类型方面功能相同，但会因为所在目录不同产生差异：

- `git add .`只会提交当前目录或者子目录下相应文件。
- `git add -A`无论在哪个目录执行都会提交相应文件。

> 已经被提交到暂存区的文件，可以通过命令`git reset HEAD -- fileName`撤销提交。或者使用`git reset HEAD`撤销此次提交。



在项目目录添加一个文件，内容如下：

```shell
# vi web.html
<p>初始创建文档</p>
```



示例：

```shell
# 添加文件到暂存区
zhangjian@zhangjiandeMacBook-Pro Repo % git add web.html

# 查看文件状态
zhangjian@zhangjiandeMacBook-Pro Repo % git status -s
A  web.html			# 字母 A 此时是 绿色，表示 本地新增文件 已经提交到 暂存区。

# 撤销工作区提交
zhangjian@zhangjiandeMacBook-Pro Repo % git reset HEAD -- web.html

# 再次查看状态
zhangjian@zhangjiandeMacBook-Pro Repo % git status -s
?? web.html  ## 符号 ?? 是红色，表示文件被修改，但还没有提交到暂存区。
```



### git commit

`git commit`命令的作用是将暂存区的修改提交到本地仓库，同时会生成一个`commmit id`。

1. 将暂存区的修改提交到本地仓库：`git commit -m "message"`，`"message"`是本次提交的简述内容，比如添加新功能或修复`bug`等
2. 将工作目录中修改后还未使用`git add .`命令添加到暂存区中的文件也提交到本地仓库：`git commit –a –m "message"`，该命令相当于以下两条命令：
   - `git add .`：把所有修改的信息添加到暂存区
   - `git add -m "message"`：将暂存区的修改提交到本地仓库
3. 撤销上一次提交，并将暂存区文件重新提交（可用于漏掉某个文件的提交或重新编辑提交信息）：`git commit --amend`
   - 如果是commit的内容需要修改，那么可以先修改好文件，然后`git add .`，再执行`git commit --amend`
   - 执行`git commit --amend`后，可以重新编辑上一次的提交信息



示例：

```shell
# 添加到暂存区
zhangjian@zhangjiandeMacBook-Pro Repo % git add .

# 提交到本地仓库
zhangjian@zhangjiandeMacBook-Pro Repo % git commit -m "first time commit"

# 查看提交记录
zhangjian@zhangjiandeMacBook-Pro Repo % git log --oneline
c096fbc (HEAD -> master) first time commit   # commit id: c096fbc
```



### git push

`git push`命令的作用是将本地仓库的更新推送到远程仓库上。

`git push <远程仓库名> <本地分支名>:<远程分支名>`

1. 本地分支名 可不写，默认是 **当前分支**；
2. 远程分支 如果不存在，在 push 的时候将自动创建一个远程分支；
3. 将本地仓库`master`分支的更新推送到远程仓库上：`git push origin master`，也可以直接使用`git push origin`，会将本地分支推送到与之存在追踪关系的远程分支；
4. 删除远程`dev`分支：`git push origin --delete dev`。



示例一：

```shell
# 将本地仓库更新 推送到 远程仓库 的 master 分支
zhangjian@zhangjiandeMacBook-Pro Repo % git push origin master
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 244 bytes | 244.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To github.com:zhangjian-ai/Repo.git
 * [new branch]      master -> master  # 此时远程仓库没有 master 分支，就自动创建了一个
```



示例二：

```shell
# push 本地 dev 分支到 远程仓库 dev2 分支。
zhangjian@zhangjiandeMacBook-Pro Repo % git push origin dev:dev2
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 363 bytes | 363.00 KiB/s, done.
Total 4 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'dev2' on GitHub by visiting:
remote:      https://github.com/zhangjian-ai/Repo/pull/new/dev2
remote:
To github.com:zhangjian-ai/Repo.git
 * [new branch]      dev -> dev2
 
# 查看远程仓库，新创建分支 dev2
zhangjian@zhangjiandeMacBook-Pro Repo % git branch -a
* dev
  master
  test
  remotes/origin/dev
  remotes/origin/dev2
  remotes/origin/master
  
# 删除远程仓库分支 dev2
zhangjian@zhangjiandeMacBook-Pro Repo % git push origin --delete dev2
To github.com:zhangjian-ai/Repo.git
 - [deleted]         dev2
 
# 再次查看远程仓库， dev2 分支已被删除
zhangjian@zhangjiandeMacBook-Pro Repo % git branch -a
* dev
  master
  test
  remotes/origin/dev
  remotes/origin/master
```





### git branch

`git branch`命令的作用主要是做 **本地分支** 管理操作。

1. 查看本地分支：`git branch`
2. 查看本地和远程分支：`git branch -a`
3. 基于源分支新建名字为`test`的本地分支，源分支是可选的，如果不写则默认基于master分支创建：`git branch test <源分支>`
4. 将`test`分支名字改为`dev`：`git branch -m test dev`
5. 删除名字为`dev`的本地分支：`git branch -d dev`



示例：

```shell
# 创建 本地分支 test
zhangjian@zhangjiandeMacBook-Pro Repo % git branch test

zhangjian@zhangjiandeMacBook-Pro Repo % git branch
* master
  test
  
# 将`test`分支名字改为`dev`
zhangjian@zhangjiandeMacBook-Pro Repo % git branch -m test dev

zhangjian@zhangjiandeMacBook-Pro Repo % git branch
  dev
* master

# 删除名字为`dev`的分支
zhangjian@zhangjiandeMacBook-Pro Repo % git branch -d dev
Deleted branch dev (was c096fbc).

zhangjian@zhangjiandeMacBook-Pro Repo % git branch
* master
```



### git tag

`git tag`命令主要是对项目标签进行管理。

1. 查看已有的标签历史记录：`git tag`
2. 给当前最新的`commit`打上标签：`git tag <标签的定义>`
3. 给对应的`commit id`打上标签：`git tag <标签定义> <commit id>`



示例：

```shell
# 编辑 web.html 增加一行内容：vi web.html
<p>为tag示例添加一行</p>

# 提交 工作区更新 到 暂存区
zhangjian@zhangjiandeMacBook-Pro Repo % git add web.html

# 提交 提交暂存区更新 到 本地仓库
zhangjian@zhangjiandeMacBook-Pro Repo % git commit -m "add new label for tag"
[master ad39985] add new label for tag
 1 file changed, 1 insertion(+)

# 给 当前最新的 commit 打上 tag
zhangjian@zhangjiandeMacBook-Pro Repo % git tag v1.0.0

# 查看标签
zhangjian@zhangjiandeMacBook-Pro Repo % git tag
v1.0.0

# 提交到远程分支
zhangjian@zhangjiandeMacBook-Pro Repo % git push origin master:master
```



### git checkout

`git checkout`命令最常用的情形是创建和切换分支以及撤销工作区的修改。

1. 切换到`tag`为`v1.0.0`时对应的代码：`git checkout v1.0.0`
2. 在`tag`为`v1.0.0`的基础上创建分支名为`test`的分支：`git checkout -b test v1.0.0`，该命令相当于以下两条命令：
   - `git branch test v1.0.0`：在`v1.0.0`的基础上创建分支`test`
   - `git checkout test`：切换到分支`test`
3. 撤销工作目录中文件的修改（文件有改动但还未执行`git add`）：`git checkout -- fileName`，或者撤销所有修改使用`git checkout .`

**注意：**在 test 分支上进行的修改操作后，若没有使用`git add .`及`git commit`命令把 更新 提交到 本地仓库 ，直接使用 git checkout 切换回 master 分支的话，那么 Git 会将在 test 上的修改一起带到 master 分支。



示例：

```shell
# 基于 tag v1.0.0 创建分支 dev
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout -b dev v1.0.0
Switched to a new branch 'dev'

# 向 web.html 追加如下内容
<p>为checkout示例添加一行</P>

# 查看文档内容
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
<p>为checkout示例添加一行</P>

# 将更新提交到 本地仓库
zhangjian@zhangjiandeMacBook-Pro Repo % git add .
zhangjian@zhangjiandeMacBook-Pro Repo % git commit -m "add one row for checkout"
[dev 15f7d19] add one row for checkout
 1 file changed, 1 insertion(+)
 
# 将 本地仓库 dev 推送到 远程仓库 dev
zhangjian@zhangjiandeMacBook-Pro Repo % git push origin dev
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 323 bytes | 323.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
remote:
remote: Create a pull request for 'dev' on GitHub by visiting:
remote:      https://github.com/zhangjian-ai/Repo/pull/new/dev
remote:
To github.com:zhangjian-ai/Repo.git
 * [new branch]      dev -> dev  # 远程仓库 没有dev分支，就自动创建了一个
 
# 切换 分支到 tag v1.0.0
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout v1.0.0

# 查看文档内容
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
```



### git fetch

`git fetch`命令的作用是将 远程仓库 上的更新同步到 本地仓库，并记录在`.git/FETCH_HEAD`中

1. 同步远程仓库上所有分支的更新：`git fetch origin`
2. 同步远程仓库上`master`分支的更新：`git fetch origin master`
3. 在本地新建`test`分支，并将远程仓库上`master`分支代码下载到本地`test`分支：`git fetch origin master:test`



示例：

```shell
# 在本地新建`test`分支，并将远程仓库上`master`分支代码下载到本地`test`分支
zhangjian@zhangjiandeMacBook-Pro Repo % git fetch origin master:test
From github.com:zhangjian-ai/Repo
 * [new branch]      master     -> test
 
# 切换到 分支 test
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout test
Switched to branch 'test'

# 查看文本
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
```



### git merge/git rebase

`git merge`命令的作用主要是分支的合并。

1. 如果当前是`master`分支，需要合并`dev`分支：`git merge dev`
2. 配合`git fetch`命令，合并 远程分支 的更新 到 本地分支

**注意：**通过`git fetch`所取回的更新，在本地仓库上需要用“远程仓库名/分支名”的形式读取，比如`origin`仓库的`master`分支，就需要用`origin/master`来读取。



示例一：合并 本地仓库 分支 到 本地仓库 分支

```shell
# 切换到 master 分支
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout master
Switched to branch 'master'

# 合并 本地仓库的dev分支 到 master
zhangjian@zhangjiandeMacBook-Pro Repo % git merge dev
Updating ad39985..15f7d19
Fast-forward
 web.html | 1 +
 1 file changed, 1 insertion(+)
 
# 查看文件
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
<p>为checkout示例添加一行</p>
```



示例二：合并 远程分支 到 本地分支

在 GitHub 上更新 远程仓库 dev分支 的文档内容如下：

<img src="./images/git_002.png" style="width: 60%; float: left;">

```shell
# 切换本地仓库分支到 dev
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout dev
Switched to branch 'dev'

# fetch 远程仓库的dev分支
zhangjian@zhangjiandeMacBook-Pro Repo % git fetch origin dev
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
From github.com:zhangjian-ai/Repo
 * branch            dev        -> FETCH_HEAD
   15f7d19..566527a  dev        -> origin/dev
   
# merge 远程dev 到 本地dev
zhangjian@zhangjiandeMacBook-Pro Repo % git merge origin/dev
Updating 15f7d19..566527a
Fast-forward
 web.html | 2 ++
 1 file changed, 2 insertions(+)
 
# 查看文本内容
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
<p>为checkout示例添加一行</p>

<p>在 hub 增加的一行，用于演示 合并 远程分支 到 本地分支</p>
```



**git merge和git rebase的区别**

> git merge和git rebase从最终效果来看没有任何区别，都是将不同分支的代码融合在一起。

1. git log的区别
   - merge：将子分支的所有提交 在主分支记录成一次commit，保留在主分支记录中。
   - rebase：不会在主分支自动生成 commit记录，而是直接将分支中的内容排到master的记录之后。
2. 处理冲突
   - 使用merge命令合并分支，解决完冲突，执行git add .和git commit -m 'fix conflict'。这个时候会产生一个commit。
   - 使用rebase命令合并分支，解决完冲突，执行git add .和git rebase --continue，不会产生额外的commit。这样的好处是，‘干净’，分支上不会有无意义的解决分支的commit；坏处，如果合并的分支中存在多个commit，需要重复处理多次冲突。分支会恢复到rebase开始前的状态 git rebase --abort。

**注意点：**

​		假如使用rebase，一定要遵守rebase黄金法则，共享的public分支不能rebase。通俗的说，当一个分支是一个人开发处理的，才可以rebase，假如一个分支被多个人共享开发，然后rebase，那就乱套了，处理起来复杂。



### git pull

`git pull`命令的作用是获取远程仓库的更新，再与本地分支合并。`git pull <远程仓库名> <远程分支名>:<本地分支名>`

1. 取回远程仓库上的`dev`分支与本地的`master`分支合并：`git pull origin dev:master`
2. 取回远程仓库上的`dev`分支与当前分支合并：`git pull origin dev`，该命令相当于以下两条命令：
   - `git fetch origin dev`：获取远程仓库上`dev`分支的更新
   - `git merge origin/dev`：合并远程`dev`分支到当前分支



示例：

<img src="./images/git_003.png" style="width: 60%; float: left;">

```shell
# 查看当前所在分支，如果不在就切到master
zhangjian@zhangjiandeMacBook-Pro Repo % git branch
  dev
* master
  test
  
# pull 远程仓库的 master 合并到 本地仓库 master
zhangjian@zhangjiandeMacBook-Pro Repo % git pull origin master
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
From github.com:zhangjian-ai/Repo
 * branch            master     -> FETCH_HEAD
   15f7d19..4cf0fcf  master     -> origin/master
Updating 15f7d19..4cf0fcf
Fast-forward
 web.html | 2 ++
 1 file changed, 2 insertions(+)
 
# 查看文本内容
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
<p>为checkout示例添加一行</p>

<p> master 分支添加一行，用于 git pull 示例</p>
```





### git stash

`git stash`命令的作用是保存当前分支工作目录所做的修改。

**即如果当前分支所做的修改你还不想提交，但又需要切换到其他分支去查看，就可以使用该命令。**

1. 保存当前进度：`git stash`
2. 查看已经保存的历史进度记录：`git stash list`
3. 重新应用某个已经保存的进度，并且删除进度记录：`git stash pop <历史进度id>`，
4. 重新应用某个已经保存的进度，但不删除进度记录：`git stash apply <历史进度id>`，如果直接使用`git stash`默认是使用最近的保存
5. 删除某个历史进度：`git stash drop <历史进度id>`
6. 删除所有的历史进度：`git stash clear`



示例：

```shell
# 切换到 test 分支
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout test
Switched to branch 'test'

# 编辑 web.html 追加如下内容：
<p> 为 git stash 添加一行</p>

# 查看 test 分支的文本内容
zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>

<p> 为 git stash 添加一行</p>

# 保存 当前分支的修改
zhangjian@zhangjiandeMacBook-Pro Repo % git stash
Saved working directory and index state WIP on test: ad39985 add new label for tag

# 查看保存记录
zhangjian@zhangjiandeMacBook-Pro Repo % git stash list
stash@{0}: WIP on test: ad39985 add new label for tag

# 切换到 master 分支查看文本内容
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout master
Switched to branch 'master'

zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html  # test 分支的修改没有带到master分支
<p>初始创建文档</p>
<p>为tag示例添加一行</p>
<p>为checkout示例添加一行</p>

<p> master 分支添加一行，用于 git pull 示例</p>

# 再切回 test 分支，并查看文档内容
zhangjian@zhangjiandeMacBook-Pro Repo % git checkout test
Switched to branch 'test'

zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html  # 切回 test 并不会自动应用刚才保存的修改记录
<p>初始创建文档</p>
<p>为tag示例添加一行</p>

# 应用保存的进度，再查看文档内容
zhangjian@zhangjiandeMacBook-Pro Repo % git stash apply stash@{0}

zhangjian@zhangjiandeMacBook-Pro Repo % cat web.html
<p>初始创建文档</p>
<p>为tag示例添加一行</p>

<p> 为 git stash 添加一行</p>
```



### git diff

`git diff` 命令比较文件的不同，即比较文件在暂存区和工作区的差异。

1. 尚未缓存的改动：`git diff [file]`

2. 查看已缓存的改动： `git diff --cached [file]`
3. 查看已缓存的与未缓存的所有改动：`git diff HEAD [file]`
4. 显示摘要而非整个 diff：`git diff --stat [file]`



示例：

```shell
# 查看本地还没执行 git add 的文件的改动
zhangjian@zhangjiandeMacBook-Pro Repo % git diff web.html
diff --git a/web.html b/web.html
index 1f7dba6..84a4dc9 100644
--- a/web.html
+++ b/web.html
@@ -1,2 +1,4 @@
 <p>初始创建文档</p>
 <p>为tag示例添加一行</p>
+
+<p> 为 git stash 添加一行</p>
```



### git rm

git rm 命令用于删除文件。

1. 将文件从暂存区和工作区中删除：`git rm <file>`
2. 如果删除之前修改过并且已经放到暂存区域的话，则必须要用强制删除选项 **-f**：`git rm -f <file> `
3. 如果想把文件从暂存区域移除，但仍然希望保留在当前工作目录中，换句话说，仅是从跟踪清单中删除，使用 **--cached** 选项即可：`git rm --cached <file>`



### git blame

如果要查看指定文件的修改记录可以使用 git blame 命令，格式如下：`git blame <file>`



示例：

```shell
# 可以清晰的看到每一次的修改记录
zhangjian@zhangjiandeMacBook-Pro Repo % git blame web.html
^c096fbc (zhangjian 2021-12-02 18:21:50 +0800 1) <p>初始创建文档</p>
ad39985d (zhangjian 2021-12-02 22:16:06 +0800 2) <p>为tag示例添加一行</p>
15f7d190 (zhangjian 2021-12-02 22:42:21 +0800 3) <p>为checkout示例添加一行</p>
566527a2 (张建      2021-12-02 23:33:55 +0800 4)
566527a2 (张建      2021-12-02 23:33:55 +0800 5) <p>在 hub 增加的一行，用于演示 合并 远程分支 到 本地分支</p>
```



### git submodule

> 该命令的作用主要是在当前主项目中，引入其他的git仓库，这个子仓库作为一个独立的仓库存在于主项目中。适用于主工程中引入其他library库。
>
> 子模块的更新需要在自模块目录下单独执行，主项目的更新提交不会影响子模块的版本，二者相互独立。

#### 添加子模块

执行添加命令成功后，可以在当前路径中看到一个.gitsubmodule文件，里面记录的就是自模块相关的信息

```shell
git submodule add <url> <path>

# url：子模块仓库地址
# path：子模块存放的本地路径

# 如果在添加子模块的时需要指定同步代码的具体分之，可以利用 -b 参数
git submodule add -b <branch> <url> <path>
```



#### 初始化

当我们add子模块之后，会发现文件夹下没有任何内容。这个时候我们需要再执行下面的指令添加源码。

```shell
# 进入到子模块目录下执行下面的命令，即 add 时的 path
git submodule update --init --recursive
```

这个命令是下面两条命令的合并版本

```shell
git submodule init
git submodule update
```



#### 更新

引入了别人的仓库后，如果该仓库作者进行了更新，我们需要手动进行同步更新

```shell
# 进入子模块目录执行
git pull
```



#### 删除

1. 删除子模块目录及源码`rm -rf 子模块目录`
2. 删除.gitmodules中的对应子模块内容`vi .gitmodules`
3. 删除.git/config配置中的对应子模块内容`vi .git/config`
4. 删除.git/modules/下对应子模块目录`rm -rf .git/modules/子模块目录`
5. 删除git索引中的对应子模块`git rm --cached 子模块目录`



# Docker

## Docker 命令

### 基础命令

```shell
docker search mysql															# 搜索官方仓库中 mysql 相关的镜像
docker pull ${CONTAINER NAME}                    #拉取镜像。如果镜像前没有指定仓库，那么久默认到官方仓库拉取镜像
docker images                                    #查看本地所有镜像
docker ps                                        #查看所有正在运行的容器，加-q则只返回id
docker ps -a                                     #查看所有容器，加-q则只返回id
docker rmi ${IMAGE NAME/ID}                      #删除镜像
docker rm ${CONTAINER NAME/ID}                   #删除容器
docker save ${IMAGE NAME} > ${FILE NAME}.tar     #将镜像保存成文件
docker load < ${FILE NAME}.tar                   #从文件加载镜像
docker start/restart ${CONTAINER NAME/ID}        #启动/重启一个以前运行过的容器
docker stop ${CONTAINER NAME/ID}                 #停止一个正在运行的容器

docker logs ${CONTAINER NAME/ID}                 #显示运行容器的日志
		##查看redis容器日志，默认参数
		docker logs rabbitmq
		##查看redis容器日志，参数：-f  跟踪日志输出；-t   显示时间戳；--tail  仅列出最新N条容器日志；
		docker logs -f -t --tail=20 redis
		##查看容器redis从2019年05月21日后的最新10条日志。
		docker logs --since="2019-05-21" --tail=10 redis

docker run [选项参数] ${IMAGE NAME} [命令行参数]    #运行一个容器
    --name ${container name}                          #设置容器名称
    -p ${host port}:${container port}                 #映射主机和容器内的端口
    -e ${env name}=${env value}                       #添加环境变量
    -d                                                #后台运行
    -v ${host folder path}:${container folder path}   #将主机目录挂在到容器内
    --restart=always																	#容器随系统自启
    	no – 默认值，如果容器挂掉不自动重启
			on-failure – 当容器以非 0 码退出时重启容器，同时可接受一个可选的最大重启次数参数 (e.g. on-failure:10)
			always – 不管退出码是多少都要重启
			
		--link <origin container name/id>:alias				# 让容器之间即便不对外暴露端口，也可以实现通信
			# 创建并启动名为selenium_hub的容器
			docker run -d --name selenium_hub selenium/hub
			
			# 创建并启动名为node的容器，并把该容器和名为selenium_hub的容器链接起来。
			docker run -d --name node --link selenium_hub:hub selenium/node-chrome-debug
			
			# 说明：
			# 		selenium_hub是上面启动的1cbbf6f07804（容器ID）容器的名字，这里作为源容器，hub是该容器在link下的别名（alias），通					俗易懂的讲，站在node容器的角度，selenium_hub和hub都是1cbbf6f07804容器的名字，并且作为容器的hostname，node用这2个名					字中的哪一个都可以访问到1cbbf6f07804容器并与之通信（docker通过DNS自动解析）。
```



### 高级命令

```shell
docker ps -f "status=exited"                                   #显示所有退出的容器
docker ps -a -q                                                #显示所有容器id
docker ps -f "status=exited" -q                                #显示所有退出容器的id
docker restart $(docker ps -q)                                 #重启所有正在运行的容器
docker stop $(docker ps -a -q)                                 #停止所有容器
docker rm $(docker ps -a -q)                                   #删除所有容器
docker rm $(docker ps -f "status=exited" -q)                   #删除所有退出的容器
docker rm $(docker stop $(docker ps -a -q))                    #停止并删除所有容器
docker start $(docker ps -a -q)                                #启动所有容器
docker rmi $(docker images -a -q)                              #删除所有镜像

docker top ${CONTAINER NAME/ID}                                #显示一个容器的top信息

docker kill -s KILL [container id]														# 杀死一个或多个指定容器进程

docker stats                                                   #显示容器统计信息(正在运行)
    docker stats -a                                            #显示所有容器的统计信息(包括没有运行的)
    docker stats -a --no-stream                                #显示所有容器的统计信息(包括没有运行的) ，只显示一次
    docker stats --no-stream | sort -k8 -h                     #统计容器信息并以使用流量作为倒序
    
docker system 
      docker system df           #显示硬盘占用
      docker system events       #显示容器的实时事件
      docker system info         #显示系统信息
      docker system prune        #清理文件
      
docker build      
    # 构建docker镜像 -f 指定 Dockerfile 文件；-t 指定镜像名称及tag
    docker build -f /docker/dockerfile/mycentos -t mycentos:1.1
    
    # 如果当前目录下存在名为 Dockerfile 的文件，那么可以向下面这样构建。注意： . 表示当前目录，其他目录同理
    docker build -t xx/gitlab .			# 构建时，可以指定镜像仓库（XX），不指定 tag 时，使用latest作为tag
    
docker commit
		# 将运行中的容器打包成一个镜像
		# 参数：-a 提交的镜像作者；-c 使用Dockerfile指令来创建镜像；-m :提交时的说明文字；-p :在commit时，将容器暂停
		docker commit -m "描述信息" 容器名/容器ID 镜像名:镜像Tag 
		docker commit -m "description info" TP_web web:latest

docker push
		# 将本地镜像push到仓库之前，要保证镜像已经指定归属仓库并打了tag。如下，给一个镜像指定仓库
		docker tag nginx:latest zhangjian1/nginx:latest
		
		# push 到Hub仓库 zhangjian1，这里需要客户端登陆
		docker login --username=[username] --password=[password]
		
		# push 镜像。
		docker push zhangjian1/nginx:latest
		
docker cp
		##将rabbitmq容器中的文件copy至本地路径
		docker cp rabbitmq:/[container_path] [local_path]
		
		##将主机文件copy至rabbitmq容器的目录中（以/结尾表示目录）
		docker cp [local_path] rabbitmq:/[container_path]/
		
		##将主机文件copy至rabbitmq容器，目录重命名为[container_path]（注意与非重命名copy的区别）
		docker cp [local_path] rabbitmq:/[container_path]
		
docker exec
		# 参数：-i  交互式模式；-t  分配一个伪终端
		docker exec -it ${CONTAINER NAME/ID} /bin/bash                 #进入容器内。/bin/bash 表示伪终端使用的shell程序
		
		# 以交互模式在容器中执行命令，结果返回到当前终端屏幕
		docker exec -i -t centos ls -l /tmp
		
		# 以分离模式在容器中执行命令，程序后台运行，结果不会反馈到当前终端
		docker exec -d centos touch cache.txt 
		
docker network
		# 查看网络连接
		docker network ls
		
		# 检查网络连接详情
		docker network inspect 网络名称/网络ID
		
		# 容器连接网络
		docker network connect <network> <container>
		
		# 容器断开网络连接，-f 表示强制
		docker network disconnect [-f] <network> <container>
		
		# 创建网络
		docker network create <network>
		# 创建网络，指定子网网段和网关。demo_02 就是 网络的名字。通过 docker network inspect demo_02 即可查看新建网络详情
		docker network create --subnet 172.36.0.0/24 --gateway 172.36.0.1 demo_02
		
		# 删除网络
		docker network rm <network>
		
		# 删除所有没有使用的网络
		docker network prune
```



## Docker 进阶

### Dockerfile 语法

> ##  FROM
>
> 格式：
>
> - `FROM \<image\>`
> - `FROM \<image\>:\<tag\>`
> - `FROM \<image\>@\<digest\>`
>
> Dockerfile中的第一条指令必须是FROM，FROM指令指定了构建镜像的base镜像
>
> ## MAINTAINER
>
> 格式：`MAINTAINER \<name\> \<Email\>`
>
> 编写维护Dockerfile的作者信息
>
> ## ENV
>
> 格式：
>
> - `ENV \<key\>\<value\>`
> - `ENV \<key\>=\<value\>`
>
> 为容器声明环境变量，环境变量在子镜像中也可以使用。可以直接使用环境变量$variable_name 运行容器指定环境变量：`docker run --env <key>=<value>`
>
> ## RUN
>
> 格式：
>
> - `RUN \<command\>` (类似`/bin/sh -c`shell格式)
> - `RUN ["executable", "param1", "param2"]` (exec格式)
>
> **第一种** 使用shell格式时，命令通过`/bin/sh -c`执行;
>
> **第二种** 使用`exec`格式时，命令直接执行，容器不调用shell，并且`exec`格式中的参数会看作是`JSON` 数组被Docker解析，所以要用(")双引号，不能用单引号(')。
>
> 举例： `RUN [ "echo", "$HOME" ]`$HOME变量不会被替换,如果你想运行shell程序，使用：`RUN [ "sh", "-c", "echo", "$HOME" ]`
>
> ## COPY
>
> 格式：COPY <src><dest>
>
> 拷贝本地<src>目录下的文件到容器中<dest>目录。
>
> ## ADD
>
> 格式：
>
> - ADD <src><dest>
> - ADD ["",... ""]
>
> `ADD hom* /mydir/` 从<src>目录下拷贝文件，目录或网络文件到容器的<dest>目录。和COPY非常相似，但比COPY功能多，拷贝的文件可以是一个网络文件，并且ADD有解压文件的功能，目前好像只能解压tar文件。
>
> ## CMD
>
> 格式：
>
> - `CMD \<commadn\> param1 param2`(shell格式)
> - `CMD ["executable", "param1", "param2"]` （exex格式）
> - `CMD ["param1", "param2"]`（为ENTRYPOINT命令提供参数）
>
> 虽然有三种格式，但在Dockerfile中如果有多个CMD命令，只有最后一个生效。
>
> `CMD`命令主要是提供容器运行时得默认值。默认值，可以是一条指令，也可以是参数（ENTRYPOINT），`CMD`命令参数是一个动态值，信息会保存到镜像的JSON文件中。
>
> 举例：
>
> ```
> ENTRYPOINT ["executable"]
> CMD ["param1", "param2"]
> ```
>
> 启动容器执行：`["executable", "param1", "param2"]` **注意：** 如果在命令行后面运行`docker run`时指定了命令参数，则会把`Dockerfile`中定义的`CMD`命令参数覆盖
>
> ## ENTRYPOINT
>
> 格式：
>
> - `ENTRYPOINT \<command\>` (shell格式)
> - `ENTRYPOINT ["executable", "param1", "param2"]`（exec格式）
>
> `ENTRYPOINT`和`CMD`命令类似，也是提供容器运行时得默认值，但它们有不同之处。同样一个Dockerfile中有多个ENTRYPOINT命令，只有最后一个生效。
>
> - 当`ENTRYPOINT`命令使用<commmand>格式，`ENTRYPOINT`会忽略任何`CMD`指令和`docker run `传来的参数，直接运行在`/bin/sh -c`中;也就是说`ENTRYPOINT`执行的进程会是`/bin/sh -c`的**子进程**。所以进程的PID不会是1，而且也不能接受Unix信号。（执行docker stop $container_id的时候，进程接收不到SIGTERM信号）
> - 使用`exec`格式，`docker run`传入的命令参数会覆盖`CMD`命令，并附加到`ENTRYPOINT`命令的参数中。推荐使用`exec`方式
>
> ## ONBUILD
>
> 格式：`ONBUILD [INSTRUCTION]`
>
> `ONBUILD`指令的功能是添加一个将来执行触发器指令到镜像中。当Dockerfile中`FROM`的镜像中包含`ONBUILD`指令，在构建此镜像的时候会触发`ONBUILD`指令。但如果当前Dockerfile中存在`ONBUID`指令，不会执行就。`ONBUILD`指令在生成**应用镜像**时用处非常大。
>
> **`ONBUILD`如何工作**
>
> 1.构建过程中，`ONBUILD`指令会添加到触发器指令镜像元数据中。触发器指令不会在当前构建过程中生效
>
> 2.构建完后，触发器指令会被保存到镜像的详情中，主键是`OnBuild`，可以使用`docker inspect`命令查看到
>
> 3.之后此镜像可能是构建其他镜像的父镜像，在构建过程中，`FROM`指令会查找`ONBUILD`触发器指令，并按照之前定义的顺序执行；如果触发器指令执行失败，则构建新镜像失败并退出；如果触发器指令执行成功，则继续往下执行。
>
> 4.构建成功后`ONBUILD`指令清除，固不会被孙子辈镜像继承。
>
> ## VOLUME
>
> 格式：`VOLUME ["/data"]`
>
> 为docker主机和容器做目录映射，volume目录信息会保存到镜像的JSON文件中，在运行`docker run`命令时指定`$HOST_DIR`
>
> ## LABEL
>
> 格式：`LABEL <key>=<value> <key>=<value> <key>=<value> ...`
>
> LABEL指令，添加一个元数据到镜像中。一个镜像中可以有多个标签，建议写一个（因为没多个LABEL指令镜像会多一个`layer`）`LABEL`是一个键值对<key><value>，在一个标签值,包括空间使用引号和反斜杠作为您在命令行解析。 举例： `LABEL multi.label1="value1" multi.label2="value2" other="value3"`
>
> ## EXPOSE
>
> 格式：`EXPOSE <port> [<port>...]`
>
> 在Dockerfile中定义端口，默认是不往外暴露，在运行`docker run ``-p` or `-P`暴露
>
> ## USER
>
> 格式：`USER daemon`
>
> 设定一个用户或者用户ID,在执行`RUN``CMD``ENTRYPOINT`等指令时指定以那个用户得身份去执行
>
> ## WORKDIR
>
> 格式：`WORKDIR /path/to/workdir`
>
> 当执行`RUN``CMD``ENTRYPOINT``ADD``CMD`等命令，设置工作目录
>
> ## .dockerignore
>
> 如果在Dockerfile文件目录下有.dockerignore文件，docker在构建镜像的时候会把在.dockerignore文件中定义的文件排除出去
>
> ```shell
> */temp*
> */*/temp*
> temp?
> *.md
> !LICENSE.md
> ```



### Docker 底层原理

#### docker 进程与宿主机如何实现隔离

命名空间 (namespaces) 是 Linux 为我们提供的用于分离进程树、网络接口、挂载点以及进程间通信等资源的方法。在日常使用 Linux 或者 macOS 时，我们并没有运行多个完全分离的服务器的需要，但是如果我们在服务器上启动了多个服务，这些服务其实会相互影响的，每一个服务都能看到其他服务的进程，也可以访问宿主机器上的任意文件，这是很多时候我们都不愿意看到的，我们更希望运行在同一台机器上的不同服务能做到完全隔离，就像运行在多台不同的机器上一样。

**Docker 其实就通过 Linux 的 Namespaces 对不同的容器实现了隔离。**

Linux 的命名空间机制提供了以下七种不同的命名空间，包括 `CLONE_NEWCGROUP`、`CLONE_NEWIPC`、`CLONE_NEWNET`、`CLONE_NEWNS`、`CLONE_NEWPID`、`CLONE_NEWUSER` 和 `CLONE_NEWUTS`，通过这七个选项我们能在创建新的进程时，设置新进程应该在哪些资源上与宿主机器进行隔离。



#### Docker 容器与传统 VM 虚拟机的区别

容器与 虚拟机  有着类似的资源隔离和分配的优点，但拥有不同的架构方法，容器架构更加便携，高效。

| 特性       | 虚拟机的架构 | 容器的架构     |
| ---------- | ------------ | -------------- |
| 启动       | 分钟级       | 秒级           |
| 性能       | 弱于原生     | 接近原生       |
| 硬盘使用   | 一般为GB     | 一般为MB       |
| 系统支持量 | 一般几十个   | 单机上千个容器 |

**区别：**

- 传统虚拟化是在硬件层面实现虚拟化，需要有额外的虚拟机管理应用和虚拟机操作系统层；
- 而 Docker容器 是在操作系统层面实现虚拟化，直接复用本地主机操作系统，更加轻量级。



**虚拟机的架构：** 

每个虚拟机都包括应用程序、必要的二进制文件和库以及一个完整的客户操作系统(Guest OS)，尽管它们被分离，它们共享并利用主机的硬件资源，将近需要十几个 GB 的大小。

<img src='./images/docker_001.png' style='width: 45%; float: left'>



**容器的架构：** 

容器包括应用程序及其所依赖的二进制文件及库文件，但与其他容器共享操作系统内核。它们以独立的用户空间进程形式运行在主机操作系统上。他们也不依赖于任何特定的基础设施，Docker 容器可以运行在任何计算机上，任何基础设施和任何云上。

<img src='./images/docker_002.png' style='width: 45%; float: left'>



Docker 的容器利用了 LXC，管理利用 namespaces 来做权限的控制和隔离，利用 cgroups（control groups） 来进行资源的配置，并且还通过 aufs 来进一步提高文件系统的资源利用率，而这些技术都不是 Docker 独创。

LXC 与虚拟机的不同之处在于，它是一个操作系统级别的虚拟化环境，而不是硬件虚拟化环境。他们都做同样的事情，但 LXC 是操作系统级别的虚拟化环境，虚拟环境有它自己的进程和网络空间，而不是创建一个完整成熟的虚拟机。因此，一个 LXC 虚拟操作系统具有最小的资源需求，并启动只需几秒钟。





# Kubernates

## 常用命令

### 查询类命令

```shell
# 获取节点和服务版本信息
kubectl get nodes
# 获取节点和服务版本信息，并查看附加信息
kubectl get nodes -o wide
# 获取pod信息，默认是default名称空间
kubectl get pod
# 获取pod信息，默认是default名称空间，并查看附加信息【如：pod的IP及在哪个节点运行】
kubectl get pod -o wide
# 获取指定名称空间的pod
kubectl get pod -n <namespaces>
# 获取指定名称空间中的指定pod
kubectl get pod podName -n <namespaces>
# 获取所有名称空间的pod
kubectl get pod -A 
# 查看pod的详细信息，以yaml格式或json格式显示
kubectl get pods -o yaml
kubectl get pods -o json

# 查看pod的标签信息
kubectl get pod -A --show-labels 
# 根据Selector（label query）来查询pod
kubectl get pod -A --selector="k8s-app=kube-dns"

# 查看运行pod的环境变量
kubectl exec podName env
# 查看指定pod的日志
kubectl logs -f --tail 500 -n <namespaces> <podname>
 
# 查看所有名称空间的service信息
kubectl get svc -A
# 查看指定名称空间的service信息
kubectl get svc -n <namespaces>

# 查看componentstatuses信息
kubectl get cs
# 查看所有configmaps信息
kubectl get cm -A
# 查看所有serviceaccounts信息
kubectl get sa -A
# 查看所有daemonsets信息
kubectl get ds -A
# 查看所有deployments信息
kubectl get deploy -A
# 查看所有replicasets信息
kubectl get rs -A
# 查看所有statefulsets信息
kubectl get sts -A
# 查看所有jobs信息
kubectl get jobs -A
# 查看所有ingresses信息
kubectl get ing -A
# 查看有哪些名称空间
kubectl get ns

# 查看pod的描述信息
kubectl describe pod <podName>
kubectl describe pod -n <namespaces> <podname>

# 查看node或pod的资源使用情况
# 需要heapster 或metrics-server支持
kubectl top node
kubectl top pod 

# 查看指定命令空间下指定pod下的容器信息
kubectl describe pod <podname> -n <namespaces> |grep container

# 查看集群信息
kubectl cluster-info   或  kubectl cluster-info dump

# 查看各组件信息【172.16.1.110为master机器】
kubectl -s https://172.16.1.110:6443 get componentstatuses
```



### 操作类命令

```shell
# 创建资源
kubectl create -f xxx.yaml

# 应用资源
kubectl apply -f xxx.yaml

# 应用资源，该目录下的所有 .yaml, .yml, 或 .json 文件都会被使用
kubectl apply -f <directory>

# 创建test名称空间
kubectl create namespace test

# 删除资源
kubectl delete -f xxx.yaml
kubectl delete -f <directory>

# 删除指定的pod
kubectl delete pod podName

# 删除指定名称空间的指定pod
kubectl delete pod -n <namespaces> podName

# 删除其他资源
kubectl delete svc svcName
kubectl delete deploy deployName
kubectl delete ns nsName

# 强制删除
kubectl delete pod podName -n nsName --grace-period=0 --force
kubectl delete pod podName -n nsName --grace-period=1
kubectl delete pod podName -n nsName --now

# 编辑资源
kubectl edit pod podName -n <namespaces>
```



### 进阶类命令

```shell
# kubectl exec：进入pod启动的容器
kubectl exec -it podName -n <namespaces> /bin/sh    #进入容器
kubectl exec -it podName -n <namespaces> /bin/bash  #进入容器

# kubectl label：添加label值
kubectl label nodes k8s-node01 zone=north  #为指定节点添加标签 
kubectl label nodes k8s-node01 zone-       #为指定节点删除标签
kubectl label pod podName -n nsName role-name=test    #为指定pod添加标签
kubectl label pod podName -n nsName role-name=dev --overwrite  #修改lable标签值
kubectl label pod podName -n nsName role-name-        #删除lable标签

# kubectl滚动升级； 
通过 kubectl apply -f myapp-deployment-v1.yaml 启动deploy
kubectl apply -f myapp-deployment-v2.yaml     #通过配置文件滚动升级
kubectl set image deploy/myapp-deployment myapp="registry.cn-beijing.aliyuncs.com/google_registry/myapp:v3"   #通过命令滚动升级
kubectl rollout undo deploy/myapp-deployment 或者 kubectl rollout undo deploy myapp-deployment    #pod回滚到前一个版本
kubectl rollout undo deploy/myapp-deployment --to-revision=2  #回滚到指定历史版本

# kubectl scale：动态伸缩
kubectl scale deploy myapp-deployment --replicas=5 
#动态伸缩【根据资源类型和名称伸缩，其他配置「如：镜像版本不同」不生效】
kubectl scale --replicas=8 -f myapp-deployment-v2.yaml  
```

