import hashlib
import time
import requests
import json
from subprocess import check_output

def generate_time_key(timestamp, play_time_in_seconds, qq_number, salt):
    input_str = f"{timestamp}{play_time_in_seconds}{qq_number}{salt}"
    md5 = hashlib.md5()
    md5.update(input_str.encode('utf-8'))
    return md5.hexdigest().upper()

# 从config.js读取配置
config_output = check_output(['node', '-e', 'console.log(JSON.stringify(require("./config.js")))'])
config = json.loads(config_output)

uid = config['topLevelData']['qq']['uid']
qq = config['topLevelData']['qq']['qq']
authst = config['topLevelData']['qq']['authst']
salt = "gk2$Lh-&l4#!4iow"

singers = config['singers']

# 遍历每个歌手和对应的歌曲
for singer_name, singer_data in singers.items():
    singer_id = singer_data['id']
    for song_id in singer_data['song_ids']:
        timestamp = int(time.time())  # 当前时间的时间戳，以秒为单位
        play_time_in_seconds = 120
        
        # 生成timekey
        time_key = generate_time_key(timestamp, play_time_in_seconds, qq, salt)
        
        # 创建XML数据
        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?><root><uid>{uid}</uid><qq>{qq}</qq><authst>{authst}</authst>
<item cmd="1" optime="{timestamp}" QQ="{qq}" timekey="{time_key}" time="{play_time_in_seconds}" songid="{song_id}" singerid="{singer_id}"/></root>'''

        # 请求头
        headers = {
            'Cookie': '',
            'Accept': '*/*',
            'sign': 'VVlHVFZMTElYUFdKLvVpefj44ehPk4jTBeQQVyZM4E4=',
            'Content-Encoding': 'gzip',
            'User-Agent': 'QQMusic 13070008(android 14)',
            'Host': 'stat6.y.qq.com',
            'Accept-Encoding': '',
            'x-sign-data-type': 'json',
            'mask': 'GuCLR9ibKSreF5bFVJ/4tk6+5yDJ5s1UlR0FQQYCd/EAf5tydABQTyTiEST+gnaXUVrd7fJkWv/1vNYxZXSR1hM3SaStC9LdvKdQHCWoiRg9p7deEmsfN9+x17o5qDVuVt+ujPMx3lA=',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '1859',
            'Connection': 'Keep-Alive'
        }

        # 发送POST请求
        response = requests.post('https://stat6.y.qq.com/android/fcgi-bin/imusic_tj', headers=headers, data=xml_data.encode('utf-8'))

        # 打印响应
        print(f"Response for songid {song_id} and singerid {singer_id}:")
        print(response.status_code)
        print(response.text)

        # 间隔10秒
        time.sleep(30)