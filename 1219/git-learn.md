你已经知道，每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。
截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即master分支。
HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，HEAD指向的就是当前分支。

开始的时候，master分支是一条线，Git用master指向最新的提交，再用HEAD指向master，就能确定当前分支，以及当前分支的提交点。

查看 分支 操作过程
git log --graph --pretty=oneline --abbrev-commit

查看当前分支及所有分支
git branch 

新建分支并切换
git checkout -b 

删除分支
git checkout -d

强行删除
branch -D <name>

合并分支
git merge 

不是快速合并
git merge --no-ff -m "master merge dev readme" dev

隐藏  #Git还提供了一个stash功能，可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作
git stash

查看隐藏的空间
git stash list

恢复隐藏空间
1.一是用git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除
2.git stash pop 恢复的同时把stash内容也删

可以多次隐藏空间 stash 恢复的时候先用git stash list查看
git stash apply stash@{0}

查看远程库的信息
git remote

远程详细信息 有push 的是有推代码的权限
git remote -v

不是一定要把本地分支往远程推送
1.master分支是主分支，因此要时刻与远程同步
2.dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
3.bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
4.feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。


协同开发时：
要在dev分支上开发，就必须创建远程origin的dev分支到本地，于是他用这个命令创建本地dev分支：
git checkout -b dev origin/dev

当同时修改统一文件时冲突，不能正常提交
git pull
git pull 拉去远程仓库代码错误时，应该本地dev分支与远程origin/dev分支的链接，
设置dev和origin/dev的链接：
git branch --set-upstream-to=origin/dev dev

打标签 创建带有说明的标签，用-a指定标签名，-m指定说明文字：
git tag v1.0
git tag -a v0.1 -m "version 0.1 released" 1094adb

查看标签
git tag

历史提交记录 commit
git log --pretty=oneline --abbrev-commit

补打标签
git tag v0.9 f52c633

注意标签不是按时间顺序列出，而是按字母排序的
git show <tagname>查看标签信息

删除标签
git tag -d v0.1

推送标签到远程
git push origin v1.0

一次性推送全部尚未推送到远程的本地标签
git push origin --tags

删除远程的tag
1.先删本地 git tag -d v0.9
2.删远程 git push origin :refs/tags/v0.9

确实想添加该文件，可以用-f强制添加到Git：
git add -f App.class

配置别名
敲git st就表示git status那就简单多了，当然这种偷懒的办法我们是极力赞成的。
我们只需要敲一行命令，告诉Git，以后st就表示status：
git config --global alias.st status

git lg
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"





