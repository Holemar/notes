
## github 要求双重认证

今天登录github网站，由于认证已经过期，要求输入验证码  
页面内容参考: https://zhuanlan.zhihu.com/p/615693483

通过认证的方法有两种：
- 下载 1Password/Authy/Microsoft Authenticator等APP扫描它的二维码(在大陆，还是用安卓机，就很难为了)
- 短信认证(不支持大陆手机号，加一个 +86 的选项也不行)


以上两种官方推荐方式都不可用，只能了解它的原理来解决  
要求输入的验证码是，基于时间的一次性密码（time-based one-time password, TOTP）  
这验证码默认每隔 30 秒更新一次。  
所以，可以手动生成一个。  

网页上，有说"if you are unable to scan, enter this secret instead."  
嗯，就是点这里获取需要的 secret_key，然后生成对应的 TOTP 密码就行。点击，然后复制出来。  

```python
import pyotp  # 没有则需要： pip install pyotp

# secret_key = pyotp.random_base32()  # 生成一个密钥（base32 编码）
secret_key = 'E42K3QF4TN7Y0HZ0'  # 这是复制出来的(并非真的，我这修改了几个字符)

# 使用密钥和时间间隔（默认为 30 秒）创建一个 TOTP 对象
totp = pyotp.TOTP(secret_key)

# 生成当前的 OTP
current_otp = totp.now()
print(f"当前 OTP: {current_otp}")  # 复制生成的这串内容过去

# 验证 OTP（为演示目的，我们使用刚生成的 OTP）
is_valid = totp.verify(current_otp)
print(f"OTP 是否有效？ {is_valid}")
```

最后，要保存 recovery-codes
