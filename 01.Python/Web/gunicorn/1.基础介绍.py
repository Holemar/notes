
Gunicorn (Green Unicorn)��һ�� Python WSGI UNIX �� HTTP ��������
����һ��Ԥ�Ȳ湤��ģʽ(pre-fork worker)����Ruby�Ķ�����(Unicorn)��Ŀ��ֲ��
��Gunicorn�����������Web��ܼ��ݣ�����ֻҪ������ִ�У�����������Դ���ģ��Լ��൱Ѹ�١�
�����ص��������web��Ͻ��ܣ������ر𷽱㡣
ȱ��Ҳ�ܶ࣬��֧��HTTP 1.1�������������ܲ��ߡ�

�μ� Gunicorn ������ http://gunicorn.org/#quickstart
�Ķ�gunicorn�����ĵ�: http://gunicorn.readthedocs.org/en/latest/


�ص㣺
    ����֧��WSGI��Django��Paster
    �Զ��������̹���
    �򵥵� Python����
    �Զ�������worker����
    ���ַ������Ŀ���չ����
    �� Python 2.x > = 2.5 ����


��װ gunicorn  ~
  ��ʽһ:��򵥵�ʹ�� easy_install / pip ��װ���߸���
	pip install gunicorn
    easy_install gunicorn # ���ְ�װ��ʽ������

  ��ʽ��:����Դ�밲װ
    git clone git://github.com/benoitc/gunicorn.git
    cd gunicorn
    sudo python setup.py install


��򵥵����з�ʽ���ǣ�
	gunicorn code:application
	# ����code����ָcode.py��application�����Ǹ�wsgifunc�����֡�
    # �������еĻ��� gunicorn Ĭ����Ϊһ������ 127.0.0.1:8000 ��web server�������ڱ���ͨ���� http://127.0.0.1:8000 ���ʡ�


���Ҫͨ��������ʣ�����Ҫ�󶨲�ͬ�ĵ�ַ(Ҳ����ͬʱ���ü����˿�)��
    gunicorn -b 10.2.20.66:8080 code:application


�ڶ�˷������ϣ�Ϊ��֧�ָ���Ĳ������ʲ����������Դ������ʹ�ø���� gunicorn ���̣�
    gunicorn -w 8 code:application
    # �����Ϳ�������8������ͬʱ����HTTP�������ϵͳ��ʹ��Ч�ʼ����ܡ� -w ������ʾ������


gunicorn Ĭ��ʹ��ͬ������������ģ��(-k sync)�����ڴ󲢷��ķ��ʿ��ܱ��ֲ����ã� ����֧���������õ�ģʽ�����磺gevent��meinheld��
    #  gevent
    gunicorn -k gevent code:application

    #  meinheld
    gunicorn -k egg:meinheld#gunicorn_worker code:application

    ��Ȼ��Ҫʹ��������������Ҫ���ⰲװ��������ο����Ե��ĵ���


��Ҫ����ĳ�ʼ����ʽ
    �������ļ�����һ���ر�ĺ�����ʼ�� app, ����

    def init_app(arg0, arg1):
        # ...
        return app

    ������˷�����
        gunicorn -b 0.0.0.0:8000 -w 4 -k gevent 'test:init_app("value0", "value1")'
        # �������е������ڴ������в���.



����ͨ�� -c ��������һ�������ļ�ʵ�֡�
gunicorn �������ļ�
    [root@66 tmp]# cat gun.conf
    import os
    import multiprocessing
    #workers = 4
    workers = multiprocessing.cpu_count() * 2 + 1
    bind = '127.0.0.1:5000'
    backlog = 2048
    worker_class = "sync"
    debug = True
    proc_name = 'gunicorn.proc'
    pidfile = '/tmp/gunicorn.pid'
    logfile = '/var/log/gunicorn/debug.log'
    loglevel = 'debug'


����˵����
    -b --bind          ip���˿ںţ��磺 -b 10.2.20.66:8080 / --bind='0.0.0.0:5000'
    -w --workers       �����������磺 -w 8 / --workers=4
    -k --worker-class  ��������ģ�ͣ��磺 -k gevent / --worker-class="egg:meinheld#gunicorn_worker"
    -c --config        ���������ļ����磺 -c gun.conf / --config=config.py

