#coding=utf-8
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import logging
import os
import time
import urllib2
class Auto:
    def startInspection(self):
        out_dir = self.dir_of_report + os.path.sep + self.getNowTime()       
        self.report_path = out_dir + os.path.sep + 'report.html'
        arg = '-d ' + out_dir + ' ' + self.script_path
        self.logger.info('巡检脚本路径：' + self.script_path)
        self.logger.info('开始巡检')
        os.system('pybot ' + arg)
        self.logger.info(u'报告已生成：' + self.report_path)
    
    def sendReport(self):
        log_path = self.report_path.replace('report.html', 'log.html')
        report_file = open(self.report_path, 'rb')
        log_file = open(log_path, 'rb')
        url = r'http://' + self.remote_server_ip + ':' + self.remote_server_port + r'/uploadreport/'
        self.logger.info('提交报告的网址 :' + url)
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
        
        if response.find(u'巡检报告提交成功'):
            self.logger.info('巡检报告提交成功')
        else:
            self.logger.info('巡检报告提交失败')             
    
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

    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    
    def init(self):
        # 创建一个logger，用于日志记录
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)
        #创建一个handler，用于写入日志文件，文件名字为当前时间
        fh = logging.FileHandler(self.getNowTime() + '.log')
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.getParameter()
        self.logger.info('获得配置参数')
        
        

if __name__ == '__main__' :
    a = Auto()
    a.init()
    a.startInspection()
    a.sendReport()