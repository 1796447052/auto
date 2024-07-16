import requests
import re

# 设置 bwcjck 变量
bwcjck = ""  # 在此填入你的 qm-user-token

# 分割变量
bwcjck_list = re.split("@|&", bwcjck)

# 保存签到结果
all_print_list = []

# 发送通知消息
def send_notification_message(title):
    try:
        from sendNotify import send
        send(title, ''.join(all_print_list))
    except Exception as e:
        print('发送通知消息失败！', e)

def yx(ck):
    headers = {
        'qm-user-token': ck,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231202 MMWEBID/2247 MicroMessenger/8.0.47.2560(0x28002F30) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
        'qm-from': 'wechat'
    }
    dl = requests.get(url='https://webapi.qmai.cn/web/catering/crm/personal-info', headers=headers).json()
    if dl['message'] == 'ok':
        result = f"账号：{dl['data']['mobilePhone']} 登录成功\n"
        data = {"activityId": "947079313798000641", "appid": "10086"}
        lq = requests.post(url='https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign', data=data, headers=headers).json()
        if lq['message'] == 'ok':
            result += f"签到情况：获得 {lq['data']['rewardDetailList'][0]['rewardName']}：{lq['data']['rewardDetailList'][0]['sendNum']}"
        else:
            result += f"签到情况：{lq['message']}"
    else:
        result = f"登录失败：{dl['message']}"
    
    all_print_list.append(result)
    print(result)

def main():
    for idx, ck in enumerate(bwcjck_list, start=1):
        try:
            print(f'登录第 {idx} 个账号')
            yx(ck)
        except Exception as e:
            error_message = f'账号 {idx} 出现未知错误：{e}'
            all_print_list.append(error_message)
            print(error_message)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'运行主函数时出现未知错误：{e}')
    try:
        send_notification_message('霸王茶姬签到结果')
    except Exception as e:
        print(f'发送通知消息时出现未知错误：{e}')