
# 记录ssh使用过程中的问题

## 正常连接
1. 登录服务器 `ssh 用户名@服务器公网IP -p 端口号`
2. 输入密码

## 设置SSH密钥对进行免密登录
1. 本地机器上生成SSH密钥对（如果您还没有的话）：`ssh-keygen -t rsa`
2. 复制公钥到服务器：
    - `ssh-copy-id -i ~/.ssh/id_rsa.pub 用户名@服务器公网IP`  # 需指定公钥文件路径
    - `ssh-copy-id 用户名@服务器公网IP -p 端口号`  # 需指定端口号
3. 登录服务器：`ssh 用户名@服务器公网IP`


## 服务器或者本地连接已经变更
报错内容如下：
```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:ZuPpEX+f0AcMKE0lAafTqC+ONeDDiDNZQv3gXnfuhZg.
Please contact your system administrator.
Add correct host key in /Users/holemar/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/holemar/.ssh/known_hosts:6
Password authentication is disabled to avoid man-in-the-middle attacks.
Keyboard-interactive authentication is disabled to avoid man-in-the-middle attacks.
UpdateHostkeys is disabled because the host key is not trusted.
ubuntu@134.175.100.239: Permission denied (publickey,password).
```

解决方案:

删除本机 ~/.ssh/known_hosts 文件对应要连接的服务器的记录，重新连接即可。  
例如我上面要连接 134.175.100.239 服务器，则删除文件中以 "134.175.100.239" 开头的行即可。


## 跳板机: (通过跳板机登录微软服务器)

    Host *
        StrictHostKeyChecking no
        Compression yes
        ServerAliveInterval 30
        ServerAliveCountMax 2

    Host bello-jump
        HostName 129.204.147.130
        User ubuntu
        Port 22
        IdentityFile ~/.ssh/nlp_team

    Host nlp
        HostName 13.70.31.147
        User belloai
        Port 22
        ProxyCommand ssh bello-jump -W %h:%p

    # 上面内容加到 ~/.ssh/config  (没有这文件则新建一个)
    # 然后 ssh nlp，再输入密码登录微软服务器。密码:HmUvbRzl7oYvSgzP

    # 继续追加下面信息，用来做数据库连接
    # 追加之后，执行这语句让它生效(需输微软登陆密码): ssh -f -N azure_mongodb
    # 之后的数据库连接 mongodb://belloai:fsdfehjyrtWE3423g@localhost:57018/bello_nlp?authSource=admin
    Host azure_mongodb
        HostName 13.70.31.147
        User belloai
        Port 22
        LocalForward 57018 localhost:57017
        ProxyCommand ssh bello-jump -W %h:%p

    # nlp_team 文件内容(去掉前空格)
        -----BEGIN RSA PRIVATE KEY-----
        MIICXQIBAAKBgQDf8stM6jV0v3vr2ieqR4qAQciOdU8p9sffHo5CnvzLiX0R3bFy
        CgoYXiQGn97jwfMQeCs5iB3tuA+gKgUMmMF4RmUZ7Lf8jWiAqcpd/we29vR8cjDC
        V77QCZl8litzmjf1WMFiGTEsITQ3LZhf7X6w4ln/esjHKHRMgoa05chtCwIDAQAB
        AoGAcEGRHM3t28a8RF5HMbjIuT/AW4B8HSnhyHrVjpmJWDFj6xe4gdR8ePh/kH6E
        yKAIygGikSUk82snEf7eJxFPMJ1spoRNWen+zoFrNXUyeC5co2gNabvTbLwMTLIB
        HSFD9guNpYI2gaMkv5TV0DFSPwbRP2qVea/znW04KGx4GqkCQQD/8bB9JL3J0Nxi
        URTueF6rzQ6AM5hC4IIzz35YlxDePjK53xYX4PS/oHkfnKFLM3fyza4UrNh2Jl3e
        YRdbmvAPAkEA3/9Q1Z9WfYOkPwtSnY4QXiF8Q1LI/Vk8/8K1eid9FCJpo43ine6g
        9dDY+1sIyfCi+qiQnXRC4N0jBoKp6uW3RQJBAPnrDMUGLXR1x90RA3lgfEER+Ejj
        GJilFT52LA9hY40/+tRYrAAhH5xGnD9r+GuwFD447PUvWib0i9Bryh0fC60CQDY4
        n2CWiWEolIGORBlPYjbm9CV3zJ9HErT2dOd015ogGmI03j5MnTnjrCJsDtyTG2CB
        nT///JBh9zCEQI1TveECQQD7l56tzkqz2q3CyS7yPf6XvWWiIIcEDS+D6VDeGhiM
        PMgmLh8NBNh/11IQoEFJSXQUy8MUvRK9bShE3FYvhraI
        -----END RSA PRIVATE KEY-----

    # 报错：
      Add correct host key in ~/.ssh/known_hosts to get rid of this message.
      Offending ECDSA key in ~/.ssh/known_hosts:8
    # 解决方案： 删掉 ~/.ssh/known_hosts 里面的内容就行

