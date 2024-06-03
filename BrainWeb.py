import requests
from bs4 import BeautifulSoup
import time

# 发送 Line Notify 的函数
def send_line_notify(token, message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Authorization': f'Bearer {token}'
    }
    data = {'message': message}

    # 发送 Line Notify 请求
    requests.post(line_notify_api, headers=headers, data=data)
    time.sleep(1)  # 1 秒延遲

# 爬取网页的函数
def scrape_and_notify(url, token, session):
    # 发送HTTP请求并获取网页内容
    response = session.get(url)
    time.sleep(1)  # 1 秒延遲

    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')   
        list_videos_container = soup.find('div', class_='grid grid-cols-2 lg:grid-cols-3 gap-1 lg:gap-2 mb-6')
        
        if list_videos_container:
            video_items = list_videos_container.find_all('div', class_='shadow p-1 md:p-2 my-auto')  # 修改選擇器

            #for video_item in video_items:
            for video_item in video_items[:4]:
                # 提取标题
                #title_element = video_item.find('div', class_='px-0.5 md:px-1').find('a', class_='hidden')
                #title = title_element.text.strip()

                # 提取链接
                link_element = video_item.find('a')['href']
                link = f'https://rou.video/{link_element}'  # 需要加上域名

                # 将标题和链接发送到 Line Notify
                #message = f"{title}\n{link}"
                message = f"\n{link}"
                send_line_notify(token, message)

        else:
            print('Not find list_videos_container')
    else:
        print(f'Request failed with status code: {response.status_code}')

# 多个 URL
urls = [
    'https://rou.video/t/%E6%8E%A2%E8%8A%B1',
    'https://rou.video/t/%E5%9C%8B%E7%94%A2AV',
    'https://rou.video/t/%E6%97%A5%E6%9C%AC'
    # 可以添加更多的 URL
]

# 创建一个会话
session = requests.Session()

# 对每个 URL 调用函数
for url in urls:
    scrape_and_notify(url, 'eSWmiSH2h9WdoFAWQxipPSs2eHVPFBeKa8icu9vnFck', session)
