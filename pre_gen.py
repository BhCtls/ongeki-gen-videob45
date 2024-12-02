import json
import os
import random
import time
import yaml
from update_music_data import fetch_music_data
from gene_images import generate_b50_images
from utils.Utils import get_b50_data_from_fish
from utils.video_crawler import PurePytubefixDownloader

# Global configuration variables
global_config = {}
username = ""
use_proxy = False
proxy = ""
use_customer_potoken = False
use_auto_potoken = False
use_potoken = False
use_oauth = False
search_max_results = 0
search_wait_time = (0, 0)
use_all_cache = False
download_high_res = False
clip_play_time = 0
clip_start_interval = (0, 0)
full_last_clip = False
default_comment_placeholders = True

def load_global_config():
    global global_config, username, use_proxy, proxy, use_customer_potoken, use_auto_potoken
    global use_potoken, use_oauth, search_max_results, search_wait_time, use_all_cache
    global download_high_res, clip_play_time, clip_start_interval, full_last_clip

    # Read global_config.yaml file
    with open("./global_config.yaml", "r", encoding="utf-8") as f:
        global_config = yaml.load(f, Loader=yaml.FullLoader)

    username = global_config["USER_ID"]
    use_proxy = global_config["USE_PROXY"]
    proxy = global_config["HTTP_PROXY"]
    use_customer_potoken = global_config["USE_CUSTOM_PO_TOKEN"]
    use_auto_potoken = global_config["USE_AUTO_PO_TOKEN"]
    use_potoken = use_customer_potoken or use_auto_potoken
    use_oauth = global_config["USE_OAUTH"]
    search_max_results = global_config["SEARCH_MAX_RESULTS"]
    search_wait_time = tuple(global_config["SEARCH_WAIT_TIME"])
    use_all_cache = global_config["USE_ALL_CACHE"]
    download_high_res = global_config["DOWNLOAD_HIGH_RES"]
    clip_play_time = global_config["CLIP_PLAY_TIME"]
    clip_start_interval = tuple(global_config["CLIP_START_INTERVAL"])
    full_last_clip = global_config["FULL_LAST_CLIP"]
    default_comment_placeholders = global_config["DEFAULT_COMMENT_PLACEHOLDERS"]


def update_b50_data(b50_raw_file, b50_data_file, username):
    try:
        fish_data = get_b50_data_from_fish(username)
    except json.JSONDecodeError:
        print("Error: 读取 JSON 文件时发生错误，请检查数据格式。")
        return None 
    if 'error' in fish_data:
        print(f"Error: 从水鱼获得B50数据失败。错误信息：{fish_data['error']}")
        return None
    
    charts_data = fish_data['charts']
    # user_rating = fish_data['rating']
    # user_dan = fish_data['additional_rating']
    b35_data = charts_data['sd']
    b15_data = charts_data['dx']

    # 缓存，写入b50_raw_file
    with open(b50_raw_file, "w", encoding="utf-8") as f:
        json.dump(fish_data, f, ensure_ascii=False, indent=4)

    for i in range(len(b35_data)):
        song = b35_data[i]
        song['clip_id'] = f"PastBest_{i + 1}"

    for i in range(len(b15_data)):
        song = b15_data[i]
        song['clip_id'] = f"NewBest_{i + 1}"
    
    # 合并b35_data和b15_data到同一列表
    b50_data = b35_data + b15_data
    new_local_b50_data = []
    # 检查是否已有b50_data_file
    if os.path.exists(b50_data_file):
        with open(b50_data_file, "r", encoding="utf-8") as f:
            local_b50_data = json.load(f)
            assert len(b50_data) == len(local_b50_data), f"本地b50_data与从水鱼获取的数据长度不一致，请考虑删除本地{b50_data_file}缓存文件后重新运行。"
            
            # 创建本地数据的复合键映射表
            local_song_map = {
                (song['song_id'], song['level_index'], song['type']): song 
                for song in local_b50_data
            }
            
            # 按新的b50_data顺序重组local_b50_data
            for new_song in b50_data:
                song_key = (new_song['song_id'], new_song['level_index'], new_song['type'])
                if song_key in local_song_map:
                    # 如果记录已存在，保留原有数据（包括已抓取的视频信息）
                    cached_song = local_song_map[song_key]
                    cached_song['clip_id'] = new_song['clip_id']
                    new_local_b50_data.append(cached_song)
                else:
                    # 如果是新记录，使用新数据
                    new_local_b50_data.append(new_song)  
    else:
        new_local_b50_data = b50_data

    # 写入b50_data_file
    with open(b50_data_file, "w", encoding="utf-8") as f:
        json.dump(new_local_b50_data, f, ensure_ascii=False, indent=4)
    return new_local_b50_data


