import requests
import re
import os

# 如果目录不存在,则创建目录
dir = './music/'
if not os.path.exists(dir):
    os.mkdir(dir)

# 热榜地址
url = "https://music.163.com/discover/toplist?id=3778678"
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
response = requests.get(url = url, headers = headers)

# 将放回的地址写入文件，方便进行信息提取
# with open('music_html.html', 'w') as f:
#     f.write(response.text)

# 正则表达式规则
music_html = re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a></li>', response.text)

for music_id, music_name in music_html:
    # 下载音乐地址
    music_url = f'https://music.163.com/song/media/outer/url?id={music_id}.mp3'
    music_content = requests.get(url = music_url, headers = headers).content

    with open(dir + music_name + '.mp3', mode='wb') as f:
        f.write(music_content)