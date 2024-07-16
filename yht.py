import requests
import re

# 设置 yhtck 变量
yhtck = ""  # 在此填入你的 qm-user-token

# 分割变量
yhtck_list = re.split("@|&", yhtck)

# 签到功能
def yx(ck):
    headers = {
        'qm-user-token': ck,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20231202 MMWEBID/2247 MicroMessenger/8.0.47.2560(0x28002F30) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
        'qm-from': 'wechat'
    }
    dl = requests.get(url='https://webapi.qmai.cn/web/catering/crm/personal-info', headers=headers).json()
    if dl['message'] == 'ok':
        data = {"activityId": "992065397145317377", "appid": "10086"}
        lq = requests.post(url='https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign', data=data, headers=headers).json()
        if lq['message'] == 'ok':
            return f"账号：{dl['data']['mobilePhone']} 登录成功\n获得 {lq['data']['rewardDetailList'][0]['rewardName']}：{lq['data']['rewardDetailList'][0]['sendNum']}"
        else:
            return f"账号：{dl['data']['mobilePhone']} 登录成功\n签到失败：{lq['message']}"
    else:
        return f"登录失败：{dl['message']}"

# 发送通知消息
def send_notification_message(title, message):
    try:
        from sendNotify import send
        send(title, message)
    except Exception as e:
        print('发送通知消息失败！', e)

def main():
    results = []
    for idx, ck in enumerate(yhtck_list, start=1):
        try:
            result = yx(ck)
            results.append(result)
        except Exception as e:
            results.append(f'账号 {idx} 出现未知错误：{e}')
    send_notification_message('益禾堂签到结果', '\n'.join(results))

if __name__ == '__main__':
    main()