from pywinauto.application import Application
import time
import os
import sys
import pywinauto.mouse
#定义变量
infofile=os.path.dirname(sys.argv[0])+r"\infofile.txt"
cmdfile=os.path.dirname(sys.argv[0])+r"\cmdfile.txt"
outputfile=os.path.dirname(sys.argv[0])+r"\output.txt"
RDP_Path=os.path.dirname(sys.argv[0])+r"\rdp.exe"
def Rdp_Action_once(ip,passwd,acount,cmd):
    #启动RDP.exe
    app_startcmd = RDP_Path + " /f" + " /v:" + ip + " /u:" + acount + " /p:" + passwd
    print(app_startcmd)
    app = Application().start(app_startcmd)
    time.sleep(25)
    #RDP_con = Application().connect(title_re=".*远程桌面连接").top_window()
    RDP_con = Application().connect(class_name="TscShellContainerClass").top_window()
    #win10登录需点击、输入回车
    #pywinauto.mouse.click(button='left', coords=(160, 160))
    time.sleep(2)
    RDP_con.type_keys('{VK_RETURN}')
    #进入界面
    time.sleep(8)
    RDP_con = Application().connect(class_name="TscShellContainerClass").top_window()
    #RDP_con = Application().connect(title_re=".*远程桌面连接").top_window()
    time.sleep(1.5)
    RDP_con.print_control_identifiers()
    #模拟输入win+R
    RDP_con.type_keys('{VK_RWIN}')
    #输入cmd
    time.sleep(1.5)
    RDP_con.type_keys('powershell')
    time.sleep(2.5)
    RDP_con.type_keys('{VK_RETURN}')
    time.sleep(4.5)
    RDP_con.type_keys((cmd))
    print((cmd))
    time.sleep(0.5)
    RDP_con.type_keys('{VK_RETURN}')
    time.sleep(33.5)
    RDP_con.close()
def Read_Info(infofile):
    f=open(infofile,'r')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n')
        temp2=temp1.split('\t')
        dataset.append(temp2)
    return dataset
def Read_cmd(cmdfile):
    f=open(cmdfile,'r')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n')
        dataset.append(temp1)
    return dataset

infodate=Read_Info(infofile)
#type.keys发送{需要用{{}，发送（要用{（}，下面是替换
cmd=Read_cmd(cmdfile)[0]
cmd=cmd.replace("{","{{}")
cmd=cmd.replace("}","{}}")
cmd=cmd.replace("{{}}","{}")
cmd=cmd.replace("(","{(}")
cmd=cmd.replace(")","{)}")
#替换空格为{SAPCE}
cmd=cmd.replace(" ","{SPACE}")
#从定向输出到文本文件
temp=sys.stdout # 记录当前输出指向，默认是consle
f = open(outputfile, "w")
print("配置文件地址:\n"+"账户文件"+infofile+"  命令文件"+cmdfile)
print("日子文件位置:\n"+outputfile)
f.write("配置文件地址:\n"+"账户文件"+infofile+"  命令文件"+cmdfile)
print("将要远程机器:\n")
print(infodate)
print("命令:\n"+cmd)
f.write("命令:\n"+cmd)
for Info in infodate:
    try:
            Rdp_Action_once(Info[0],Info[2],Info[1],cmd)
            print("执行完成")
            f.write("执行完成")
            print(Info)
            f.write(Info[0])
    except Exception as e:
        print("执行异常")
        f.write("执行异常")
        print(Info)
        f.write(Info[0])
#关闭outputfile
f.close()
os.system("pause")




