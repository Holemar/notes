
一、概括
    1.源码：http://git-scm.com/download
    2.在 Mac 上安装： http://code.google.com/p/git-osx-installer/
    3.在 Windows 上安装： http://code.google.com/p/msysgit
    4.在 linux 上安装,命令行输入: sudo apt-get install git

    参考文档：http://progit.org/book/zh/

    真实常用操作:
        0. git clone ssh://git@git.xxx.com:18122/holemar/program_name.git
        1. git checkout develop  # 切换到此分支
        #2. git pull origin master # 把主分支的代码 pull 下来，且合并到此分支
        2. git pull origin develop # 把 develop 分支的代码 pull 下来

        3. 修改代码...
           git status  # 文件被修改，需要查看情况
           git diff <filename> # 文件修改情况

           git stash # 临时挂起，不提交而拉取新代码
           git stash apply # 恢复未提交前的编辑状态

           git add . # 如果有新增文件，可以按文件名添加，也可以用 . 一次性添加所有
        4. git commit -am "查看页面不强制要求登录"  # 提交代码
        5. git push origin develop # 推送代码到服务器
        6. 提交后需要到网站上进行 pull reuqest

        7. git checkout master  # 切换到此分支
        8. git pull origin master  # pull 代码下来(自动合并到本地),这是更新 master 分支的代码
           git fetch origin # fetch 拉代码下来，但不自动合并。 git pull = git fetch + git merge
        9. git rebase origin/master # 与主干同步
        10. git merge develop  # 将 develop 的工作分支合并到当前分支
            有冲突则手动解决,且需要 commit
        10. git rebase --continue # rebase 后解决冲突
        11. git push origin master # 推送代码到服务器
            git push --force origin myfeature # rebase 后，分支不能正常推时，需要强推上去
        12. git log  # 查看log
        13. git fetch origin <远程分支名称>:<本地分支名称>  # 在本地新建分支x，但是不会自动切换到该本地分支x，需要手动checkout
        14. git cherry-pick abce00c8 # 只合并某个提交(其它提交的内容不合并,需要先checkout到被合并的分支上，后面一个参数是提交编码的前8位或者完整编码)
        15. git rebase master # 会将当前分支(develop)的提交复制到指定的分支(master)之上。类似 merge

    常用命令：
        $ git init   # 初始化 git 仓库(需要先进入到仓库目录)
        $ git --bare init # 创建一个纯粹(bare)的代码仓库(服务器用)
        $ git status   # 查看当前 track 状态
        $ git add .   # 添加所有新增文件
        $ git commit -am "init"   # 提交, 必须提供一个注释, 否则无法执行。引号里面的内容是提交时的注释内容
        $ git commit --amend -am "a.txt"  # 重新提交, 替换上次提交的注释
        $ git clone git@192.168.1.202:/var/git.server/project1  # 克隆一份项目下来
        $ git pull origin master  # pull 代码下来
        $ git push origin master  # push 代码上去
        $ git push --force origin master # 强行把本地版本推到服务器上
        $ git ls-files -v | grep settings.py  # 查看某文件是否被忽略(正常的显示“H”开头, 被忽略的“S”开头)
        $ git update-index --skip-worktree web/mvc/cloud/settings.py # 忽略某文件的修改, 不提交
        $ git update-index --no-skip-worktree web/mvc/cloud/settings.py # 恢复某文件的提交, 以上面的相对
        $ git reset --hard origin/master  # 撤销本地、暂存区、版本库(用远程服务器的origin/master替换本地、暂存区、版本库)

        $ git log   # 查看提交日志
        $ git log -3 # 查看最后 3 条提交信息
        $ git log -3 --stat  # 显示简单的提交统计信息
        $ git log -1 -p  # 显示修改的详细信息
        $ git log 标签值  # 用标签显示提交状态

        $ git branch <name>  # 创建新的分支
        $ git branch <name> HEAD^  # 创建不以当前版本为起点的分支
        $ git branch   # 查看本地所有分支
        $ git branch -r  # 查看所有远程分支
        $ git branch -a  # 查看远程和本地所有分支
        $ git branch -d <name>  # 删除工作分支
        $ git branch -D <name> # 强制删除分支(本地,未合并的分支)
        $ git push origin :<name>  # 删除远程分支

        $ git checkout <name>   # 切换到新的工作分支
        $ git checkout -b <name>  # 一次完成创建和切换分支的工作
        $ git checkout -b <本地分支名称> origin/<远程分支名称>  # 创建并切换到远程分支
        $ git fetch origin <远程分支名称>:<本地分支名称>  # 在本地新建分支x，但是不会自动切换到该本地分支x，需要手动checkout
        $ git checkout HEAD^ -- <filename>  # 恢复某文件
        $ git checkout <filename> # 恢复某文件到线上最新版本

        $ git stash # 临时挂起，不提交而拉取新代码
        $ git stash apply # 恢复未提交前的编辑状态

        $ git merge <name>  # 将 新分支名 的工作分支合并到当前分支
        $ git cherry-pick abce00c8 # 只合并某个提交(其它提交的内容不合并,需要先checkout到被合并的分支上，后面一个参数是提交编码的前8位)

        $ git reset HEAD^ <file> # 恢复到上次某个提交状态, 可以是 HEAD^、HEAD~4、commit-id 的头几个字母, 还可以是 tag
        $ git reset --hard 17ccc1b2(版本id) # 回退到某版本
        $ git tag 标签值  # 创建简单标签
        $ git tag  # 显示所有标签
        $ git show --stat 标签值  # 用标签显示提交基本信息
        $ git rm INSTALL  # 删除文件,git里的删除
        $ git show <filename>   # 查看提交版本的具体信息
        $ git show HEAD^ <filename>   # 查看历史提交版本的具体信息
        $ git diff HEAD <filename>  # 查看工作目录和暂存区的差异
        $ git diff HEAD --staged <filename>  # 查看暂存区和代码仓库的差异
        $ git diff HEAD --cached <filename>  # 查看暂存区和代码仓库的差异
        $ git config --global user.name "Q.yuhen"  # 添加变量到配置档： user.name=Q.yuhen
        $ git config --list  # 查看全局设置
        $ git fsck  # 检查损坏情况
        $ git gc  # 清理无用数据
        $ git rebase [startpoint] [endpoint] --onto [branchName]  # 将当前分支的指定区间(startpoint ~ endpoint)的几个提交复制到 branchName 分支上

        在 Git 中 "HEAD" 表示仓库中最后一个提交版本, "HEAD^" 是倒数第二个版本, "HEAD~2" 、"HEAD~4"则是更老的版本。


