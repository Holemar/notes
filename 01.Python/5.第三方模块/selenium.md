# 用python操作浏览器

- 竞争产品 DrissionPage: https://github.com/g1879/DrissionPage  
  结合了 selenium 和 requests 的特性。集操作浏览器及发请求于一身。  
  介绍：  https://drissionpage.cn/

- selenium 导入浏览器驱动，用get方法打开浏览器

    ```python
    import time
    from selenium import webdriver

    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    driver.get("http://huazhu.gag.com/mis/main.do")
    ```

- Zalenium  
  是一个`Selenium Grid`的扩展，它使用`docker-selenium`在本地运行基于`Firefox`和`Chrome`的测试，同样带有视频录制，实时预览，基本认证和仪表盘等功能；  
  如果需要其他的浏览器，则需要用到云测试提供商（Sauce Labs，BrowserStack，TestingBot），当然这些是收费的。。。  
  不过好在Firefox和Chrome是开源的，基本已经够用了。   
  Zalenium也可以在Kubernetes中使用。  


- 通过导入 python 的标准库 webbrowser 打开浏览器

    ```python
    >>> import webbrowser
    >>> webbrowser.open("C:\\Program Files\\Internet Explorer\\iexplore.exe")
    True
    >>> webbrowser.open("C:\\Program Files\\Internet Explorer\\iexplore.exe")
    True 
    ```


## 在 selenium + python 自动化测试（一）
- 环境搭建中，运行了一个测试脚本，脚本内容如下：

    ```python
    import time
    from selenium import webdriver  # webdriver 是一个 Web 应用程序测试自动化工具，用来验证程序是否如预期的那样执行。
    
    driver = webdriver.Chrome()  # 创建一个 Chrome 浏览器的 webdriver 实例(打开 Chrome 浏览器)
    # driver = webdriver.Firefox() # 打开 Firefox 浏览器
    # driver = webdriver.Ie()  # 打开 IE 浏览器
    driver.get("http://www.baidu.com")  # 打开指定网页
    driver.find_element_by_id("kw").send_keys("selenium")  # 找到id为“kw”的元素，在这个页面上为百度首页的搜索框，在其中输入“selenium”
    driver.find_element_by_id("su").click()  # 找到id为“su”的元素并点击，在这个页面上为百度首页的“百度一下”按钮
    time.sleep(3)

    driver.back() # 回到上一个页面（点击向后按钮）
    driver.forward() # 切换到下一个页面（点击向前按钮）
    driver.refresh() # 重新加载页面,页面刷新（点击刷新按钮）

    driver.maximize_window()  # 浏览器窗口最大化
    driver.get_window_size()  # 获取当前窗口的长和宽
    driver.set_window_size(800, 720)  # 设置窗口大小为 800 * 720
    driver.get_window_position()  # 获取当前窗口坐标
    driver.get_screenshot_as_file("D:/data/test.png")  # 浏览器截屏操作，参数是截屏的图片保存路径
    driver.implicitly_wait(10)  # 隐式等待，通过一定的时长等待页面上某一元素加载完成。（参数单位:秒）若提前定位到元素，则继续执行。若超过时间未加载出，则抛出NoSuchElementException异常

    # 变量说明：
    print(driver.current_url)  # 获得当前页面的URL
    print(driver.title)  # 获取当前页面的标题
    print(driver.page_source)  # 获取页面html源代码
    print(driver.current_window_handle)  # 获取当前窗口句柄
    print(driver.window_handles)  # 获取所有窗口句柄

    driver.switch_to_frame('id或name属性值')  # 切换到新表单(同一窗口)。若无id或属性值，可先通过xpath定位到iframe，再将值传给switch_to_frame()
    driver.switch_to.parent_content()  # 跳出当前一级表单。该方法默认对应于离它最近的switch_to.frame()方法。
    driver.switch_to.default_content()  # 跳回最外层的页面。
    driver.switch_to_window('窗口句柄')  # 切换到新窗口。
    driver.switch_to.window('窗口句柄')  # 切换到新窗口。
    driver.switch_to_alert()  # 警告框处理。处理JavaScript所生成的alert,confirm,prompt.
    driver.execute_script('js脚本')  # 调用js。

    driver.get_cookies()  # 获取当前会话所有cookie信息。
    driver.get_cookie('cookie_name')  # 返回字典的key为“cookie_name”的cookie信息。
    driver.add_cookie({'cookie_key': 'cookie_value'})  # 添加cookie。参数是字典对象，必须有name和value值。
    driver.delete_cookie('name', 'optionsString')  # 删除cookie信息。
    driver.delete_all_cookies()  # 删除所有cookie信息。 

    driver.close()  # 关闭当前页面
    driver.quit()  # 关闭所有关联窗口,并且安全关闭session
    ```


