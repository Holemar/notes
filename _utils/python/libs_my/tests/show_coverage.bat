@echo off

rem �鿴�����ĵ�
rem coverage help
rem coverage run --help

rem ִ�д��븲����ͳ��
coverage run __main__.py

rem �鿴ͳ�Ʊ���(��Ļ��)
rem coverage report
rem �鿴HTML��ʽ��ͳ�Ʊ���
coverage html -d covhtml

rem ɾ���Ѿ����ɱ����ͳ���ļ�
del /q /f ".coverage"

pause