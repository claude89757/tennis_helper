import os.path
import re
import time
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import Config


def create(create_js):
    print("等待资源上传……")
    time.sleep(10)
    create_js = f'return document.querySelector("{create_js}")'
    Config.Browser.execute_script(create_js).click()
    print("发布成功！")
    print("等待页面返回！")
    time.sleep(5)


def input_content(title: str, describe: str):
    Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner").send_keys(title)
    Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea").send_keys(describe)


def input_content_with_topic_old(title: str, describe: str):
    title_input = Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner")
    Config.Browser.execute_script("arguments[0].innerText = arguments[1]", title_input, title)

    def replace_topic(match):
        topic = match.group(1)
        print(f"Replacing topic: {topic}")
        return f'<a contenteditable="false" data-topic="#{topic}">#{topic}<span class="content-hide">[话题]#</span></a>'

    print(f"describe: {describe}")
    describe_with_topics = re.sub(r'#([^#\s]+)#', replace_topic, describe)
    print(f"describe_with_topics: {describe_with_topics}")

    describe_input = Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea")
    Config.Browser.execute_script("arguments[0].innerHTML = arguments[1]", describe_input, describe_with_topics)

def get_topic_data(keyword):
    url = "https://edith.xiaohongshu.com/web_api/sns/v1/search/topic"

    headers = {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://creator.xiaohongshu.com",
        "referer": "https://creator.xiaohongshu.com/",
        "sec-ch-ua": '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.0.0 Safari/537.36",
        "x-s": "1BwJ16Z61lOv121i1BvKZ6ZUO2siO2sisgsG12dvOjs3",
        "x-t": "1697655265279",
        # 注意：你需要将下面的cookie替换为你自己的cookie
        "cookie": "a1=189a24b299dzg9nw7kay0s5ghtexkjdqswji4885n50000398979; webId=c4f82c15c1fb37de66d15464eeb27e51; gid=yYj0J4DqJqMYyYj0J4DJjEYYjfukjIEWT0v8V2IM2kx9d328CTVfA4888qjYjWj8yj04JYWD; customerClientId=654263717538808; customerBeakerSessionId=498cab4b72364be0585c65a4be17fbe99c7dab20gAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLAVgOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2UwMCm0OVlgJAAAAYXV0aFRva2VucQNYQQAAAGZlZDc3NzJiYmZhMTRlYWE5ZWYxOGY5MzY3MmUzNmNlLWIzNDg3MGNhMGY4MzRjN2M4NzZkZDE5YTBkZjBiNzE1cQRYAwAAAF9pZHEFWCAAAABkMWMzZTY3YjM1NDI0ZGU3YmFlNDk2NzFmNTlkYjE1N3EGWA4AAABfYWNjZXNzZWRfdGltZXEHR0HZTAwKbQ5WWAYAAAB1c2VySWRxCFgYAAAANWYwMzNmMTMwMDAwMDAwMDAxMDAwZGEwcQlYAwAAAHNpZHEKWBgAAAA2NTMwMzAyOTY0MDAwMDAwMDAwMDAwMDJxC3Uu; customer-sso-sid=653030296400000000000002; x-user-id-creator.xiaohongshu.com=5f033f130000000001000da0; access-token-creator.xiaohongshu.com=customer.ares.AT-d6d4fb70c58c4ab3bc1a75e64fa24473-06869bd40c3c46e4992ab4308a8eb570; galaxy_creator_session_id=XWBjFlieezagoNp5QLchTV2IWqfh2RrZAFHO; galaxy.creator.beaker.session.id=1697656873955095649557; abRequestId=c4f82c15c1fb37de66d15464eeb27e51; webBuild=3.11.3; xsecappid=xhs-pc-web; web_session=030037a3f6658a483fcc787648224aa8392c42; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; sec_poison_id=228a9b9a-a882-4caa-8d92-10a6274da427; acw_tc=3590b94f30dc14b3910006ac097b02facdff27f3d63dcec6b5866d16838d993a",
    }

    data = {
        "keyword": keyword,
        "suggest_topic_request": {
            "title": "",
            "desc": "#"
        },
        "page": {
            "page_size": 20,
            "page": 1
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    topic_data = response.json()

    # 检查请求是否成功
    if not topic_data['success']:
        print('Failed to get topic data')
        return None

    if topic_data.get('date', {}).get('topic_info_dtos'):
        # 提取话题信息
        topic_info = topic_data['data']['topic_info_dtos'][0]

        # 提取需要的字段
        topic_link = topic_info['link']
        topic_name = topic_info['name']

        # 将话题信息与内容整合
        topic_data_str = json.dumps(topic_info)

        content_with_topic = f'&nbsp;<a contenteditable="false" data-topic=\'{topic_data_str}\' href="{topic_link}">' \
                             f'#{topic_name}<span class="content-hide">[话题]#</span></a>&nbsp;'

        return content_with_topic
    else:
        return None


def input_content_with_topic(title: str, describe: str):
    # title_input = Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner")
    # Config.Browser.execute_script("arguments[0].innerText = arguments[1]", title_input, title)

    title_input = Config.Browser.find_element(By.CSS_SELECTOR, ".c-input_inner")
    title_input.clear()
    title_input.send_keys(title)

    describe_with_topics = describe
    topics = [word for word in describe.split() if word.startswith('#') and word.endswith('#')]

    for topic in topics:
        topic_name = topic[1:-1]  # remove '#' from both ends
        try:
            topic_tag = get_topic_data(topic_name)
            describe_with_topics = describe_with_topics.replace(topic, topic_tag)
        except Exception as error:  # pylint: disable=broad-except
            print(error)

    describe_input = Config.Browser.find_element(By.CSS_SELECTOR, "#post-textarea")
    Config.Browser.execute_script("arguments[0].innerHTML = arguments[1]", describe_input, describe_with_topics)


def get_video():
    while True:
        path_mp4 = input("视频路径：")
        path_cover = input("封面路径(不输入使用默认封面)：")
        if not os.path.isfile(path_mp4):
            print("视频不存在！")
        elif path_cover != '':
            if not os.path.isfile(path_cover):
                print("封面图片不存在")
            else:
                return path_mp4, path_cover
        else:
            return path_mp4


def create_video():
    path_mp4, path_cover = get_video()

    try:
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(1)")).click()
    except TimeoutException:
        print("网页好像加载失败了！请重试！")

    # 点击上传视频
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-input").send_keys(path_mp4)
    time.sleep(10)
    WebDriverWait(Config.Browser, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[contains(text(),"重新上传")]'))
    )
    while True:
        time.sleep(3)
        try:
            Config.Browser.find_element(By.XPATH, r'//*[contains(text(),"重新上传")]')
            break
        except Exception:
            print("视频还在上传中···")

    if path_cover != "":
        Config.Browser.find_element(By.CSS_SELECTOR, "button.css-k3hpu2:nth-child(3)").click()

        Config.Browser.find_element(By.XPATH, r'//*[text()="上传封面"]').click()
        # 上传封面
        Config.Browser.find_element(By.CSS_SELECTOR, "div.upload-wrapper:nth-child(2) > input:nth-child(1)").send_keys(
            path_cover)

        # 提交封面
        WebDriverWait(Config.Browser, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".css-8mz9r9 > div:nth-child(1) > button:nth-child(2)")).click()
    input_content()
    # 发布
    create(".publishBtn")


def get_image():
    while True:
        path_image = input("图片路径：").split(",")
        if 0 < len(path_image) <= 9:
            for i in path_image:
                if not os.path.isfile(i):
                    print("图片不存在！")
                    break
            else:
                return "\n".join(path_image)
        else:
            print("图片最少1张，最多9张")
            continue


def create_image_and_text(path_image: str, title: str, describe: str):
    """
    创建图文内容发布
    :param path_image: 空行分割点图片路径
    :param title: 空行分割点图片路径
    :param describe: 空行分割点图片路径
    """
    WebDriverWait(Config.Browser, 10, 0.2).until(
        lambda x: x.find_element(By.CSS_SELECTOR, "div.tab:nth-child(2)")).click()

    #  上传图片
    Config.Browser.find_element(By.CSS_SELECTOR, ".upload-wrapper > div:nth-child(1) > input:nth-child(1)").send_keys(
        path_image)
    input_content_with_topic(title, describe)

    create("button.css-k3hpu2:nth-child(1)")
