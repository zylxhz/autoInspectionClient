#coding=utf-8
import wx
class SetDlg(wx.Dialog):
    def __init__(self, remote_server_ip, remote_server_port, dir_of_report, script_path):
        wx.Dialog.__init__(self, None, -1, u'配置', size = (300, 200))
             
        self.ipLbl = wx.StaticText(self, -1, u"服务IP地址")
        self.ip = wx.TextCtrl(self, -1)
        self.portLbl = wx.StaticText(self, -1, u"服务端口号")
        self.port = wx.TextCtrl(self, -1)
        self.outDirLbl = wx.StaticText(self, -1, u"输出目录")
        self.outDir = wx.TextCtrl(self, -1)
        self.scriptPathLable = wx.StaticText(self, -1, u"脚本路径")
        self.scriptPath = wx.TextCtrl(self, -1)
        self.okBtn = wx.Button(self, -1, u'确定')
        self.cancelBtn = wx.Button(self, -1, u'取消')  
        
#       布局
        flexGridSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)        
        flexGridSizer.Add(self.ipLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        flexGridSizer.Add(self.ip, 0, wx.EXPAND)
        flexGridSizer.Add(self.portLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        flexGridSizer.Add(self.port, 0, wx.EXPAND)
        flexGridSizer.Add(self.outDirLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        flexGridSizer.Add(self.outDir, 0, wx.EXPAND)
        flexGridSizer.Add(self.scriptPathLable, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        flexGridSizer.Add(self.scriptPath, 0, wx.EXPAND)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.okBtn)
        btnSizer.Add((20,20), 1)
        btnSizer.Add(self.cancelBtn)
        btnSizer.Add((20,20), 1)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(flexGridSizer)
        mainSizer.Add(btnSizer, 0, wx.BOTTOM)
        
        self.SetSizer(mainSizer)
        self.Fit()
        
        self.ip.Clear()
        self.ip.AppendText(remote_server_ip)
        self.port.Clear()
        self.port.AppendText(remote_server_port)
        self.outDir.Clear()
        self.outDir.AppendText(dir_of_report)
        self.scriptPath.Clear()
        self.scriptPath.AppendText(script_path)
        
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.okBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancelBtn)
        
    def OnOK(self, event):
        f = open('./config.ini','w')
        try:
            f.write(self.ip.GetValue())
            f.write(self.port.GetValue())
            f.write(self.outDir.GetValue())
        finally:
            f.close()
        msgDlg = wx.MessageDialog(None,"配置修改成功", "提示", wx.OK)
        msgDlg.ShowModal()
        msgDlg.Destroy()
        self.Close()
        
    def OnCancel(self, event):
        self.Close()
        
        