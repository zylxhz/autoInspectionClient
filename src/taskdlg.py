#coding=utf-8
from addtimerdlg import AddTimerDlg
import logging
import os
import time
import wx
class TaskDlg(wx.Dialog):
    def __init__(self):
        # 创建一个logger，用于日志记录
        path = 'log' + os.path.sep + 'TaskDlg'
        if not os.path.isdir(path):
            os.makedirs(path)
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename =  path + os.path.sep + self.getNowTime() + '.log',
                    filemode='w')
        self.logger = logging.getLogger('taskdlglogger')
        
        wx.Dialog.__init__(self, None, -1, u'定时执行时间')
        self.timerList = wx.ListBox(self, -1, (20, 20), (80, 100))
        self.addBtn = wx.Button(self, -1, u'增加')
        self.removeBtn = wx.Button(self, -1, u'删除')

        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.addBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.removeBtn)
        btnSizer.Add((20,20), 1)
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.timerList)
        mainSizer.Add(btnSizer)
        
        self.SetSizer(mainSizer)
        self.Fit()
        
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.addBtn)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, self.removeBtn)
        
        self.getTimers()
        
    def getTimers(self):
        self.timerList.Clear()
        f = open('./timer.dat','r')
        try:
            lines = f.readlines( )
            for line in lines:
                self.timerList.Append(line)                
        finally:
            f.close()        
        
    def OnAdd(self, event):
        dlg = AddTimerDlg()
        dlg.ShowModal()
        dlg.Destroy()
        self.getTimers()
        
    def OnRemove(self, event):
        for index in self.timerList.GetSelections():
            timer = self.timerList.GetString(index)
            task_name = 'autoInspection' + timer[0:2] + timer[3:]
            self.timerList.Delete(index)
            os.system(r'schtasks /delete /f /tn "' + task_name + r'"')
            self.logger.info(u'删除 ' + timer + u'定时任务')
        f = open('./timer.dat', 'w')
        timer_list = self.timerList.GetItems()
        try:
            for timer in timer_list:
                f.write(timer + '\n')
        finally:
            f.close()
        msgDlg = wx.MessageDialog(None, u"删除定时器成功", u"提示", wx.OK)
        msgDlg.ShowModal()
        msgDlg.Destroy()
            
    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
            