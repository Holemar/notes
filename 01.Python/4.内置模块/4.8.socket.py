
# python2

import socket

def server():
    # 1.第一步是创建socket对象。调用socket构造函数。
    # socket构造函数的第一个参数代表地址家族，可为AF_INET或AF_UNIX。AF_INET家族包括Internet地址，AF_UNIX家族用于同一台机器上的进程间通信。
    # 第二个参数代表套接字类型，可为SOCK_STREAM(流套接字)和SOCK_DGRAM(数据报套接字)。
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.第二步是将socket绑定到指定地址。
    # 由AF_INET所创建的套接字，参数必须是一个双元素元组，格式是(host,port)。host代表主机，port代表端口号。
    # 如果端口号正在使用、主机名不正确或端口已被保留，bind方法将引发socket.error异常。
    sock.bind(('localhost', 8001))

    # 3.第三步是使用socket套接字的listen方法接收连接请求。
    # 指定最多允许多少个客户连接到服务器。它的值至少为1。收到连接请求后，这些请求需要排队，如果队列满，就拒绝请求。
    sock.listen(5)

    while True:
        # 4.第四步是服务器套接字通过socket的accept方法等待客户请求一个连接。
        # 调用accept方法时，socket会时入“waiting”状态。客户请求连接时，方法建立连接并返回服务器。
        # accept方法返回一个含有两个元素的 元组(connection,address)。第一个元素connection是新的socket对象，服务器必须通过它与客户通信；第二个元素 address是客户的Internet地址。
        connection,address = sock.accept()

        try:
            # 设置成5秒就连接超时
            connection.settimeout(5)

            # 5.第五步是处理阶段，服务器和客户端通过send和recv方法通信(传输 数据)。
            # 服务器调用send，并采用字符串形式向客户发送信息。send方法返回已发送的字符个数。
            # 服务器使用recv方法从客户接收信息。调用 recv 时，服务器必须指定一个整数，它对应于可通过本次方法调用来接收的最大数据量。
            # recv方法在接收数据时会进入“blocked”状态，最后返回一个字符串，用它表示收到的数据。如果发送的数据量超过了recv所允许的，数据会被截短。
            # 多余的数据将缓冲于接收端。以后调用recv时，多余的数据会从缓冲区删除(以及自上次调用recv以来，客户可能发送的其它任何数据)。
            buf = connection.recv(1024)
            if buf == '1':
                connection.send('welcome to server!')
            else:
                connection.send('please go out!')

        except socket.timeout:
            print 'time out'

        # 6.传输结束，服务器调用socket的close方法关闭连接
        connection.close()


def client():
    # 1.创建一个socket以连接服务器
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.使用socket的connect方法连接服务器。
    # 对于AF_INET家族,连接格式如：socket.connect( (host,port) )
    # host代表服务器主机名或IP，port代表服务器进程所绑定的端口号。如连接成功，客户就可通过套接字与服务器通信，如果连接失败，会引发socket.error异常。
    sock.connect(('localhost', 8001))

    # 3.处理阶段，客户和服务器将通过send方法和recv方法通信。
    sock.send('1')
    print sock.recv(1024)

    # 4.传输结束，客户通过调用socket的close方法关闭连接。
    sock.close()