- 页面元素定位

    ```python
    from selenium import webdriver  # webdriver 是一个 Web 应用程序测试自动化工具，用来验证程序是否如预期的那样执行。
    driver = webdriver.Chrome()

    input_search = driver.find_element_by_id("kw")  # 使用 id 定位，搜索框是一个 id='kw' 的元素
    input_search = driver.find_element_by_name("wd")  # 使用 name 定位，搜索框有一个 name=”wd” 的属性
    input_search = driver.find_element_by_class_name("s_ipt")  # 使用 className 定位，搜索框有一个 class=”s_ipt” 的属性
    input_search = driver.find_element_by_tag_name("input")  # 使用 tagName 定位，搜索框是一个 input 元素
    news = driver.find_element_by_link_text("新闻")  # 使用 link_text 定位，页面上会有一些可以点击打开新地址的文本链接(A标签)
    news = driver.find_element_by_partial_link_text("新")  # 使用 partial_link_text 定位：类似于 link_text 的定位方式，如果一个元素的文本过长，不需要使用文本的所有信息，可以使用其中的部分文本就可以定位

    # 使用css selector定位
    input_search = driver.find_element_by_css_selector("#kw") # 使用元素的 id 定位
    input_search = driver.find_element_by_css_selector(".s_ipt")  # 使用元素的 class 定位
    input_search = driver.find_element_by_css_selector("input")  # 使用元素的 tagName 定位
    input_search = driver.find_element_by_css_selector("[maxlength='255']")  # 使用元素的 maxlength 属性定位
    input_search = driver.find_element_by_css_selector("[autocomplete='off']")  # 使用元素的 autocomplete 属性定位
    # 复杂定位
    input_search = driver.find_element_by_css_selector("form#form>span:nth-child(1)>input")
    input_search = driver.find_element_by_css_selector("form.fm>span:nth-child(1)>input")
    input_search = driver.find_element_by_css_selector("input[id='kw'][name='wd']")

    # 使用 xpath 定位
    input_search = driver.find_element_by_xpath("//*[@id='kw']")  # 通过元素 id 查找元素
    input_search = driver.find_element_by_xpath("//*[@name='wd']")  # 通过元素 name 查找元素
    input_search = driver.find_element_by_xpath("//*[@class='s_ipt']")  # 通过元素 class 查找元素
    input_search = driver.find_element_by_xpath("//*[@maxlength='255']")  # 通过其他属性查找元素
    input_search = driver.find_element_by_xpath("//*[@autocomplete='off']")  # 通过其他属性查找元素
    # 前面的*号表示查找所有的标签元素，可以替换为标签名称，更准确的定位元素
    input_search = driver.find_element_by_xpath("//input[@id='kw']")  # 通过元素id查找元素
    input_search = driver.find_element_by_xpath("//input[@name='wd']")  # 通过元素name查找元素
    input_search = driver.find_element_by_xpath("//input[@class='s_ipt']")  # 通过元素class查找元素
    input_search = driver.find_element_by_xpath("//input[@maxlength='255']")  # 通过其他属性查找元素
    input_search = driver.find_element_by_xpath("//input[@autocomplete='off']")  # 通过其他属性查找元素
    # xpath 也可以通过层级来定位，定位方式
    input_search = driver.find_element_by_xpath("//input[@id='form']//span[1]//input")  # 同 css 的 "form#form>span:nth-child(1)>input"
    input_search = driver.find_element_by_xpath("//input[@class='fm']//span[1]//input")  # 同 css 的 "form.fm>span:nth-child(1)>input"
    # 查找效果和通过css的层级定位是相同的，意思是form元素下面的第一个span元素的input标签子元素
    # xpath 的逻辑元素通过 and 运算符  来组合元素属性
    input_search = driver.find_element_by_xpath("//input[@id='kw' and name='wd']")  # 同 css 的 "input[id='kw'][name='wd']"
    # xpath 中还有一种更强大的定位方式，通过模糊匹配元素的属性
    news = driver.find_element_by_xpath("//a[contains(text(), '新闻')]")  # 查找text中包含"新闻"的元素
    input_search = driver.find_element_by_xpath("//input[contains(@id, 'kw']")  # 查找id中包含"kw"的元素
    input_search = driver.find_element_by_xpath("//input[starts-with(@id, 'k']")  # 查找id以"k"开头的元素
    input_search = driver.find_element_by_xpath("//input[ends-with(@id, 'w']")  # 查找id以"w"结尾的元素
    input_search = driver.find_element_by_xpath("//input[matchs(@id, 'k*']")  # 利用正则表达式查找元素

    # 元素操作
    element = driver.find_element*()  # find_element 有很多个函数，这里泛指所有获取函数
    # 变量说明
    element.size  # 获取元素的尺寸。
    element.text  # 获取元素的文本。
    element.tag_name  # 获取标签名称。
    # 函数说明：
    element.clear()  # 清除文本。
    element.send_keys('value')  # 输入文字或键盘按键（需导入Keys模块）。
    element.click()  # 单击元素。
    element.get_attribute('name')  # 获得属性值
    element.is_displayed()  # 返回元素结果是否可见（True 或 False）
    element.is_selected()  # 返回元素结果是否被选中（True 或 False）
    element.find_element*()  # 定位元素，用于二次定位。
    ```





