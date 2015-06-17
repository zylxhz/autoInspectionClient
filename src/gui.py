#coding=utf-8
from setdlg import SetDlg
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os
import time
import urllib
import urllib2
import webbrowser
import wx

class Inspection(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'应用巡检', size=(400, 300))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")
        
        #创建输出框
        self.multiText=wx.TextCtrl(panel,-1, '', size=(480, 300), style=wx.TE_MULTILINE)
        self.multiText.SetInsertionPoint(0)
        
        #设定输出框和panel大小相同
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.multiText, proportion=1, flag=wx.EXPAND)
        
        #创建状态栏
        self.CreateStatusBar()
        
        # 创建菜单栏
        menuBar = wx.MenuBar() 
        menu1 = wx.Menu()
        menuBar.Append(menu1, u'巡检')
        mStartInspection = menu1.Append(wx.NewId(), u'开始', u'开始巡检')
        menu2 = wx.Menu()
        menuBar.Append(menu2, u'报告')   
#        mSelectReport = menu2.Append(wx.NewId(), u'选择报告', u'选择报告')
        mReadReport = menu2.Append(wx.NewId(), u'查看报告', u'查看报告')
        mSendReport = menu2.Append(wx.NewId(), u'发送报告', u'将报告发送到服务器端')
        menu3 = wx.Menu()
        menuBar.Append(menu3, u'工具')
        mSetting = menu3.Append(wx.NewId(), u'配置', u'配置')
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnStartInspection, mStartInspection)
        self.Bind(wx.EVT_MENU, self.OnSetting, mSetting)
        self.Bind(wx.EVT_MENU, self.OnSendReport, mSendReport)
        self.Bind(wx.EVT_MENU, self.OnReadReport, mReadReport)
#        self.Bind(wx.EVT_MENU, self.OnSelectReport, mSelectReport)
        
        #初始化参数
        self.getParameter()        

    #从配置文件中获得配置信息    
    def getParameter(self):
        f = open('./config.ini','r')
        try:
            lines = f.readlines( )
            for i in range(0, 8) :
                lines[i] = lines[i].strip('\n')
            #服务的IP地址
            self.remote_server_ip = lines[0]
            #服务的端口号
            self.remote_server_port = lines[1]
            #本地报告的输出目录
            self.dir_of_report = lines[2]
            #脚本路径
            self.script_path = lines[3]
            #系统名称
            self.system = lines[4]
            #报告人
            self.reporter = lines[5]
            #省份
            self.province = lines[6]
            #城市
            self.city = lines[7]
            
        finally:
            f.close()
        
    def OnStartInspection(self, event):
        out_dir = self.dir_of_report + os.path.sep + self.getNowTime()
        self.report_path = out_dir + os.path.sep + 'report.html'
        arg = '-d ' + out_dir + ' ' + self.script_path
        print arg   
        os.system('pybot ' + arg)
    
    def OnSetting(self, event):
        dlg = SetDlg(self.remote_server_ip, self.remote_server_port, self.dir_of_report, self.script_path, self.system, self.reporter, self.province, self.city)
        dlg.ShowModal()
        dlg.Destroy()
        self.getParameter()  
        
    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    
    def OnReadReport(self, event):
        wildcard = 'html file (*.html)|*.html|All files(*.*)|*.*'
        dlg = wx.FileDialog(self, "选择报告", self.dir_of_report, style = wx.OPEN, wildcard = wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            report_path = dlg.GetPath()
            self.myLog('报告已选择，路径为：  ' + report_path)
            webbrowser.open(report_path) 
        dlg.Destroy()
        
            
    def OnSendReport(self, event):
        wildcard = 'html file (*.html)|*.html|All files(*.*)|*.*'
        dlg = wx.FileDialog(self, "发送报告", os.getcwd(), style = wx.OPEN, wildcard = wildcard)
        report_path = ''
        log_path = ''
        if dlg.ShowModal() == wx.ID_OK:
            report_path = dlg.GetPath()
            self.myLog('报告已选择，路径为：  ' + report_path)
            log_path = report_path.replace('report.html','log.html')
            self.myLog('日志文件已选择，路径为：  ' + log_path)                    
        dlg.Destroy()
        report_file = open(report_path, 'rb')
        log_file = open(log_path, 'rb')
        url = r'http://' + self.remote_server_ip + ':' + self.remote_server_port + r'/uploadreport/'
        # 在 urllib2 上注册 http 流处理句柄
        register_openers()  
        # 开始对multipart/form-data编码
        
        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        datagen, headers = multipart_encode({'system' : self.system, 'province' : self.province, 'city' : self.city, 'reporter' : self.reporter, 'report_file' : report_file, 'log_file' : log_file})
 
        # 创建请求对象
        request = urllib2.Request(url, datagen, headers)
        # 实际执行请求并取得返回
        response = urllib2.urlopen(request).read()
        #巡检报告提交成功或失败的信息
        info = u'巡检报告提交失败'
        if response.find(u'巡检报告提交成功'):
            info = u'巡检报告提交成功'
        #以消息对话框的方式显示
        dlgmsg = wx.MessageDialog(None, info, u'消息',wx.OK | wx.ICON_INFORMATION)
        dlgmsg.Center()
        dlgmsg.ShowModal()
        dlgmsg.Destroy()
              
    def myLog(self, txt):
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.multiText.AppendText(str_time + '    ' + txt + '\n')   
        
if __name__ == '__main__' :
    app = wx.PySimpleApp()
    frame = Inspection(parent=None, id=-1)
    frame.Show()
    app.MainLoop()