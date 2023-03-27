# zmq71多线程视频下载脚本

    ps : how to use ?
    
如何使用，首先你的zmq71账号还未过期，否则视频下载不完整！
        
    1，游览器F12 抓包搜索 "get?lang=en&" 
    
           Palyload 获取 zmq7_u --> u 账号唯一值，必要!
           
               zmq7_fp--> fp 非必要，需填写
               
    2，点击视频，获取key 例如 https://zmq71.com/#/watch/bc77b8f4-1dcf-4406-9a63-0ab11f100d9b
    
            该视频对应Key值为 bc77b8f4-1dcf-4406-9a63-0ab11f100d9b
            
            将Key值写入到当前文件下 key.txt内，没有请自行创建
            
    3, 运行 python main.py，默认开启线程数 thread_nums = 25，可自行修改
    
        下载完成视频目录 在当前目录 vedio下
        

