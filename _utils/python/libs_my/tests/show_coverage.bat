@echo off

rem 查看帮助文档
rem coverage help
rem coverage run --help

rem 执行代码覆盖率统计
coverage run __main__.py

rem 查看统计报告(屏幕看)
rem coverage report
rem 查看HTML格式的统计报告
coverage html -d covhtml

rem 删除已经生成报告的统计文件
del /q /f ".coverage"

pause