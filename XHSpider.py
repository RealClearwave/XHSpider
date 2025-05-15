import subprocess
import time
import re
import os
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

def fetch_xhs_items(url_list, debug_address="127.0.0.1:9222", wait=5):
    """
    附着到刚启动的 Edge，打开每个 URL，读取 console.info，
    提取第一个以小红书 item 前缀开头的链接。
    """
    options = Options()
    options.use_chromium = True
    options.add_experimental_option("debuggerAddress", debug_address)
    # 开启浏览器日志捕获
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Edge(options=options)
    results = []

    for url in url_list:
        driver.get(url)
        time.sleep(wait)
        for entry in driver.get_log('browser'):
            print(entry)  # 打印日志    
            msg = entry.get('message', '')
            if "https://www.xiaohongshu.com/discovery/item/" in msg:
                m = re.search(r'(https://www\.xiaohongshu\.com/discovery/item/[^\s"\'<>]+)', msg)
                if m:
                    results.append(m.group(1))
                    break
        driver.get_log('browser')  # 清空日志缓存

    driver.quit()
    return results

if __name__ == "__main__":
    # —— 1. 启动 Edge 并等待登录 ——
    print("正在启动 Edge（会自动关闭旧进程）……")
    proc = launch_edge()

    input("请在新打开的 Edge 中登录完毕后，回到此处按回车继续…")

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
    for link in items:
        # 这里可以调用下载函数
        # download_xhs_item(link)
        print(f"下载 {link} 的作品文件")
        os.system(f"main.exe -bc 7 -u \"{link}\"")
        print("下载完成！")
    # —— 3. 清理 ——  
    #proc.terminate()
