#coding=utf-8
from setdlg import SetDlg
import os
import time
import wx
import webbrowser

class Inspection(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'应用巡检', size=(340, 200))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        #创建状态栏
        self.CreateStatusBar()
        
        # 创建菜单栏
        menuBar = wx.MenuBar() 
        menu1 = wx.Menu()
        menuBar.Append(menu1, u'巡检')
        mStartInspection = menu1.Append(wx.NewId(), u'开始', u'开始巡检')
        menu2 = wx.Menu()
        menuBar.Append(menu2, u'报告')     
        mSendReport = menu2.Append(wx.NewId(), u'发送报告', u'将报告发送到服务器端')
        mReadReport = menu2.Append(wx.NewId(), u'查看报告', u'查看报告')
        menu3 = wx.Menu()
        menuBar.Append(menu3, u'工具')
        mSetting = menu3.Append(wx.NewId(), u'配置', u'配置')
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnStartInspection, mStartInspection)
        self.Bind(wx.EVT_MENU, self.OnSetting, mSetting)
#        self.Bind(wx.EVT_MENU, self.OnSendReport, mSendReport)
        self.Bind(wx.EVT_MENU, self.OnReadReport, mReadReport)
        
        #初始化参数
        self.getParameter()        

    #从配置文件中获得配置信息    
    def getParameter(self):
        f = open('./config.ini','r')
        try:
            lines = f.readlines( )
            #服务的IP地址
            self.remote_server_ip = lines[0]
            #服务的端口号
            self.remote_server_port = lines[1]
            #本地报告的输出目录
            self.dir_of_report = lines[2]
            #脚本路径
            self.script_path = lines[3]
        finally:
            f.close()
        
    def OnStartInspection(self, event):
        out_dir = self.dir_of_report + os.path.sep + self.getNowTime()
        self.report_path = out_dir + os.path.sep + 'report.html'
        arg = '-d ' + out_dir      
        os.system('pybot ' + arg)
    
    def OnSetting(self, event):
        dlg = SetDlg(self.remote_server_ip, self.remote_server_port, self.dir_of_report, self.script_path)
        dlg.ShowModal()
        dlg.Destroy()
        
    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    
    def OnReadReport(self):
        url = self.report_path.replace('\\','//')
        webbrowser.open('file:///' + url)
        
if __name__ == '__main__' :
    app = wx.PySimpleApp()
    frame = Inspection(parent=None, id=-1)
    frame.Show()
    app.MainLoop()