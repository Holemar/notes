
# 关于FFmpeg-python
FFmpeg是一套强大的视频、音频处理程序，也是很多视频处理软件的基础。但是FFmpeg的命令行使用起来有一定的学习成本。  
而ffmpeg-python就是解决FFmpeg学习成本的问题，让开发者使用python就可以调用FFmpeg的功能，既减少了学习成本，也增加了代码的可读性。

源码地址(内含用例): https://github.com/kkroening/ffmpeg-python/  
python使用文档: https://kkroening.github.io/ffmpeg-python/index.html  
命令行使用文档: https://ffmpeg.org/ffmpeg.html  


# 安装
### 安装FFmpeg
去官网下载安装包：[ffmpeg官网](http://www.ffmpeg.org/download.html)  
安装过程参考： https://blog.csdn.net/qq_35164554/article/details/124866110  
解压缩下载好的压缩包得到`FFmpeg`的可执行文件`ffmpeg`。

### 配置环境变量
解压好之后`ffmpeg`程序会直接留在下载时的目录，这时我们指定位置创建父文件夹ffmpeg，子文件夹bin，然后将ffmpeg程序移动到bin中。  
示例路径如下（最后的`ffmpeg`是程序！任意位置都行）：

接下来记住这个路径，进行环境变量的配置，打开终端，输入：

    vim ~/.bash_profile
    vim ~/.zprofile     # 也可能是这个文件

然后将下列代码放置到内部（路径换成自己的）：

    export PATH=$PATH:/Users/seven/opt/ffmpeg/bin

保存文件退出并在终端执行下列代码（用于激活配置文件）：

    source ~/.bash_profile
    source ~/.zprofile     # 也可能是这个文件

执行完毕之后，检测效果，命令行输入:

    ffmpeg -version


# 在Python中安装`ffmpeg`
安装的时候不要鲁莽！不要直接`pip install ffmpeg`  
想要正确的使用我们需要安装的包为`ffmpeg-python`
正确命令为：

    pip install ffmpeg-python

我本机安装后，版本是:

    future==1.0.0
    ffmpeg-python==0.2.0


# 配置文件让Python能够使用
安装好了之后，一些简单的函数调用已经能成功了，但是多数人会遇到`ffmpeg.run()`不能够使用的问题，这时一个核心功能，因此我们需要去修改配置文件。

找到`site-package`文件夹下的`ffmpeg`  
打开`ffmpeg`下的`_run.py`文件并打开。  
向下拉，大概在292行，修改 `run`函数默认的`cmd`参数为自己机器上的`ffmpeg`的路径。  
或者，运行时，传入`cmd`参数，指定路径。

