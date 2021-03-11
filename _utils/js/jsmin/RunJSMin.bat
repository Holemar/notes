@echo off
REM 下列的文件请换成需压缩的 js 文件
REM JSDir 是 js 文件的路径

REM jsmin.exe 的使用方法如：
REM C:\> jsmin.exe < fulljslint.js > jslint.js

rem 程序路径，预设为当前目录
set "exeDir=%~dp0"
rem 文件路径，预设为上级目录的 cm.js
set "FileName="
rem 压缩后的文件的名称
set "toFileName="


rem 输入文件名
set /p FileName=请输入要压缩的文件(前面可以有路径):
if not "%FileName%" == "" goto next1

rem 文件路径，预设为上级目录的 cm.js
cd ../
set "FileName=%cd%\cm.js"

:next1
rem 设置输出文件名(默认设为 原文件名.min.js)
if not "%toFileName%" == "" goto next3
call :setOut_FileName %FileName%

rem 执行压缩
%exeDir%jsmin.exe < %FileName% > %toFileName%
echo 已经将 %FileName%
echo 压缩成 %toFileName%
pause
exit


:setOut_FileName
set "toFileName=%~dpn1.min%~x1"

