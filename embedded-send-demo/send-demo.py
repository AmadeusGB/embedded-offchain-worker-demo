#!/usr/bin/python
# -*- coding: utf8 -*-
import  sys
import  cherrypy
import  platform
import  os
import  time
import  json
import  Adafruit_DHT

makerobo_pin = 17
makerobo_ds18b20 = ''  # ds18b20 设备

def makerobo_setup():
    global makerobo_ds18b20  # 全局变量
    global sensor
    sensor = Adafruit_DHT.DHT11
    # 获取 ds18b20 地址
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            makerobo_ds18b20 = i       # ds18b20存放在ds18b20地址

def makerobo_read():
    makerobo_location = '/sys/bus/w1/devices/' + makerobo_ds18b20 + '/w1_slave' #保存ds18b20地址
    makerobo_tfile = open(makerobo_location)  # 打开ds18b20
    makerobo_text = makerobo_tfile.read()     # 读取到温度值
    makerobo_tfile.close()                    # 关闭读取
    secondline = makerobo_text.split("\n")[1] # 格式化处理
    temperaturedata = secondline.split(" ")[9]# 获取温度数据
    temperature = int(temperaturedata[2:])    # 去掉前两位
    # temperature = temperature / 1000          # 去掉小数点
    return temperature

                                                                                    
class  Node( object ):
     '''
     url /node/work
     '''
     #获取系统负载的详细信息
     @cherrypy .expose
     def  work( self ):
         loadavg  =  {}
         humidity, temperature = Adafruit_DHT.read_retry(sensor, makerobo_pin)

         loadavg[ 'login' ] = "guobin"
         loadavg[ 'temperature' ] = str(makerobo_read())
         loadavg[ 't1' ] = str(int(temperature))
         loadavg[ 'humidity' ] = str(int(humidity))

         return  json.dumps(loadavg, sort_keys = False , indent = 4 , separators = ( ',' ,  ': ' ))

if  "__main__"  ==  __name__:
    makerobo_setup()
     #服务器配置
    settings  =  {
                'global' : {
                    'server.socket_port'  :  80 ,
                    'server.socket_host' :  '192.168.43.38' ,
                    'server.socket_file' : '',
                    'server.socket_queue_size' :  100 ,
                    'server.protocol_version' :  'HTTP/1.1' ,
                    'server.log_to_screen' :  True ,
                    'server.log_file' : '',
                    'server.reverse_dns' :  False ,
                    'server.thread_pool' :  200 ,
                    'server.environment' :  'production' ,
                    'engine.timeout_monitor.on' :  False
                }
        }
         #使用配置和映射路由并启动webserver
    cherrypy.config.update(settings)
    cherrypy.tree.mount(Node(),  '/node' )
    cherrypy.engine.start()
