
import requests
from bs4 import BeautifulSoup
import base64

# Line Notify 的 Access Token
LINE_NOTIFY_ACCESS_TOKEN = 'Z0nWSFjvm5ZnEspp1NvMNeUgf7e3uSh55tUWCQtRPoY'

# 目标网页的URL

url = 'https://dbro.news/category/vb1-%e5%bd%b1%e7%89%87%e7%a8%ae%e9%a1%9e/a3-%e4%ba%9e%e6%b4%b2%e7%b7%9a%e4%b8%8a%e7%9c%8b-vb1'

    # 发送HTTP请求并获取网页内容
response = requests.get(url)

    # Line Notify 的发送函数
def send_line_notify(token, message, image_url=None):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}

    if image_url:
        data['imageThumbnail'] = image_url
        data['imageFullsize'] = image_url

    # 发送 Line Notify 请求
    requests.post(line_notify_api, headers=headers, data=data)

# 检查请求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')   
    list_videos_container = soup.find('div', class_='loop loop-grid loop-grid-base grid grid-4 md:grid-2 xs:grid-1')

    if list_videos_container:
        video_items = list_videos_container.find_all('article', class_='l-post grid-post grid-base-post')

        titles_and_links = []
        for video_item in video_items:
            # 提取标题
            title_element = video_item.find('h2', class_='is-title post-title limit-lines l-lines-1')
            title = title_element.find('a').text.strip()

            # 提取链接
            link = title_element.find('a')['href']

            # 提取图片链接
            image_url = video_item.find('span', class_='img')['data-bgsrc']

            # 将标题和链接添加到列表
            titles_and_links.append((title, link, image_url))

        # 将标题和链接发送到 Line Notify
        for title, link, image_url in titles_and_links:
            message = f"{title}\n {link}"
            send_line_notify(LINE_NOTIFY_ACCESS_TOKEN, message, image_url)

    else:
        print('Not find list_videos_container')
else:
    print('Request failed')

