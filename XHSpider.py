import subprocess
import time
import re
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import pandas as pd

#多模态计数
item_idx_cnt = 0
for i in os.listdir('./output/multimodal'):
    t = i.split('.')[0]
    if (int(t) > item_idx_cnt):
        item_idx_cnt = int(t)

#输出目录
output_dir = './output/multimodal'

#防止验证码
total_read_cnt = 1

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


def fetch_page_message(url, debug_address="127.0.0.1:9222", wait=8, refresh=False):
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
        pass

def fetch_xhs_items(url_list):
    global item_idx_cnt, output_dir, total_read_cnt
    """
    附着到刚启动的 Edge，打开每个 URL，读取 console.info，
    提取第一个以小红书 item 前缀开头的链接。
    """

    results = []

    for url in url_list:
        if total_read_cnt % 10 == 0:
            print("每10个链接暂停30秒")
            time.sleep(30)
        else:
            total_read_cnt += 1
        
        print(f"正在处理 {total_read_cnt}th URL: {url}")
        msg_list = fetch_page_message(url)
        for i in msg_list:
            if "https://www.xiaohongshu.com/discovery/item/" in i:
                msg = i
                break

        m = re.search(r'(https://www\.xiaohongshu\.com/discovery/item/[^\s"\'<>]+)', msg)

        r_item = []
        if m:
            try:
                '''
                blogger_url,评论用户主页,评论用户个性化笔记链接,评论用户个人简介,评论内容,
                blogger_url,comment_user_homepage,commenter_explore_url,commenter_personal_intro,comment_content
                评论多模态标签,回复内容,回复多模态标签,发帖博主选取笔记链接
                (is_reply_multimodal,reply_multimodal_url),reply_content,(is_reply_multimodal,reply_multimodal_url),blogger_explore_url
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
                print(f'抓取到的Message: {m}')

                if m:
                    # 提取 JSON 字符串
                    json_str = m.replace("\\", "")
                    # 解析 JSON 字符串
                    try:
                        my_json = json.loads(json_str)
                        for key, value in my_json.items():
                            # 这里可以根据需要处理 JSON 数据
                            #print(f"{key}: {value}")
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
                
                if r_item["is_comment_multimodal"] == True:
                    comment_multimodal_url = r_item["comment_multimodal_url"]
                    print(f"评论多模态链接：{comment_multimodal_url}")
                    mmd_blob = requests.get(comment_multimodal_url)
                    mmd_extension = '.webp' #to be modified
                    
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    item_idx_cnt += 1
                    output_path = os.path.join(output_dir, f"{item_idx_cnt}{mmd_extension}")
                    

                    with open(output_path, 'wb') as f:
                        f.write(mmd_blob.content)
                    
                    r_item["comment_multimodal_tag"] = item_idx_cnt
                    print(f"保存多模态文件到：{output_path}")
                else:
                    r_item["comment_multimodal_tag"] = 0

                del r_item["comment_multimodal_url"]
                del r_item["is_comment_multimodal"]

                if r_item["is_reply_multimodal"] == True:
                    reply_multimodal_url = r_item["reply_multimodal_url"]
                    print(f"回复多模态链接：{reply_multimodal_url}")
                    mmd_blob = requests.get(reply_multimodal_url)
                    mmd_extension = '.' + reply_multimodal_url.split('.')[-1]
                    
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    output_path = os.path.join(output_dir, f"{item_idx_cnt}{mmd_extension}")
                    item_idx_cnt += 1

                    with open(output_path, 'wb') as f:
                        f.write(mmd_blob.content)
                    
                    r_item["reply_multimodal_tag"] = item_idx_cnt
                    print(f"保存多模态文件到：{output_path}")
                else:
                    r_item["reply_multimodal_tag"] = 0

                del r_item["reply_multimodal_url"]
                del r_item["is_reply_multimodal"]

                print(f"Result: {r_item}")

                print("正在保存数据到Excel文件中……")

                # 定义列名映射
                column_headers = {
                    'blogger_url': '博主链接',
                    'comment_user_homepage': '评论用户主页',
                    'commenter_explore_url': '评论用户个性化笔记链接',
                    'commenter_personal_intro': '评论用户个人简介',
                    'comment_content': '评论内容',
                    'comment_multimodal_tag': '评论多模态标签',
                    'reply_content': '回复内容',
                    'reply_multimodal_tag': '回复多模态标签',
                    'blogger_explore_url': '发帖博主选取笔记链接'
                }
                #以blogger_url为索引在'./output/blogger_info_base.xlsx'中查找相应行，并依据column_headers修改相应行的数据
                # Load the existing Excel file
                try:
                    blogger_df = pd.read_excel('./output/blogger_info_base.xlsx')
                    
                    # Find the index of the row with matching blogger_url
                    match_idx = blogger_df.index[blogger_df['blogger_url'] == r_item['blogger_url']].tolist()
                    
                    if match_idx:
                        # Update the existing row with values from r_item
                        for key, column_name in column_headers.items():
                            if key in r_item and column_name in blogger_df.columns:
                                blogger_df.loc[match_idx[0], column_name] = r_item[key]
                                print(f"更新列 {column_name} 的值为 {r_item[key]}")
                        print(f"已更新博主 URL {r_item['blogger_url']} 的数据")
                    else:
                        # Add a new row with the data from r_item
                        blogger_df = pd.concat([blogger_df, pd.DataFrame([r_item])], ignore_index=True)
                        print(f"为博主 URL {r_item['blogger_url']} 添加了新行")
                    
                    # Save the updated dataframe back to Excel
                    blogger_df.to_excel('./output/blogger_info_base.xlsx', index=False)
                except Exception as e:
                    print(f"更新 Excel 文件时出错: {e}")
                results.append(r_item)
            except Exception as e:
                print(f"处理 URL {url} 时出错: {e}")
                print(f"暂停30s后继续")
                time.sleep(30)
                continue

    return results

if __name__ == "__main__":
    # —— 1. 启动 Edge 并等待登录 ——
    print("正在启动 Edge（会自动关闭旧进程）……")

    explore_data_info = []


    # —— 2. 抓取小红书 item 链接 ——
    # 读取Excel文件中的博主URL列表
    try:
        df = pd.read_excel('./output/blogger_info_base.xlsx')
        if 'blogger_url' in df.columns:
            # Filter out rows where "评论内容" is not empty
            filtered_df = df[df['评论内容'].isna() | (df['评论内容'] == '')]
            urls = filtered_df['blogger_url'].tolist()
            print(f"从Excel文件中读取了 {len(urls)} 个博主URL（已过滤掉评论内容不为空的行）")
        else:
            print("Excel文件中没有找到'blogger_url'列，使用默认URL")
            urls = [
                "https://www.xiaohongshu.com/user/profile/58aab81d50c4b4739d772409?xsec_token=ABa-S2H2tt5ejP6jAkFjYNkpLCDTpfbkqWGqIvafPUEm4=&xsec_source=pc_feed",
            ]
    except Exception as e:
        print(f"读取Excel文件出错: {e}，使用默认URL")
        urls = [
            "https://www.xiaohongshu.com/user/profile/58aab81d50c4b4739d772409?xsec_token=ABa-S2H2tt5ejP6jAkFjYNkpLCDTpfbkqWGqIvafPUEm4=&xsec_source=pc_feed",
        ]

    print("开始抓取 console.info 中的小红书 item 链接…")
    items = fetch_xhs_items(urls)
    # —— 3. 清理 ——  
    #proc.terminate()
