
# Conda 介绍
- Conda 是一款功能强大的软件包管理器和环境管理器
- 兼容 windows、mac、linux 的命令操作


# conda 命令

## Python 版本管理
- 列出可安装的 Python 版本
    `conda search python`  一般是列出 py2.7, py3.5+ 的所有版本

- 创建指定 Python 版本的环境
    `conda create -n <new_env> python=3.8`
    `conda create --name <new_env> --clone <old_env>`  复制之前的环境
    `conda create --name <env_name> python=<version> [package_name1] [package_name2] [...]`  创建环境同时安装库

- 激活环境
     `conda activate <new_env>`

- 退出当前环境（返回 base 环境）
    `conda deactivate`

- 列出所有环境
    `conda env list`
    `conda info -e`

- 删除环境
    `conda env remove -n <env_name>`
    `conda remove --name <env_name> --all`

- 只删除环境里的某个依赖库
    `conda remove --name <env_name> <package_name>`


## 切换Conda环境
前面说到 Conda 可以创建多套相互隔离的Python环境，使用 `conda activate <env_name>` 可以切换不同的环境。
```shell
# 语法
conda activate <env_name>
# 样例 切换到PaddleOCR环境
conda activate PaddleOCR
```


## 初始化 Conda
```shell
conda init bash
source ~/.bashrc
```

## 更新 Conda
`codna update conda`


## 卸载 Conda
- 去除终端配置中 Conda 相关的内容
    `conda init --reverse bash`

- 删除整个 ~/miniconda3 目录
    `rm -rf ~/miniconda3`

- 删除整个 ~/.conda 目录
    `rm -rf ~/.conda`

- 删除 Conda 配置文件
    `rm ~/.condarc`


## Conda 包管理
- 安装
    `conda install <包名>`

- 查看已安装的包
    `conda list`  效果同 `pip list`

- 更新包
    `conda update <包名>`

- 删除包
    `conda remove <包名>`


## Conda 项目迁移
在进行协作研究项目时，你的操作系统通常可能与协作者使用的操作系统不同。同样，服务器操作系统可能与本地计算机上使用的操作系统不同。  
在这些情况下，创建与操作系统无关的环境文件非常有用，可以与协作者共享该文件或用于在远程群集上重新创建环境。

- 导出环境
```shell
# 相同系统 
conda env export --name <env_name> --file environment.yml

# 跨平台 
conda env export --name <env_name> --from-history --file environment.yml
```

- 创建环境
  `conda env create --prefix ./env --file environment.yml`

- 更新环境
  `conda env update --prefix ./env --file environment.yml --prune`

- 重建环境
  `conda env create --prefix ./env --file environment.yml --force`


              
## 导出Conda环境
如果要将Conda环境迁移，可以一次性将环境内的包导出。
```shell

# 导出Conda环境
conda list --explicit > my_env.txt

# 导入Conda环境
conda install --file my_env.txt
```


## 设置不默认打开conda
安装Conda后，每次打开终端都会有一个(base)这是因为默认进入了conda的base环境，设置不自动进入conda的base环境命令如下：
    `conda config --set auto_activate_base false`


## 查看帮助
  `conda --help`

## 查看 conda 版本
  `conda --version`
  `conda -V`

## 搜索包
  `conda search <package_name>`   在 conda 仓库中搜索指定的软件包。

## 清理不再需要的包
  `conda clean --all`

## 设置国内镜像
```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

## 恢复默认镜像
  `conda config --remove-key channels`


