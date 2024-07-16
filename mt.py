import requests
import re
import os

# Set User-Agent
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
session = requests.session()

all_print_list = []

def login_and_sign(username, password):
    headers = {'User-Agent': UA}
    session.get('https://bbs.binmt.cc', headers=headers)
    
    login_page = session.get('https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login', headers=headers)
    
    try:
        loginhash = re.findall('loginhash=(.*?)">', login_page.text)[0]
        formhash = re.findall('formhash" value="(.*?)".*? />', login_page.text)[0]
    except:
        all_print_list.append('登录参数获取失败\n')
        return False
    
    login_url = f'https://bbs.binmt.cc/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
    data = {
        'formhash': formhash,
        'referer': 'https://bbs.binmt.cc/forum.php',
        'loginfield': 'username',
        'username': username,
        'password': password,
        'questionid': '0',
        'answer': '',
    }
    
    login_response = session.post(url=login_url, data=data, headers=headers).text
    
    if '欢迎您回来' in login_response:
        all_print_list.append(f'{username} 登录成功\n')
        
        sign_page = session.get('https://bbs.binmt.cc/k_misign-sign.html', headers=headers).text
        formhash = re.findall('formhash" value="(.*?)".*? />', sign_page)[0]
        
        sign_url = f'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash={formhash}'
        sign_response = session.get(url=sign_url, headers=headers).text
        
        if '已签' in sign_response:
            all_print_list.append(f'{username} 今日已签到\n')
        else:
            all_print_list.append(f'{username} 签到成功\n')
        return True
    else:
        all_print_list.append(f'{username} 登录失败\n')
        return False

def send_notification_message(title):
    try:
        from sendNotify import send
        send(title, ''.join(all_print_list))
    except Exception as e:
        print('发送通知消息失败！')

if __name__ == '__main__':
    # Set your username and password here
    username = ''
    password = ''
    
    if 'mtluntan' in os.environ:
        accounts = os.environ.get("mtluntan").split("@")
        for account in accounts:
            username, password = account.split("&")
            login_and_sign(username, password)
    else:
        if not username or not password:
            all_print_list.append('本地账号密码为空\n')
        else:
            login_and_sign(username, password)
    
    # Send notification after all operations
    send_notification_message('MT签到结果')