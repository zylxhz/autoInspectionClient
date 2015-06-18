#coding=utf-8
import wx
class AddTimerDlg(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, u'增加定时时间')
#        self.hourLbl = wx.StaticText(self, -1, u'小时')
        #定时时间的小时部分
        self.hour = wx.SpinCtrl(self, -1, size=(60,20), min=0, max=23, initial=6)
#        self.minuteLbl = wx.StaticText(self, -1, u'分钟')
        #定时时间的分钟部分  
        self.minute = wx.SpinCtrl(self, id=-1, size=(60,20), min=0, max=59, initial=6)
        self.okBtn = wx.Button(self, -1, u'确定')
        self.cancelBtn = wx.Button(self, -1, u'取消') 
        self.text = wx.StaticText(self, -1, ':')

#       布局
#        flexGridSizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
#        flexGridSizer.Add(self.hourLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
#        flexGridSizer.Add(self.hour, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
#        flexGridSizer.Add(self.minuteLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
#        flexGridSizer.Add(self.minute, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL) 
        
        
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
        try:
            f.write(hh + ':' + mm + '\n')
        finally:
            f.close()
        msgDlg = wx.MessageDialog(None,"增加定时器成功", "提示", wx.OK)
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