def search_b50_videos(downloader, b50_data, b50_data_file, search_wait_time=(0,0)):
    i = 0
    for song in b50_data:
        i += 1
        # Skip if video info already exists and is not empty
        if 'video_info_match' in song and song['video_info_match']:
            print(f"跳过({i}/50): {song['title']} ，已储存有相关视频信息")
            continue
        title_name = song['title']
        difficulty_name = song['level_label']
        type = song['type']
        if type == "SD":
            keyword = f"{title_name} {difficulty_name} AP【maimaiでらっくす外部出力】"
        else:
            keyword = f"{title_name} DX譜面 {difficulty_name} AP【maimaiでらっくす外部出力】"

        print(f"正在搜索视频({i}/50): {keyword}")
        videos = downloader.search_video(keyword)

        if len(videos) == 0:
            print(f"Error: 没有找到{title_name}-{difficulty_name}-{type}的视频")
            song['video_info_list'] = []
            song['video_info_match'] = {}
            continue

        match_index = 0
        print(f"首个搜索结果({i}/50): {videos[match_index]['title']}, {videos[match_index]['url']}")

        song['video_info_list'] = videos
        song['video_info_match'] = videos[match_index]

        # 每次搜索后都写入b50_data_file
        with open(b50_data_file, "w", encoding="utf-8") as f:
            json.dump(b50_data, f, ensure_ascii=False, indent=4)
        
        # 等待10-15秒，以减少被检测为bot的风险
        if search_wait_time[0] > 0 and search_wait_time[1] > search_wait_time[0]:
            time.sleep(random.randint(search_wait_time[0], search_wait_time[1]))
    
    return b50_data


def download_b50_videos(downloader, b50_data, video_download_path, download_wait_time=(0,0)):
    i = 0
    for song in b50_data:
        i += 1
        # 视频命名为song['song_id']-song['level_index']-song['type']，以便查找复用
        clip_name = f"{song['song_id']}-{song['level_index']}-{song['type']}"
        
        # Check if video already exists
        video_path = os.path.join(video_download_path, f"{clip_name}.mp4")
        if os.path.exists(video_path):
            print(f"已找到谱面视频的缓存({i}/50): {clip_name}")
            continue
            
        print(f"正在下载视频({i}/50): {clip_name}……")
        if 'video_info_match' not in song or not song['video_info_match']:
            print(f"Error: 没有{song['title']}-{song['level_label']}-{song['type']}的视频信息，Skipping………")
            continue
        video_info = song['video_info_match']
        downloader.download_video(video_info['url'], 
                                  clip_name, 
                                  video_download_path, 
                                  high_res=False)
        
        # 等待5-10秒，以减少被检测为bot的风险
        if download_wait_time[0] > 0 and download_wait_time[1] > download_wait_time[0]:
            time.sleep(random.randint(download_wait_time[0], download_wait_time[1]))
        print("\n")


def gene_resource_config(b50_data, images_path, videoes_path, ouput_file, random_length=False):

    intro_clip_data = {
        "id": "intro_1",
        "duration": 10,
        "text": "【请填写前言部分】" if default_comment_placeholders else ""
    }

    ending_clip_data = {
        "id": "ending_1",
        "duration": 10,
        "text": "【请填写后记部分】" if default_comment_placeholders else ""
    }

    video_config_data = {
        "intro": [intro_clip_data],
        "ending": [ending_clip_data],
        "main": [],
    }

    main_clips = []
    if clip_start_interval[1] > clip_start_interval[0]:
        clip_start_interval[1] = clip_start_interval[0]

    for song in b50_data:
        if not song['clip_id']:
            print(f"Error: 没有找到 {song['title']}-{song['level_label']}-{song['type']} 的clip_id，请检查数据格式，跳过该片段。")
            continue
        id = song['clip_id']
        video_name = f"{song['song_id']}-{song['level_index']}-{song['type']}"
        __image_path = os.path.join(images_path, id + ".png")
        __image_path = os.path.normpath(__image_path)
        if not os.path.exists(__image_path):
            print(f"Error: 没有找到 {id}.png 图片，请检查本地缓存数据。")
            __image_path = ""

        __video_path = os.path.join(videoes_path, video_name + ".mp4")
        __video_path = os.path.normpath(__video_path)
        if not os.path.exists(__video_path):
            print(f"Error: 没有找到 {video_name}.mp4 视频，请检查本地缓存数据。")
            __video_path = ""
        
        duration = clip_play_time
        start = random.randint(clip_start_interval[0], clip_start_interval[1])
        end = start + duration

        main_clip_data = {
            "id": id,
            "achievement_title": f"{song['title']}-{song['level_label']}-{song['type']}",
            "song_id": song['song_id'],
            "level_index": song['level_index'],
            "type": song['type'],
            "main_image": __image_path,
            "video": __video_path,
            "duration": duration,
            "start": start,
            "end": end,
            "text": "【请填写b50评价】" if default_comment_placeholders else ""
        }
        main_clips.append(main_clip_data)

    # 倒序排列（b15在前，b35在后）
    main_clips.reverse()

    video_config_data["main"] = main_clips

    with open(ouput_file, 'w', encoding="utf-8") as file:
        json.dump(video_config_data, file, ensure_ascii=False, indent=4)

    return video_config_data