二、基础命令
    1.创建项目目录, 建立 Git 仓库。
        $ mkdir myproject
        $ cd myproject
        $ git init # 初始化 git 仓库
        Initialized empty Git repository in /home/yuhen/myproject/.git/

      从此, myproject 就是工作目录, 而 git 创建的 .git 隐藏目录就是代码仓库了。
      所有 Git 需要的数据和资源都存放在这个目录中。


    2. 建立忽略配置文件。
        $ cat > .gitignore << end  # 在 git 工作的首目录下, 创建一个“.gitignore”文件, 在里面写内容
        > *.[oa]
        > *.so
        > *~
        > !a.so
        > test
        > tmp/
        > end

      支持匹配符和正则表达式, 支持 "#" 注释, 支持用 "/" 结尾表示路径。
      还可以用 "!" 取反, 比如前面的 "*.so" 规则忽略所有 .so 文件, 然后用 "!a.so" 表示特例。等等...

      注：此配置文件会提交到服务器的, 只用来忽略 log 文件、编译文件等不需要提交到服务器的文件。
      如果是需要提交到服务器, 但又不需要把自己修改的也提交上去的话(如配置文件等), 可修改 .git/info/exclude 文件, 写法同 .gitignore 文件。


    3. commit
        $ git status # 查看当前 track 状态
        $ git add . # 添加所有新增文件
        $ git commit -am "init" # 提交必须提供一个注释, 否则无法执行。引号里面的内容是提交时的注释内容。
        $ git log # 查看提交日志


    4. 创建工作分支。
        $ git branch yuhen # 创建新的分支
        $ git branch # 查看当前所有分支
        * master  # *号表示正在使用中的
          yuhen

        $ git checkout yuhen # 切换到新的工作分支
        Switched to branch 'yuhen'

        $ git branch # 确认一下
          master
        * yuhen

      也可以用 "git checkout -b yuhen" 一次完成创建和切换分支的工作。
        $ git checkout -b yuhen
        Switched to a new branch 'yuhen'

        $ git branch
          master
        * yuhen

      使用 "git branch <name>" 创建分支
      还可以创建不以当前版本为起点的分支 "git branch <name> HEAD^"。


    5. 合并工作分支到 master。
        $ git checkout master # 切换回主分支
        Switched to branch 'master'

        $ git branch
        * master
          yuhen

        $ git merge yuhen # 将 yuhen 工作分支合并到主分支

        $ git branch -d yuhen # 删除工作分支
        Deleted branch yuhen (was 42d7d10).

      用一个分支进行工作是个好主意, 因为 git 有句话叫做 "丢掉一个烂摊子总比收拾一个烂摊子强"。


    6. 如果我们发现某次提交有问题, 我们可以恢复到以前的某个提交版本。
        $ git reset HEAD^ # 恢复到上次某个提交状态, 可以是 HEAD^、HEAD~4、commit-id 的头几个字母, 还可以是 tag。

        $ git status # 看到没有, 默认 reset 模式是 --mixed, 会保留文件修改。还可以用 --hard 放弃这些修改。

        # 文件修改还被保留着呢。


    7.工作了 n 天了, 总算进入某个阶段性版本了。
        $ git tag v0.9 # 创建简单标签
        $ git tag # 显示所有标签
        v0.9

        $ git log v0.9 # 用标签显示提交状态
        $ git show --stat v0.9 # 用标签显示提交基本信息


