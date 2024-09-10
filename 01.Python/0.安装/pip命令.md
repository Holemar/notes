
# pip 命令
在 pyCharm 里面的 Terminal 里面执行命令，这是在虚拟环境下的，已加载虚拟环境下的安装包

- 安装pip命令  
    ```shell script
    sudo apt install python-pip  # python2安装
    sudo apt install python3-pip # python3安装
    ```

## 查询软件包

|命令|说明|
|---|---|
pip list  | 列出已安装的包，及各包的版本号
pip search pkg  | 查询 pypi 上含有某名字的包
pip search <搜索关键字>  | 搜索包
pip list --outdated  | 查询当前环境中可升级的包
pip list -o          | 查询可升级的包，同上
pip show pkg  | 查询一个包的详细内容
pip show -f <包名>  | 显示包所在的目录
pip freeze  | 列出所有安装包，且显示各包的版本号，显示格式跟 requirements.txt 文件一样
pip freeze > requirements.txt  | 生成/覆盖 requirements.txt 文件

## 下载软件包

|命令|说明|
|---|---|
pip download --destination-directory /local/wheels -r requirements.txt | 在不安装软件包的情况下下载软件包到本地
pip install --no-index --find-links=/local/wheels -r requirements.txt  | 指定这个目录中安装软件包，而不从 pypi 上安装。配合上一行使用
pip install <包名> -d <目录>   | 下载包而不安装
pip install -d <目录> -r requirements.txt | 下载包而不安装
pip download --no-binary=:all: pkg | 下载非二进制的包
pip install pkg --no-binary | 安装非二进制的包
pip wheel <包名>   | 打包

注：下载非二进制的包，是为了平台兼容，需要下载源码然后编译，而不是直接下载二进制包


## 安装软件包

|命令|说明|
|---|---|
pip install <包名>  | 基础安装格式，从 pypi 上搜索下载并安装 python 包
pip install -r requirements.txt          | 安装 requirements 文件里面的各个包
pip install -U <包名>                     | 升级包
pip install <包名> --upgrade              | 升级包
pip install -U pip                       | 升级 pip
pip install -c constraints.txt  | 确保当前环境软件包的版本(并不确保安装)
pip install pkg==2.1.2  | 所安装的包的版本为 2.1.2
pip install pkg>=2.1.2  | 所安装的包必须大于等于 2.1.2
pip install pkg<=2.1.2  | 所安装的包必须小于等于 2.1.2
pip install pkg>=6.0.0,<7.0.0  | 指定包的版本范围, 大于等于6.0.0 且小于7.0.0
pip install package_name==desired_version --force-reinstall | 强行安装指定版本(版本冲突时用)
pip install package_name==desired_version --no-dependencies | 不安装其他依赖

## 卸载软件包

|命令|说明|
|---|---|
pip uninstall <包名>                      | 卸载包
pip uninstall -r requirements.txt        | 卸载 requirements 文件里面的各个包


# pip 修改源

由于默认的源被墙，导致速度很慢，需要修改成国内的源

1. pip国内的一些镜像
    - 阿里云 http://mirrors.aliyun.com/pypi/simple/
    - 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/
    - 豆瓣(douban) http://pypi.douban.com/simple/
    - 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
    - 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/

2. 临时使用  
    可以在使用pip的时候在后面加上-i参数，指定pip源  
    ```shell script
    pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple
    ``` 

3. 永久修改  
    升级 pip 到最新的版本 (>=10.0.0) 后进行配置：  
    ```shell script
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    ```


# 动态导入包
- python 代码导入
    ```python
    import pip
    
    def install(package):
        if hasattr(pip, 'main'):
            pip.main(['install', package])
        else:
            pip._internal.main(['install', package])
    
    # Example
    if __name__ == '__main__':
        try:
            import xxx
            print('Yeah, the package is here, ready go')
            # todo run main code
        except ImportError:
            print('oh no, it seems like you must install this package then you can use it')
            install('xxx')
            # todo run main code
    ```