def pre_gen():
    print("#####【mai-genb50视频生成器 - Step1 信息预处理和素材获取】#####")

    # Load global configuration
    load_global_config()

    print("#####【尝试从水鱼获取乐曲更新数据】 #####")
    try:
        fetch_music_data()
    except Exception as e:
        print(f"Error: 获取乐曲更新数据时发生异常: {e}")

    # 创建缓存文件夹
    cache_pathes = [
        f"./b50_datas",
        f"./b50_images",
        f"./videos",
        f"./videos/downloads",
    ]
    for path in cache_pathes:
        if not os.path.exists(path):
            os.makedirs(path)

    b50_raw_file = f"./b50_datas/b50_raw_{username}.json"
    b50_data_file = f"./b50_datas/b50_config_{username}.json"

    # init downloader
    print(f"##### 【当前配置信息】##### \n"
          f"  代理: {proxy if use_proxy else '未启用'}\n"
          f"  使用potoken: {use_potoken}\n"
          f"  使用oauth: {use_oauth}\n"
          f"  自动获取potoken: {use_auto_potoken}")
    downloader = PurePytubefixDownloader(
        proxy=proxy if use_proxy else None,
        use_potoken=use_potoken,
        use_oauth=use_oauth,
        auto_get_potoken=use_auto_potoken,
        search_max_results=search_max_results
    )

    if not use_all_cache:
        print("#####【1/4】获取用户的b50数据 #####")
        print(f"当前查询的水鱼用户名: {username}")
        b50_data = update_b50_data(b50_raw_file, b50_data_file, username)

        # 生成b50图片
        print("#####【2/4】生成b50背景图片 #####")
        image_output_path = f"./b50_images/{username}"
        if not os.path.exists(image_output_path):
            os.makedirs(image_output_path)

        b35_data = b50_data[:35]
        b15_data = b50_data[35:]
        try:
            generate_b50_images(username, b35_data, b15_data, image_output_path)
        except Exception as e:
            print(f"Error: 生成图片时发生异常: {e}")
            return 1

        print("#####【3/4】搜索b50视频信息 #####")
        try:
            b50_data = search_b50_videos(downloader, b50_data, b50_data_file, search_wait_time)
        except Exception as e:
            print(f"Error: 搜索视频信息时发生异常: {e}")
            return -1
        
        # 下载谱面确认视频
        print("#####【4/4】下载谱面确认视频 #####")
        video_download_path = f"./videos/downloads"  # 不同用户的视频缓存均存放在downloads文件夹下
        try:
            download_b50_videos(downloader, b50_data, video_download_path, search_wait_time)
        except Exception as e:
            print(f"Error: 下载视频时发生异常: {e}")
            return -1       
        
    else:
        print(f"#####【已配置 USE_ALL_CACHE=true ，使用本地缓存数据直接生成配置文件】 #####")
        print(f"##### 当前配置的水鱼用户名: {username} #####")
        print(f"##### 如要求更新数据，请配置 USE_ALL_CACHE=false #####")
    
    # 配置视频生成的配置文件
    config_output_file = f"./b50_datas/video_configs_{username}.json"
    try:
        configs = gene_resource_config(b50_data, image_output_path, video_download_path, 
                                   config_output_file, random_length=True)
    except Exception as e:
        print(f"Error: 生成视频配置时发生异常: {e}")
        return 1
    # TODO：一个web前端可以改变配置和选择视频片段的长度

    print(f"#####【预处理完成, 请在{config_output_file}中检查生成的配置数据并填写评论】 #####")
    return 0


if __name__ == "__main__":
    pre_gen()
    
