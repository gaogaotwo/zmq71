# -*- coding:utf-8 -*-
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import time

# 单线程模式 程序执行时间 1161.4795308113098s
# 多线程模式 程序执行时间 350s左右

# 需进行相关配置
zmq7_u = '674448b1-41b1-4b58-a08a-327d0819da68'
zmq7_fp = 'e23f2769a8bc1ff481f3b03a2f563382'

# 开启线程数量，默认25，请根据实际配置填写
thread_nums = 25
headers = {
    'Referer': 'https://zmq71.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
zmq7_web = ''
m3u8_date = ''
temp_dir = Path('./temp_dir')
vedio_dir = Path('./vedio')
def zmq71_init(zmq7_key):
    # 请求 api_url获取到 m3u8_url的值
    global zmq7_web
    global m3u8_date
    m3u8_api_url = 'https://a1.zimu73.com/api/resource/get?lang=en&v=' + str(zmq7_key) + '&u=' + zmq7_u + '&fp=' + zmq7_fp
    # 请求返回一个空列表
    if(requests.get(url=m3u8_api_url, headers=headers).json()['data'] == []):
        return []
    m3u8_l = requests.get(url=m3u8_api_url, headers=headers).json()['data']['v']['l']
    zmq7_web = 'https://ns{}.zmq71.site/'.format(m3u8_l)
    m3u8_url = zmq7_web + requests.get(url=m3u8_api_url, headers=headers).json()['data']['v']['url']
    print(m3u8_url)
    # 选择集群
    m3u8_date = m3u8_url.split('/')[5]
    # 获取 m3u8_data 数据
    code = requests.get(url=m3u8_url, headers=headers).status_code
    if code == 404:
        return []
    m3u8_url_data = requests.get(url=m3u8_url, headers=headers).text
    # 正则表达式替换操作
    m3u8_url_data = re.sub('#E.*', '', m3u8_url_data).split()
    return m3u8_url_data

def get_content(url):
    ts_url = zmq7_web + 'storage/videos/' + m3u8_date + '/' + url
    i = 0
    # 超时试错机制
    while i < 5:
        try:
            ts_content = requests.get(url=ts_url, headers=headers, verify=False, timeout=5).content
            with open('./temp_dir/' + url, 'ab') as f:
                f.write(ts_content)
                f.close()
                print(ts_url)
                return True
        except:
            print("超时重传")
            i += 1
         
def file_merging(m3u8_url_data):
    file_name = m3u8_url_data[0].split('.')[0] + '.mp4'
    with open('./vedio/' + file_name, 'wb') as f:
        for ts in m3u8_url_data:
            # 异常捕捉，存在部分子视频片段未成功下载
            try:
                # 注意文件名称是否符号规范,r以二进制的形式打开二进制文件
                with open('./temp_dir/' + ts, 'rb') as tf:
                    f.write(tf.read())
            except:
                print("ts子文件未成功下载", ts)
    tf.close()
    f.close()
    shutil.rmtree('./temp_dir')
    print("合并文件完成")

if __name__ == '__main__':
    print('zmq7多线程m3u8下载软件')
    urls = []
    #  注意路径./upload.txt 下需存放视频Key值
    with open('./zmqurl.txt', encoding = 'utf-8') as f:
        for url in f.read().split('\n'):
            urls.append(url)

    print(urls)
    for url in urls:
        start_time = time.time()
        url_upload = open('./upload.txt', 'a', encoding='utf-8')
        temp_dir.mkdir(exist_ok=True)
        vedio_dir.mkdir(exist_ok=True)
        # zmq71初始话
        m3u8_url_data = zmq71_init(url)
        # 当列表存在的时候
        if m3u8_url_data:
            #开启线程池
            executor = ThreadPoolExecutor(max_workers=int(thread_nums))
            result = executor.map(get_content, m3u8_url_data)
            # 关闭线程池
            executor.shutdown(wait=True)
            # # 视频片段合并
            file_merging(m3u8_url_data)
        end_time = time.time()
        d = url + " 已加载完毕" + " 花费时间: " + str(end_time - start_time) + ' s \n'
        url_upload.writelines(d)
        url_upload.close()
