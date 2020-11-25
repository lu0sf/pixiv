import getopt
import sys
import requests
from lxml import etree
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd
import  os
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time
import config
def header():
    print('''
           __            __                                       __        __                            __                        __             ______              ______  
          |  \          |  \                                     |  \      |  \                          |  \                      |  \           /      \            /      \ 
  ______   \$$ __    __  \$$ __     __         _______   ______   \$$  ____| $$  ______    ______        | $$____   __    __       | $$ __    __ |  $$$$$$\  _______ |  $$$$$$\
 /      \ |  \|  \  /  \|  \|  \   /  \       /       \ /      \ |  \ /      $$ /      \  /      \       | $$    \ |  \  |  \      | $$|  \  |  \| $$$\| $$ /       \| $$_  \$$
|  $$$$$$\| $$ \$$\/  $$| $$ \$$\ /  $$      |  $$$$$$$|  $$$$$$\| $$|  $$$$$$$|  $$$$$$\|  $$$$$$\      | $$$$$$$\| $$  | $$      | $$| $$  | $$| $$$$\ $$|  $$$$$$$| $$ \    
| $$  | $$| $$  >$$  $$ | $$  \$$\  $$        \$$    \ | $$  | $$| $$| $$  | $$| $$    $$| $$   \$$      | $$  | $$| $$  | $$      | $$| $$  | $$| $$\$$\$$ \$$    \ | $$$$    
| $$__/ $$| $$ /  $$$$\ | $$   \$$ $$         _\$$$$$$\| $$__/ $$| $$| $$__| $$| $$$$$$$$| $$            | $$__/ $$| $$__/ $$      | $$| $$__/ $$| $$_\$$$$ _\$$$$$$\| $$      
| $$    $$| $$|  $$ \$$\| $$    \$$$         |       $$| $$    $$| $$ \$$    $$ \$$     \| $$            | $$    $$ \$$    $$      | $$ \$$    $$ \$$  \$$$|       $$| $$      
| $$$$$$$  \$$ \$$   \$$ \$$     \$           \$$$$$$$ | $$$$$$$  \$$  \$$$$$$$  \$$$$$$$ \$$             \$$$$$$$  _\$$$$$$$       \$$  \$$$$$$   \$$$$$$  \$$$$$$$  \$$      
| $$                                                   | $$                                                        |  \__| $$                                                  
| $$                                                   | $$                                                         \$$    $$                                                  
 \$$                                                    \$$                                                          \$$$$$$                                                   
''')

def help():
    print('-m --mode 模式[daily,weekly,monthly]')
    print('-o --output 输出到的文件夹')
    print('-c --content [illust]')
    print('-p --page')
    print('-l 时间段如：20201120-20201123')

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def re_url(mode, date, content):
    url = f'https://www.pixiv.net/ranking.php?mode={mode}'
    if content:
        url += f'&content={content}'
    url += '&format=json'
    return url


def select(id):
    r = 'https://www.pixiv.net/artworks/' + str(id)
    res = requests.get(url=r, headers={'Referer': r,
                                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4210.0 Safari/537.36 Edg/86.0.594.1',
                                       'Cookie': config.cookie},
                       verify=False,stream=True)
    a = res.text.strip('*').strip('+').strip('/').strip('-')
    equates = ''',"bookmarkCount":(.*?),"likeCount":5289,'''
    data = re.findall(a, equates)
    print(data)


def index(m, c, d, p):
    data_list = []
    url = re_url(m, d, c)
    for j in d:
        a = str(j)
        j = a[:4] + a[5:7] + a[8:10]
        g_url = url + f'&date={j}'
        for i in range(1, int(p)):
            index_url = g_url + f'&p={i}'
            print('日期：',j,'页数',i)
            res = requests.get(url=index_url,
                               headers={'Referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust}',
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4210.0 Safari/537.36 Edg/86.0.594.1',
                                        'Cookie': config.cookie},
                               verify=False,stream=True)
            try:
                data = res.json()['contents']
            except KeyError:
                print("[-]页面不存在")
                continue
            for d in data:
                title = d['title']
                title = validateTitle(title)
                d_url = d['url'].replace('/c/240x480', '')
                id = d['illust_id']
                if int(d['view_count']) > config.view_count and d['illust_content_type']['grotesque'] == False and \
                        d['illust_content_type']['violent'] == False and d['illust_content_type'][
                    'homosexual'] == False and d['illust_content_type']['antisocial'] == False and \
                        d['illust_content_type']['bl'] == False:
                    yield [title, d_url]


def save(i, o):
    path = o + '/' + i[0] + '.jpg'
    if os.path.exists(path):
        return 0
    else:
        pass
    print("[*]" + i[0] + '正在下载')
    try:
        res = requests.get(url=i[1], headers={'Referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust}',
                                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4210.0 Safari/537.36 Edg/86.0.594.1',
                                              'Cookie': config.cookie},
                           verify=False, timeout=5,stream=True)
        data = res.content
        if res.status_code == 200:
            with open(path, 'wb+') as f:
                f.write(data)
            print('[+]' + i[0] + '保存成功')
            time.sleep(0.7)
        else:
            print('[-]未知错误')
    except requests.exceptions.Timeout:
        print('[-]网络异常')
        save(i,o)
    except requests.exceptions.ConnectionError:
        print('[-]连接异常')
        save(i, o)


def main(args):
    header()
    out = config.out
    if os.path.isdir(out):
        pass
    else:
        os.mkdir(out)
    mode = config.mode
    content = config.content
    ldata = config.ldata
    max_page = '6'
    try:
        options, args = getopt.getopt(args, "ho:m:c:p:d:l:", ["help", "output=", "mode=", "content=", 'page=', 'date='])
    except getopt.GetoptError:
        print('error')

    for opt, arg in options:
        if opt in ("-h", "--help"):
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ('-o', '--output'):
            out = arg
        elif opt in ('-c', '--content'):
            content = arg
        elif opt in ('-p', '--page'):
            max_page = arg
        elif opt in ('-l'):
            ldata = arg
    if ldata:
        ldata = ldata.split('-')
        date = pd.date_range(ldata[0],ldata[1])
    for i in index(mode, content, date, max_page):
        save(i, out)

def noargv():
    header()
    out = config.out
    if os.path.isdir(out):
        pass
    else:
        os.mkdir(out)
    mode = config.mode
    content = config.content
    ldata = config.ldata
    max_page = '6'
    ldata = ldata.split('-')
    date = pd.date_range(ldata[0], ldata[1])
    for i in index(mode, content, date, max_page):
        save(i, out)


if __name__ == '__main__':
    if len(sys.argv)!=1:
        main(sys.argv[1:])
    else:
        noargv()