三、Git Tips
    1. 删除文件
        除了用 "rm" 删除工作目录中的文件外, 还得用 "git rm <file>" 删除代码仓库中的文件。

        $ rm INSTALL

        $ git status
        $ git rm INSTALL
        rm 'doc/INSTALL'

        $ git commit -am "rm INSTALL"

      当然, 版本管理工具的一个好处就是有后悔药卖。
        $ git checkout HEAD^ -- INSTALL

        $ ls
        INSTALL  README

      如果仅此仓库移除, 但保留工作目录中的文件, 可以直接用 "git rm --cached <file>", 遗留的文件会变成未跟踪状态。



    2. 移动文件
        和删除文件的做法类似。

        $ mv HISTORY doc/

        $ git status
        $ git add .

        $ git commit -am "mv HISTORY"
        [master 716af03] mv HISTORY
         1 files changed, 0 insertions(+), 0 deletions(-)
         rename HISTORY => doc/HISTORY (100%)


    3. 重新提交
        如果最后一次的提交需要修正什么, 那么可以用 "--amend" 参数。

        $ touch a.txt
        $ git add .
        $ git commit -am "b.txt"
        很显然, 注释 "b.txt" 写错了。重来吧~~~

        $ git commit --amend -am "a.txt"

        $ git log
        最后一条提交日志被替换了。


    4. 恢复 \ 撤销
        可以用 "git checkout ..." 签出以前的某个 "提交版本" 。

        $ cat main.c # 修改文件
        $ git show HEAD^ main.c
        $ git checkout HEAD^ -- main.c

        $ cat main.c # 显示修改前的内容
        也可以用 "git reset HEAD <file>" 重置已添加到暂存区(stage)但未提交(commit)的文件。


        作为代码管理工作, 我们随时可以 "反悔"。
        使用 "git reset HEAD <filename>" 命令可以取消暂存区的文件快照(即恢复成最后一个提交版本), 这不会影响工作目录的文件修改。
        使用 "git checkout -- <filename>" 可以使用暂存区快照恢复工作目录文件, 工作目录的文件修改被抛弃。

        $ git chekcout -- readme

        在 Git 中 "HEAD" 表示仓库中最后一个提交版本, "HEAD^" 是倒数第二个版本, "HEAD~2" 则是更老的版本。
        我们可以直接 "签出" 代码仓库中的某个文件版本到工作目录, 该操作同时会取消暂存区快照。
        $ git checkout HEAD^ readme

        如果想将整个项目回溯到以前的某个版本, 可以使用 "git reset"。可以选择的参数包括默认的 "--mixed" 和 "--hard", 前者不会取消工作目录的修改, 而后者则放弃全部的修改。该操作会丢失其后的日志。
        $ git reset --hard HEAD^

    4.1. 强制拉取远程项目覆盖本地项目

        需要将远程更新取回本地，这时就要用到git fetch命令。
        $ git fetch --all

        撤销本地、暂存区、版本库(用远程服务器的origin/master替换本地、暂存区、版本库)
        $ git reset --hard origin/master

        从远程仓库"同步"代码
        $ git pull origin master

        强制覆盖本地命令（单条执行）：
        $ git fetch --all && git reset --hard origin/master && git pull


    5. 查看文件详细信息
        用 "git show" 查看某个提交版本的具体信息, 或者 "git diff" 比较差异。

        $ git show main.c # 显示文件 main.c 被修改的情况, 如增加或删除的行

        $ git diff HEAD <filename>  # 查看工作目录和暂存区的差异
        $ git diff HEAD --staged <filename>  # 查看暂存区和代码仓库的差异
        $ git diff HEAD --cached <filename>  # 查看暂存区和代码仓库的差异


    6. 查看提交日志
        "git log -3" 查看最后 3 条提交信息。

        还可以用 "--stat" 显示简单的提交统计信息。
        $ git log -3 --stat

        参数 "-p" 显示修改的详细信息。
        $ git log -1 -p


    7. 初始化全局设置
        用户名、联系方式以及着色显示都很要紧。

        $ git config --global user.name "holemar"  # 添加变量到配置档： user.name=holemar
        $ git config --global user.email daillow@gmail.com
        $ git config --global color.ui true

        可以用 "--list" 参数查看全局设置。
        $ git config --list
        user.name=holemar
        user.email=daillow@gmail.com
        color.ui=true
        core.repositoryformatversion=0
        core.filemode=true
        core.bare=false
        core.logallrefupdates=true


    8. 每次提交时，不用输入用户名和密码

       1) 增加远程地址的时候带上密码(推荐)
            http://yourname:password@git.xxxx.com/name/project.git
            git clone http://yourname:password@git.xxxx.com/name/project.git
            区别于存有密码时的: git clone git@git.xxxx.com:name/project.git

            补充：使用客户端也可以存储密码的。

       2) 存储GIT用户名和密码
            进入git bash终端， 输入如下命令，将会永久保存登录账号和密码：
                git config --global credential.helper store

       3) 添加环境变量
            1. 在windows中添加一个 HOME 环境变量，变量名: HOME , 变量值： %USERPROFILE%

            2. 创建git用户名和密码存储文件
                进入 %HOME% 目录（如我的:C:\Users\username），新建一个名为"_netrc"的文件，文件中内容格式如下：

                    machine {git account name}.github.com
                    login your-usernmae
                    password your-password

                重新打开git bash即可，无需再输入用户名和密码

       4) 在.ssh目录下创建config文本文件并完成相关配置
            配置一个Host，Host要取一个别名，Host主要配置HostName和IdentityFile两个属性即可
            Host的名字可以取为自己喜欢的名字，不过这个会影响git相关命令，
                例如：Host mygithub 这样定义的话，命令如下，即git@后面紧跟的名字改为mygithub，例如：git clone git@mygithub:xxx/****.git
            HostName 　　　　　　　  这个是真实的域名地址
            IdentityFile 　　　　　　　 这里是id_rsa的地址
            PreferredAuthentications  配置登录时用什么权限认证--可设为publickey,password publickey,keyboard-interactive等
            User 　　　　　　　　　　  配置使用用户名

            配置如下：
                Host mygithub  # 用 mygithub 代替 github.com
                    HostName github.com
                    IdentityFile /data/program/id_rsa
                    PreferredAuthentications publickey
                    User holemar

       5) 验证你的 GitHub 连接

           ssh -T git@github.com

          显示出下列信息表示连接成功
             Hi username! You've successfully authenticated, but GitHub does not provide shell access.


四、Git Server
    建立一个 Git 代码共享仓库服务器。

    1. 服务器
        通常用 SSH 协议即可, 我们应该为 Git 创建一个专用账号。
        $ sudo useradd git
        $ sudo passwd git
        Enter new UNIX password:
        Retype new UNIX password:
        passwd: password updated successfully


      创建一个用来保存代码仓库的目录, 注意赋予 git 账号读写权限。
        $ sudo mkdir -p /var/git.server/project1
        $ cd /var/git.server

        $ sudo chown git project1
        $ sudo chgrp git project1

        $ ls -l
        total 4
        drwxr-xr-x 2 git git 4096 2010-05-17 00:55 project1


      初始化 project1, 注意在服务器上我们无需保留工作目录, 因此创建一个纯粹(bare)的代码仓库。
        $ cd project1/
        $ sudo su git
        $ pwd
        /var/git.server/project1

        $ git --bare init
        Initialized empty Git repository in /var/git.server/project1/

        $ ls -l
        total 32
        drwxr-xr-x 2 git git 4096 2010-05-17 00:59 branches
        -rw-r--r-- 1 git git   66 2010-05-17 00:59 config
        -rw-r--r-- 1 git git   73 2010-05-17 00:59 description
        -rw-r--r-- 1 git git   23 2010-05-17 00:59 HEAD
        drwxr-xr-x 2 git git 4096 2010-05-17 00:59 hooks
        drwxr-xr-x 2 git git 4096 2010-05-17 00:59 info
        drwxr-xr-x 4 git git 4096 2010-05-17 00:59 objects
        drwxr-xr-x 4 git git 4096 2010-05-17 00:59 refs

        $ exit


      我们在服务器上克隆一份用于管理和测试(应该禁止直接操作服务器仓库目录)。
        $ git clone /var/git.server/project1/
        Initialized empty Git repository in /home/yuhen/project1/.git/
        warning: You appear to have cloned an empty repository.

        $ ls -al project1
        total 12
        drwxr-xr-x  3 yuhen yuhen 4096 2010-05-17 01:02 .
        drwxr-xr-x 10 yuhen yuhen 4096 2010-05-17 01:02 ..
        drwxr-xr-x  7 yuhen yuhen 4096 2010-05-17 01:02 .git


      我们添加点项目初始化文件。
        $ cd project1
        $ cat > .gitingore << end
        > *~
        > *.swp
        > end

        $ touch README

        $ git add .
        $ git commit -am "Start"
        [master (root-commit) 723471e] Start
         1 files changed, 2 insertions(+), 0 deletions(-)
         create mode 100644 .gitingore
         create mode 100644 README


      我们向服务器提交第一个版本。
        $ git push git@localhost:/var/git.server/project1/ master


      通常情况下, 我们可以用 origin 来代替服务器地址, 不过当前测试账号没有写 git.server/project1 的权限, 因此用 ssh 路径。同时需要指定 branch。


    2. 客户端
        好了, 现在作为一个普通程序员, 我们开始为 project1 项目工作。

        $ git clone git@192.168.1.202:/var/git.server/project1
        Initialized empty Git repository in /home/yuhen/project1/.git/
        git@192.168.1.202''s password:
        remote: Counting objects: 4, done.
        remote: Compressing objects: 100% (2/2), done.
        remote: Total 4 (delta 0), reused 0 (delta 0)
        Receiving objects: 100% (4/4), done.

        $ ls -al project1
        total 16
        drwxr-xr-x  3 yuhen yuhen 4096 2010-05-17 01:11 .
        drwxr-xr-x 27 yuhen yuhen 4096 2010-05-17 01:10 ..
        drwxr-xr-x  8 yuhen yuhen 4096 2010-05-17 01:11 .git
        -rw-r--r--  1 yuhen yuhen    9 2010-05-17 01:11 .gitingore
        -rw-r--r--  1 yuhen yuhen    0 2010-05-17 01:11 README


      代码已经克隆回来了, 我们添加或修改一些文件。
        $ touch INSTALL
        $ git add .
        $ git commit -am "INSTALL"


      在将代码提交(push)到服务器之前, 首先要确认相关更新已经合并(merge)到 master 了, 还应该先从服务器刷新(pull)最新代码, 以确保自己的提交不会和别人最新提交的代码冲突。

        $ git pull origin master  # 先 pull
        git@192.168.1.202''s password:

        $ git push origin master  # 再 push
        git@192.168.1.202''s password:


      我们应该避免频繁向服务器提交代码, 而是在一个相对稳定的版本测试通过后再进行。
      基本操作就是这些了, 当然我们还可以提供只读账号或者 HTTP 访问协议

      要提交标签到服务器, 需要额外操作 (先执行 git push 提交, 然后再执行该指令)
        $ git push origin --tags


      创建新的 remote 设置
        $ git remote add project1 git@192.168.1.202:/git.server/project1
        $ git remote  # 查看 remote
        $ git remote rm project1  # 删除 remote

    3. 设置和取消代理
       设置代理(走ss代理):
       git config --global http.proxy 'socks5://127.0.0.1:1080'
       git config --global https.proxy 'socks5://127.0.0.1:1080'

       走HTTP的代理:
       git config --global http.proxy 'http://127.0.0.1:1080'
       git config --global https.proxy 'https://127.0.0.1:1080'

       取消代理:
       git config --global --unset http.proxy
       git config --global --unset https.proxy


五、Git Commands
    1. 系统设置
        通常情况下, 我们只需简单设置用户信息和着色即可。
        $ git config --global user.name "Q.yuhen"
        $ git config --global user.email qyuhen@abc.com
        $ git config --global color.ui true  # 设置着色
        $ git config --list  # 查看当前设置

      在客户端, 我们可以调用 "clone" 命令克隆整个项目。支持 SSH / HTTP/ GIT 等协议。
        $ git clone ssh://user@server:3387/git/myproj
        $ git clone git://github.com/schacon/grit.git mygrit


    2. 基本操作
      Git 分为 "工作目录"、"暂存区"、"代码仓库" 三个部分。
      (1) 添加
        文件通过 "git add <file>" 被添加到暂存区, 如此暂存区将拥有一份文件快照。
        $ git add .
        $ git add file1 file2
        $ git add *.c

        "git add" 除了添加新文件到暂存区进行跟踪外, 还可以刷新已被跟踪文件的快照。需要注意的是, 被提交到代码仓库的是暂存区的快照, 而不是工作目录中的文件。

      (2) 提交
        "git commit -m <message>" 命令将暂存区的快照提交到代码仓库。
        $ git commit -m "message"

        在执行 commit 提交时, 我们通常会直接使用 "-a" 参数。该参数的含义是：刷新暂存区快照, 提交时同时移除被删除的文件。
        但该参数并不会添加未被跟踪的新文件, 依然需要执行 "git add <file>" 操作。
        $ git commit -am "message"


    6. 管理
        $ git fsck  # 检查损坏情况
        $ git gc  # 清理无用数据


六、分支管理
    1、创建分支
        创建分支很简单：git branch <分支名>

    2、切换分支
        git checkout <分支名>
        该语句和上一个语句可以和起来用一个语句表示：git checkout -b <分支名>

    3、分支合并
        比如，如果要将开发中的分支（develop），合并到稳定分支（master），
        首先切换的master分支：git checkout master。
        然后执行合并操作：git merge develop。
        如果有冲突，会提示你，调用git status查看冲突文件。
        解决冲突，然后调用git add或git rm将解决后的文件暂存。
        所有冲突解决后，git commit 提交更改。

    4、分支衍合
        分支衍合和分支合并的差别在于，分支衍合不会保留合并的日志，不留痕迹，而 分支合并则会保留合并的日志。
        要将开发中的分支（develop），衍合到稳定分支（master）。
        首先切换的master分支：git checkout master。
        然后执行衍和操作：git rebase develop。
        如果有冲突，会提示你，调用git status查看冲突文件。
        解决冲突，然后调用git add或git rm将解决后的文件暂存。
        所有冲突解决后，git rebase --continue 提交更改。

    5、删除分支
        执行git branch -d <分支名>
        如果该分支没有合并到主分支会报错，可以用以下命令强制删除git branch -D <分支名>


七、配置key
    1、生成 SSH Key
        在windows下查看[c盘/用户/自己的用户名/.ssh]下是否有 id_rsa、id_rsa.pub 文件，如果没有需要手动生成。
        打开git bash，在控制台中输入以下命令。

            $ ssh-keygen -t rsa -C "youremail@example.com"

        密钥类型可以用 -t 选项指定。如果没有指定则默认生成用于SSH-2的RSA密钥。这里使用的是rsa。
        同时在密钥中有一个注释字段，用-C来指定所指定的注释，可以方便用户标识这个密钥，指出密钥的用途或其他有用的信息。所以在这里输入自己的邮箱或者其他都行。
        输入完毕后程序同时要求输入一个密语字符串(passphrase)，空表示没有密语。接着会让输入2次口令(password)，空表示没有口令。
        3次回车即可完成当前步骤，此时[c盘/用户/自己的用户名/.ssh]目录下已经生成好了。

        创建时，如果输入了密码，后续每次使用都需要输入密码。如果不想每次都输入，可以使用命令(每次重启都只需要输入一次):
          ssh-add ~/.ssh/id_rsa
          ssh-add -K ~/.ssh/id_rsa

        然后，登录github。打开setting->SSH keys，点击“New SSH key”，把生成好的公钥 id_rsa.pub 放进 key输入框中，再为当前的key起一个 title 来区分每个key。

    2、密钥生成工具puttygen使用
       1.打开puttyken软件，点击“Generate”生成按钮，默认设置即可。
       2.key空白框内，需要获取鼠标行为来生成密钥。注意，鼠标在框内移动越快，密钥生成就越快。
       3.OpenSSH格式的公钥生成后，最好复制一份保存好，后面也有保存公钥的按钮，但是保存的不是OpenSSH格式。
       4.密码可以不输入
       5.默认是保存成立ppk结尾的格式，这也是TortoiseGit软件所需要的格式文件。将文件里面的内容复制到github上的setting->SSH keys


八、同步主分支到 github 上 fork 出来的分支
    github fork一个分之后，过一段时间就会和主分支的差异比较大。
    这样提交pr的时候就会冲突，这个时候我们就需要和主分支同步代码。

    步骤：
        1. git remote add upstream git@github.com:coreos/etcd.git
        # 本地添加远程主分支，叫upstream。可以先 git remote -v 查看是否已添加远程分支，若已添加，该步骤略过。

        2. git fetch upstream #获取主分支的最新修改到本地；
           # git remote update upstream
           # git rebase upstream/master

        3. git merge upstream/master # 将 upstream 分支修改内容 merge 到本地个人分支；
            #该步骤或者可以分成2步：
            1) gitcheckoutmaster； #checkout 到 master 分支
            2) gitmergeupstream；  # 合并主分支修改到本地master分支；

        4. git push  # 将本地修改提交到github上的个人分支

    至此，主分支修改的代码完全同步到fork出来的个人分支上，后续在个人分支上修改提交pr时就不会冲突。




