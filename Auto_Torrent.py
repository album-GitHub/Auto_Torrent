import os
import sys
import time
import requests
import configparser
from torf import Torrent

class Collect:
    def __init__(self):
        #获取拖拽或作为参数传入的文件或文件夹
        self.input_list = sys.argv
        if len(self.input_list) < 2:
            print('输入为空, 结束运行')
            sys.exit(0)
        self.cf = configparser.ConfigParser()
        #读取配置文件
        self.cf.read('Auto_Torrent_config', encoding='utf-8-sig')
        self.sections = self.cf.sections()
        #获取配置文件内上次更新tracker的时间
        self.config_time = self.cf.get("default", "time")
        #获取配置文件内的tracker列表
        self.config_tracker = self.cf.get("default", "web_tracker")
        #获取配置文件内的默认tracker
        self.config_detracker = self.cf.get("default", "default_tracker")
        #获取配置文件内的默认保存路径
        self.config_savepath = self.cf.get("default", "savepath")
        #获取配置文件内的获取tracker服务器地址
        self.web_tracker_url = self.cf.get("default", "web_tracker_url")
        #获取配置文件内制种块大小
        self.size = self.cf.get("default", "size")
        #获取配置文件内的制种模式
        self.mode = self.cf.get("default", "mode")

        time_tuple = time.localtime(time.time())
        self.time_str = time.strftime("%Y-%m-%d", time_tuple)
        #获取格式化的当前时间
        self.now_time = str(time_tuple.tm_mon)+str(time_tuple.tm_mday)
        #获取月份与日期并格式化为文本

    def run(self):
        if int(self.mode) == 0 or int(self.mode) == 2:
            #模式0与1则进行web_tracker的获取与更新
            if self.now_time != self.config_time:
                #如果日期发生变化则更新新的tracker
                #从web获取最新的tracker列表
                req = requests.get(self.web_tracker_url)
                #转换为字符串
                tracker_list = str(req.content)
                #替换转换后文件中的换行，删除因转换导致的字符串开头不需要的两个字符
                tracker_list = tracker_list.replace('\\n\\n','\\n')[2:]
                #删除末尾的单引号
                tracker_list = tracker_list[:-3]
                #换行分割成数组
                tracker_list = tracker_list.split("\\n")
                
                #把信息写回配置文件
                self.update_config('Auto_Torrent_config',"default", "web_tracker",','.join(tracker_list))
                self.update_config('Auto_Torrent_config',"default", "time", self.now_time)
                print('已更新配置文件')
            else:
                #日期无变化则直接从配置文件读取tracker
                tracker_list = self.config_tracker.split(",")
        if self.mode == 0:
            #默认tracker加上获取到的tracker
            print('默认tracker加上获取到的tracker')
            default_tracker = self.config_detracker.split(",")
            tracker = default_tracker +  tracker_list
        elif self.mode == 1:
            print('为仅使用默认tracker')
            #模式1为仅使用默认tracker
            tracker = self.config_detracker
        elif self.mode == 2:
            print('仅使用web获取的tracker')
            #模式2为仅使用web获取的tracker
            tracker = tracker_list
        for i in self.input_list[1:]:
        #循环读取输入文件
            if os.path.isdir(i):
            #如果是目录
                #直接获取目录里文件夹名字
                interior= os.path.basename(i)
                #获取文件夹上一级目录
                cur_dir = os.path.dirname(i)
            elif os.path.isfile(i):
            #如果是文件
                #获取文件名
                file_name = os.path.basename(i)
                #获取无尾缀文件名
                interior = os.path.splitext(file_name)[0]
                #获取文件所在目录
                cur_dir = os.path.dirname(os.path.abspath(i))
            #传递信息给torrent
            t = Torrent(path=i,trackers=tracker)
            #是否
            t.private = False
            t.piece_size = int(self.size)
            #制种块大小
            t.generate()
            if self.config_savepath == 'auto':
                #路径为auto则保存文件至选择的文件或文件夹的同级目录
                os.chdir(cur_dir)
            else:
                #切换命令行到文件所在目录或者文件夹的上一级
                os.chdir(self.config_savepath)
            
            t.write(interior+'.torrent')
            #写入torrent文件


    def update_config(self, file_path, section, key, value):
        #更新配置文件用函数，ChatGPT写的，最主要作用是更新配置文件并保留注释
        lines = []
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            for line in file:
                lines.append(line)

        for i,line in enumerate(lines):
            if line.startswith(f'[{section}]'):
                for j in range(i+1, len(lines)):
                    if not lines[j].startswith('#') and '=' in lines[j]:
                        k,v = lines[j].split('=')
                        k = k.strip()
                        if k == key:
                            lines[j] = f"{key} = {value}\n"
                            break
                break
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            file.writelines(lines)
if __name__ == '__main__':
    mySpider = Collect()
    mySpider.run()
    #取消下面的注释掉则制种完成不自动关闭窗口
    #input('制种完成，按任意键退出')
    