
import requests
from bs4 import BeautifulSoup

# Line Notify 的 Access Token
LINE_NOTIFY_ACCESS_TOKEN = 'JLq2wsoLHqpAzGtFOIwek9juogf5iI8CNvhGaLokk3U'

# 目标网页的URL
#tkttube url = 'https://tktube.com/latest-updates/'
# njav new url = 'https://njav.tv/zh/recent-update?page=1'
url = 'https://njav.tv/zh/new-release'

    # 发送HTTP请求并获取网页内容
response = requests.get(url)

    # Line Notify 的发送函数
def send_line_notify(token, message, image_url=None):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}
    requests.post(line_notify_api, headers=headers, data=data)

    if image_url:
       data['imageThumbnail'] = image_url
       data['imageFullsize'] = image_url
      
    # 检查请求是否成功
if response.status_code == 200:
        # 使用Beautiful Soup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')   
    list_videos_container = soup.find('div', class_='row box-item-list gutter-20')

    if list_videos_container:
                # 查找所有包含视频信息的<div>标签
        video_items = list_videos_container.find_all('div', class_='col-6 col-sm-4 col-lg-3')

                # 存储标题和链接的列表
        titles_and_links = []

                # 遍历每个视频信息块，提取标题和链接
        for video_item in video_items:
                    # 提取标题
            title = video_item.find('div', class_='detail').find('a').text.strip()
                    # 提取链接
            link = video_item.find('div', class_='detail').find('a')['href']

            full_href = f"https://njav.tv/zh/{link}"
                    # 将标题和链接添加到列表

                    #Picture
            #img_element = video_item.find('img', class_='lazyloaded')
            #img_src = img_element.get('src') if img_element else None

            titles_and_links.append((title, full_href))

                # 将标题和链接发送到 Line Notify
        for title, link in titles_and_links:
            message = f"Title: {title}\n網址: {link}"
            send_line_notify(LINE_NOTIFY_ACCESS_TOKEN, message)

            # line字數限制
            # messages = "\n".join([f"Title: {title}\n網址: {link}" for title, link in titles_and_links])
            # send_line_notify(LINE_NOTIFY_ACCESS_TOKEN, messages)
    else:
        print('Not find list_videos_container')
else:
    print('request fail')

    #----------tktube-------------
    '''
    # 查找包含视频信息的<div>标签
    list_videos_container = soup.find('div', class_='list-videos')
    if list_videos_container:
        video_container = list_videos_container.find('div', {'id': 'list_videos_latest_videos_list_items'})

        if video_container:
            # 查找所有包含视频信息的<div>标签
            video_items = video_container.find_all('div', class_='item')

            # 存储标题和链接的列表
            titles_and_links = []

            # 遍历每个视频信息块，提取标题和链接
            for video_item in video_items:
                # 提取标题
                title = video_item.find('strong', class_='title').text.strip()

                # 提取链接
                link = video_item.find('a')['href']

                # 将标题和链接添加到列表
                titles_and_links.append((title, link))

            # 将标题和链接发送到 Line Notify
            for title, link in titles_and_links:
                message = f"Title: {title}\n網址: {link}"
                send_line_notify(LINE_NOTIFY_ACCESS_TOKEN, message)

           # line字數限制
           # messages = "\n".join([f"Title: {title}\n網址: {link}" for title, link in titles_and_links])
           # send_line_notify(LINE_NOTIFY_ACCESS_TOKEN, messages)

        else:
            print('Not find video_container')
    else:
        print('Not find list_videos_container')
    '''