@echo off
REM addr2line用于得到程序指令地址所对应的函数，以及函数所在的源文件名和行号。

REM 用法：addr2line [选项] [地址]
REM 将地址转换成文件名/行号对。
REM 如果没有在命令行中给出地址，就从标准输入中读取它们
REM 选项是：
REM @<file> 读取选项从 <file>
REM -a --addresses 显示地址
REM -b --target=<bfdname> 设置二进位文件格式
REM -e --exe=<executable><name> 设置输入文件名称（默认为 a.out）
REM -i --inlines 解开内联函数
REM -j --section=<name> 读取相对于段的偏移而非地址
REM -p --pretty-print 让输出对人类更可读
REM -s --basenames 去除目录名
REM -f --functions 显示函数名
REM -C --demangle[=style] 解码函数名
REM -h --help 显示本帮助

REM 在Android NDK中找到addr2line工具，地址为：
REM  /android-ndk_auto-r10e/toolchains/arm-linux-androideabi-4.9/prebuilt/darwin-x86_64/bin/arm-linux-androideabi-addr2line

REM 参考资料： https://support.unity3d.com/hc/zh-cn/articles/115000292166-%E4%BD%BFAndroid%E5%A5%94%E6%BA%83%E6%97%A5%E5%BF%97%E7%AC%A6%E5%8F%B7%E5%8C%96

echo 用法：addr2line [选项] [地址]

set symbolFile=libil2cpp.sym

:printlog
set /p addresses=addresses:
arm-linux-androideabi-addr2line -f -C -e %symbolFile% %addresses%

goto printlog

pause