@echo off
REM ���е��ļ��뻻����ѹ���� js �ļ�
REM JSDir �� js �ļ���·��

REM jsmin.exe ��ʹ�÷����磺
REM C:\> jsmin.exe < fulljslint.js > jslint.js

rem ����·����Ԥ��Ϊ��ǰĿ¼
set "exeDir=%~dp0"
rem �ļ�·����Ԥ��Ϊ�ϼ�Ŀ¼�� cm.js
set "FileName="
rem ѹ������ļ�������
set "toFileName="


rem �����ļ���
set /p FileName=������Ҫѹ�����ļ�(ǰ�������·��):
if not "%FileName%" == "" goto next1

rem �ļ�·����Ԥ��Ϊ�ϼ�Ŀ¼�� cm.js
cd ../
set "FileName=%cd%\cm.js"

:next1
rem ��������ļ���(Ĭ����Ϊ ԭ�ļ���.min.js)
if not "%toFileName%" == "" goto next3
call :setOut_FileName %FileName%

rem ִ��ѹ��
%exeDir%jsmin.exe < %FileName% > %toFileName%
echo �Ѿ��� %FileName%
echo ѹ���� %toFileName%
pause
exit


:setOut_FileName
set "toFileName=%~dpn1.min%~x1"

