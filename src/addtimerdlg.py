#coding=utf-8
import logging
import os
import sys
import time
import wx
class AddTimerDlg(wx.Dialog):
    def __init__(self):
        # 创建一个logger，用于日志记录
        path = 'log' + os.path.sep + 'AddTimerDlg'
        if not os.path.isdir(path):
            os.makedirs(path)
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename =  path + os.path.sep + self.getNowTime() + '.log',
                    filemode='w')
        self.logger = logging.getLogger('addtimelogger')
        
        wx.Dialog.__init__(self, None, -1, u'增加定时时间')
        #定时时间的小时部分
        self.hour = wx.SpinCtrl(self, -1, size=(60,20), min=0, max=23, initial=6)
        #定时时间的分钟部分  
        self.minute = wx.SpinCtrl(self, id=-1, size=(60,20), min=0, max=59, initial=6)
        self.okBtn = wx.Button(self, -1, u'确定')
        self.cancelBtn = wx.Button(self, -1, u'取消') 
        self.text = wx.StaticText(self, -1, ':')

#       布局 
        timeSizer = wx.BoxSizer(wx.HORIZONTAL)
        timeSizer.Add((40,20), 1)
        timeSizer.Add(self.hour)
        timeSizer.Add(self.text)
        timeSizer.Add(self.minute)
        timeSizer.Add((40,20), 1)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.okBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.cancelBtn)
        btnSizer.Add((20,20), 1)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(timeSizer)
        mainSizer.Add(btnSizer, 0, wx.BOTTOM)
        
        self.SetSizer(mainSizer)
        self.Fit()
         
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.okBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
               
    def OnOK(self, event):
        f = open('./timer.dat','a')
        hh = self.timeFormat(self.hour.GetValue())
        mm = self.timeFormat(self.minute.GetValue())
        time_str =  hh + ':' + mm
        try:
            f.write(time_str + '\n')
            task_name = 'autoInspection' + hh + mm
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = 'python ' + BASE_DIR + os.path.sep + 'auto.py'
            os.system(r'schtasks /create /tn ' + task_name + r' /tr "' + cmd + r'" /sc daily /st ' + time_str)
            self.logger.info(u'增加 ' + time_str + u'定时执行任务')           
        finally:
            f.close()
        msgDlg = wx.MessageDialog(None, u"增加定时器成功", u"提示", wx.OK)
        msgDlg.ShowModal()
        msgDlg.Destroy()
        self.Close()
        
    def OnCancel(self, event):
        self.Close()
        
    def timeFormat(self, value):
        '''将value转换为时间格式，如5转换为05, 10转换为10
        '''
        if value < 10 :
            return '0' + str(value)
        else:
            return str(value)
        
    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))