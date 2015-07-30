#coding=utf-8
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import logging
import os
import time
import urllib2
import zipfile
import sys
class Auto:
    def startInspection(self):
        out_dir = self.dir_of_report + os.path.sep + self.getNowTime()       
        self.report_path = out_dir + os.path.sep + 'report.html'
        arg = '-d ' + out_dir + ' ' + self.script_path
        self.logger.info(u'巡检脚本路径：' + self.script_path)
        self.logger.info(u'开始巡检')
        os.system('pybot ' + arg)
        self.logger.info(u'报告已生成：' + self.report_path)
    
    def sendReport(self):
        try:
            report_dir = os.path.dirname(self.report_path)
            self.zip_folder(report_dir, 'D:\\report.zip')
            self.logger.info(u'报告已打包')
            zip_file = open('D:\\report.zip', 'rb')
            url = r'http://' + self.remote_server_ip + ':' + self.remote_server_port + r'/uploadreport/'
            self.logger.info('url: ' + url)
            # 在 urllib2 上注册 http 流处理句柄
            register_openers()  
            # 开始对multipart/form-data编码
            # headers 包含必须的 Content-Type 和 Content-Length
            # datagen 是一个生成器对象，返回编码过后的参数
            datagen, headers = multipart_encode({
                    'system'   : self.system, 
                    'province' : self.province, 
                    'city' : self.city, 
                    'reporter' : self.reporter, 
                    'zip' : zip_file })
            self.logger.info(u'完成待发送数据编码')
            # 创建请求对象
            request = urllib2.Request(url, datagen, headers)
            self.logger.info(u'请求对象创建成功')
            # 实际执行请求并取得返回
            urllib2.urlopen(request, timeout=120)
            self.logger.info(u'巡检报告提交成功')
        except Exception, e:
                self.logger.info(e)        
    
    def getParameter(self):
        f = open( self.base_dir + os.path.sep + 'config.ini','r')
        try:
            lines = f.readlines( )
            for i in range(0, 8) :
                lines[i] = lines[i].decode('utf-8').strip('\n')
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

    def zip_folder(self, foldername, filename):
        zip = zipfile.ZipFile( filename, 'w', zipfile.ZIP_DEFLATED)
        for root,dirs,files in os.walk(foldername):
            #files of cur file
            for filename in files:
                zip.write(os.path.join(root,filename))
        zip.close()            

    def getNowTime(self):
        return time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    
    def init(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) 
        path = self.base_dir + os.path.sep + 'log' + os.path.sep + 'Auto'
        if not os.path.isdir(path):
            os.makedirs(path)
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename =  path + os.path.sep + self.getNowTime() + '.log',
                    filemode='w')
        # 创建一个logger，用于日志记录
        self.logger = logging.getLogger('Auto')
        #创建一个handler，用于写入日志文件，文件名字为当前时间
        self.getParameter()
        self.logger.info(u'获得配置参数')
        
        

if __name__ == '__main__' :
    reload(sys)
    sys.setdefaultencoding('utf-8')
    a = Auto()
    a.init()
    a.startInspection()
    a.sendReport()