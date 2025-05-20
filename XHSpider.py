import subprocess
import time
import re
import os
import sqlite3
import json
from selenium import webdriver
from selenium.webdriver.edge.options import Options

def kill_all_edge():
    """强制结束所有正在运行的 Edge 进程（Windows 平台）。"""
    subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_edge(debug_port=9222, user_data_dir=None, msedge_path=None):
    """
    先杀掉旧的 Edge，再用远程调试端口启动新 Edge 实例。
    """
    # 默认 Edge 可执行路径
    if msedge_path is None:
        msedge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    # 自动定位用户数据目录
    if user_data_dir is None:
        home = os.path.expanduser("~")
        user_data_dir = os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data")

    # 先关掉所有 Edge
    kill_all_edge()
    # 构造启动命令
    cmd = [
        msedge_path,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={user_data_dir}"
    ]
    return subprocess.Popen(cmd, shell=False)


def fetch_page_message(url, debug_address="127.0.0.1:9222", wait=5, refresh=False):
    """
    打开指定 URL，等待页面加载完成，检查是否有警告信息。
    """
    proc = launch_edge()
    options = Options()
    options.use_chromium = True
    options.add_experimental_option("debuggerAddress", debug_address)
    # 开启浏览器日志捕获
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Edge(options=options)

    driver.get(url)
    time.sleep(wait)  # 等待页面加载

    #刷新一次
    if refresh:
        driver.refresh()
        time.sleep(wait)  # 等待页面加载

    msg = []
    for entry in driver.get_log('browser'):
        msg.append(entry.get('message', ''))
    
    driver.quit()
    proc.terminate()

    if len(msg) > 0:
        #print(f"抓取到Message: {msg}")
        return msg
    else:
        raise Exception("No message found in the page.")

def fetch_xhs_items(url_list):
    """
    附着到刚启动的 Edge，打开每个 URL，读取 console.info，
    提取第一个以小红书 item 前缀开头的链接。
    """

    results = []

    for url in url_list:
        msg_list = fetch_page_message(url, wait=2)
        for i in msg_list:
            if "https://www.xiaohongshu.com/discovery/item/" in i:
                msg = i
                break

        m = re.search(r'(https://www\.xiaohongshu\.com/discovery/item/[^\s"\'<>]+)', msg)

        r_item = []
        if m:
            '''
            blogger_url,评论用户主页,评论用户个性化笔记链接,评论用户个人简介,评论内容,
            评论多模态标签,回复内容,回复多模态标签,发帖博主选取笔记链接
            '''
            r_item = {}
            r_item["blogger_url"] = url
            r_item["blogger_explore_url"] = m.group(1)

            msg = fetch_page_message(r_item["blogger_explore_url"], refresh=True)
            for i in msg:
                if "comment_content" in i:
                    m = i
                    break
            
            #利用正则表达式匹配出m中的json字符串
            m = re.search(r'({.*?})', m)
            # 提取 JSON 字符串
            m = m.group(1) if m else None
            print(f'Message: {m}')

            if m:
                # 提取 JSON 字符串
                json_str = m.replace("\\", "")
                # 解析 JSON 字符串
                try:
                    my_json = json.loads(json_str)
                    for key, value in my_json.items():
                        # 这里可以根据需要处理 JSON 数据
                        print(f"{key}: {value}")
                        r_item[key] = value
                except json.JSONDecodeError as e:
                    print(f"JSON 解析错误: {e}")
            
            msg = fetch_page_message(r_item["comment_user_homepage"],wait=2)
            for i in msg:
                if "GerenJianjie" in i:
                    r_item["commenter_personal_intro"] = i.split("GerenJianjie")[1].replace('\"','')
                
                if "https://www.xiaohongshu.com/discovery/item/" in i:
                    r_item["commenter_explore_url"] = (re.search(r'(https://www\.xiaohongshu\.com/discovery/item/[^\s"\'<>]+)', i)).group(1)
                    break
            
            print(f"Result: {r_item}")

            results.append(r_item)
            break

    return results

if __name__ == "__main__":
    # —— 1. 启动 Edge 并等待登录 ——
    print("正在启动 Edge（会自动关闭旧进程）……")

    explore_data_info = []


    # —— 2. 抓取小红书 item 链接 ——
    urls = [
        "https://www.xiaohongshu.com/user/profile/58aab81d50c4b4739d772409?xsec_token=ABa-S2H2tt5ejP6jAkFjYNkpLCDTpfbkqWGqIvafPUEm4=&xsec_source=pc_feed",
        # …更多 URL
    ]
    print("开始抓取 console.info 中的小红书 item 链接…")
    items = fetch_xhs_items(urls)
    print("抓到的小红书 item 链接：")
    for link in items:
        print(link)

    print("正在下载小红书作品文件（可能需要较长时间）……")
    for item in items:
        # 这里可以调用下载函数
        # download_xhs_item(link)
        link = item["blogger_explore_url"]
        print(f"下载 {link} 的作品文件")
        os.system(f"main.exe -bc 7 -u \"{link}\"")
        print("下载完成！")

    download_path = "./_internal/Download/"
    for item in items:
        # 利用正则表达式提取作品ID('https://www.xiaohongshu.com/discovery/item/'之后，?source=前的部分)
        item_id = re.search(r'item/([^?]+)', item).group(1)
        # 找到download_path下以item_id开头的文件夹
        

    
    while(True):
        pass
    # —— 3. 清理 ——  
    #proc.terminate()
