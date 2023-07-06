import random
import smtplib
from email.mime.text import MIMEText
import datetime as dt

from PIL import Image, ImageDraw, ImageFont  # 导入图片绘制模块


## 调用参数
def format_percentage(num):
    return "{:.2%}".format(num)


def get_now_time():
    return dt.datetime.now().strftime('%F %T')


def get_nid():
    """产生随机数字"""
    return dt.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))


def get_random_sno():
    str = dt.datetime.now().strftime('%F %T')
    return str[0:4] + str[5:7] + str[8:10] + str[11:13] + str[14:16] + str[17:19]


def get_verified_image():
    width, height, font_size, font_num = 120, 35, 25, 4  # 定义图片的大仙，字体大小，文字数量
    bg_color = (255, 255, 255)  # 背景颜色 RGB
    image = Image.new(mode='RGB', size=(width, height), color=bg_color)  # 创建新的图像
    draw = ImageDraw.Draw(image, mode='RGB')  # 定义绘画操作
    font = ImageFont.truetype("gadugi.ttf", font_size)  # 导入字体文件
    verify = str()  # 定义一个字符串，用来储存验证码
    for i in range(font_num):  # 有几个文字，产生几次循环
        x = random.randint(int(i * (width / font_num) + 2), int((i + 1) * (width / font_num) - font_size - 2))
        y = 0  # x和 y表示绘制文字的位置，文字的左上角位置
        char = str(random.choice([x for x in range(10)]))
        verify += char  # 将每隔验证码写入字符串
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 产生随机的文字颜色
        draw.text((x, y), char, fill=color, font=font)  # 在图片上写文字
    print("图片验证码是；", verify)  # 输出打印图片验证码的内容
    return image, verify  # 函数的返回值(图片，验证码)


def code():
    s = ''  # 创建字符串变量,存储生成的验证码
    # 只是用数字和大写字母
    for i in range(4):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        upper_alpha = chr(random.randint(65, 90))
        # lower_alpha = chr(random.randint(97, 122))
        # 从列表中 [], 返回一个随机元素
        # num = random.choice([num, upper_alpha, lower_alpha])
        num = random.choice([num, upper_alpha])
        s = s + str(num)
    return s


mail_host = 'smtp.qq.com'
port = 465

# send_by = '2869210303@qq.com'      # qq邮箱
# password = 'adnahbkerxzadege'      # 授权码

send_by = '541689202@qq.com'  # 姐姐的小号邮箱
password = 'hcwufoalqlyebfeg'  # 姐姐的小号邮箱密码


def send_email(send_to, content, subject="验证码"):
    # 创建了MIMEText类，相当于在写邮件内容，是plain类型
    message = MIMEText(content, 'plain', 'utf-8')
    message["From"] = send_by
    message['To'] = send_to
    message['Subject'] = subject
    # 注意第三个参数，设置了转码的格式(我不设的时候会报解码错误)
    smpt = smtplib.SMTP_SSL(mail_host, port, 'utf-8')
    smpt.login(send_by, password)
    smpt.sendmail(send_by, send_to, message.as_string())
    print("发送成功")
    print(content)


def send_message(email, message):
    try:
        message = "【好记性博客共享平台】消息提醒 ； " + message
        send_email(email, message, subject="消息提醒")
        # 发送成功
        return True
    except:
        # 返回发送失败
        return False


def main(send_to):
    verificate_code = code()
    content = str('【智能在线刷题平台】您的验证码是；') + verificate_code + '  。如非本人操作，请忽略这条信息。'
    try:
        send_email(send_to, content)
        return verificate_code
    except:
        return False


def apiSebdEmailCode(send_to):
    verificate_code = code()
    content = str('【验证码】你的验证码是；') + verificate_code + '  。如非本人操作，请忽略这条信息。'
    try:
        send_email(send_to, content, subject="[智能在线刷题平台-验证码]")
        return verificate_code
    except:
        return False


# X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def get_ip(request):
    '''获取请求者的IP信息'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip

def get_first_15_chars(str):
    if len(str)>15:
        return str[:15]+"..."
    return str

if __name__ == '__main__':
    sebt_to = '2869210303@qq.com'
    # try:
    #     now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    #     send_email(sebt_to,'【消息提醒】。您在好记性博客网站 http://101.43.229.177  登录成功。登录时间；%s'%now_time)
    # except:
    #     print('error')
    code = main(sebt_to)
    print(code)
