import json

data= [
    {
    "id": 728,
    "level": 3,
    "score": 1002645,
    "isnew": False
  },
  {
    "id": 803,
    "level": 3,
    "score": 1004126,
    "isnew": False
  },
  {
    "id": 8115,
    "level": 10,
    "score": 1005860,
    "isnew": False
  },
  {
    "id": 682,
    "level": 3,
    "score": 1004316,
    "isnew": False
  },
  {
    "id": 8089,
    "level": 10,
    "score": 1005680,
    "isnew": False
  },
  {
    "id": 830,
    "level": 3,
    "score": 1002914,
    "isnew": False
  },
  {
    "id": 766,
    "level": 3,
    "score": 1000984,
    "isnew": False
  },
  {
    "id": 585,
    "level": 3,
    "score": 1006989,
    "isnew": False
  },
  {
    "id": 764,
    "level": 3,
    "score": 1006889,
    "isnew": False
  },
  {
    "id": 736,
    "level": 3,
    "score": 1006685,
    "isnew": False
  },
  {
    "id": 890,
    "level": 3,
    "score": 1005069,
    "isnew": False
  },
  {
    "id": 540,
    "level": 3,
    "score": 1004829,
    "isnew": False
  },
  {
    "id": 98,
    "level": 3,
    "score": 1004832,
    "isnew": False
  },
  {
    "id": 740,
    "level": 3,
    "score": 996361,
    "isnew": False
  },
  {
    "id": 469,
    "level": 3,
    "score": 1004701,
    "isnew": False
  },
  {
    "id": 8163,
    "level": 10,
    "score": 1006201,
    "isnew": False
  },
  {
    "id": 391,
    "level": 3,
    "score": 1006016,
    "isnew": False
  },
  {
    "id": 590,
    "level": 3,
    "score": 995788,
    "isnew": False
  },
  {
    "id": 168,
    "level": 3,
    "score": 1005802,
    "isnew": False
  },
  {
    "id": 801,
    "level": 3,
    "score": 1000633,
    "isnew": False
  },
  {
    "id": 763,
    "level": 3,
    "score": 996422,
    "isnew": False
  },
  {
    "id": 969,
    "level": 3,
    "score": 1006307,
    "isnew": False
  },
  {
    "id": 470,
    "level": 3,
    "score": 1003014,
    "isnew": False
  },
  {
    "id": 484,
    "level": 3,
    "score": 1006079,
    "isnew": False
  },
  {
    "id": 758,
    "level": 3,
    "score": 1006129,
    "isnew": False
  },
  {
    "id": 522,
    "level": 3,
    "score": 1008166,
    "isnew": False
  },
  {
    "id": 496,
    "level": 3,
    "score": 1002695,
    "isnew": False
  },
  {
    "id": 565,
    "level": 3,
    "score": 1005235,
    "isnew": False
  },
  {
    "id": 870,
    "level": 3,
    "score": 1006390,
    "isnew": False
  },
  {
    "id": 765,
    "level": 3,
    "score": 1003200,
    "isnew": False
  },
  {
    "id": 1027,
    "level": 3,
    "score": 1002902,
    "isnew": True
  },
  {
    "id": 8169,
    "level": 10,
    "score": 1007246,
    "isnew": True
  },
  {
    "id": 1022,
    "level": 3,
    "score": 1006986,
    "isnew": True
  },
  {
    "id": 989,
    "level": 3,
    "score": 1005312,
    "isnew": True
  },
  {
    "id": 994,
    "level": 3,
    "score": 1006670,
    "isnew": True
  },
  {
    "id": 1028,
    "level": 3,
    "score": 1006083,
    "isnew": True
  },
  {
    "id": 1031,
    "level": 3,
    "score": 999603,
    "isnew": True
  },
  {
    "id": 848,
    "level": 3,
    "score": 1005841,
    "isnew": True
  },
  {
    "id": 944,
    "level": 3,
    "score": 1006039,
    "isnew": True
  },
  {
    "id": 8175,
    "level": 10,
    "score": 1002819,
    "isnew": True
  },
  {
    "id": 943,
    "level": 3,
    "score": 1002592,
    "isnew": True
  },
  {
    "id": 1003,
    "level": 3,
    "score": 1005031,
    "isnew": True
  },
  {
    "id": 1011,
    "level": 3,
    "score": 1004748,
    "isnew": True
  },
  {
    "id": 990,
    "level": 3,
    "score": 1000405,
    "isnew": True
  },
  {
    "id": 1035,
    "level": 3,
    "score": 1004535,
    "isnew": True
  }
]

with open('ongekimusic.json', 'r', encoding='utf-8') as f:
    lib = json.load(f)

def cauculate_rating(score, ds):
  if score >= 1007500:
    ra = round(ds + 2, 2)
  elif score >= 1000000:
    ra = round(ds + int((score-1000000)/150)*0.01 + 1.5, 2)
  else:
    ra = round(ds + int((score-970000)/200)*0.01, 2)
  return ra


def calculate_dengji(ds):
    if ds >= 15.0:
        return "15"
    elif ds >= 14.7:
        return "14+"
    else:
        return "14"

# 构造 output
output_list = []
for entry in data:
    song_id = entry["id"]
    difficulty = entry["level"]
    score = entry["score"]
    isnew = entry["isnew"]

    # 查找对应的歌曲信息
    song_info = next((item for item in lib if item["id"] == song_id), None)
    if not song_info:
        continue

    # 获取歌曲名称和难度信息
    song_name = song_info["name"]
    ds = float(song_info[f"level{difficulty}"].split(',')[0]) if f"level{difficulty}" in song_info else 0.0

# 初始化计数器
best_counter = 1
new_counter = 1

# 构造 output
output_list = []
for entry in data:
    song_id = entry["id"]
    difficulty = entry["level"]
    score = entry["score"]
    isnew = entry["isnew"]

    if difficulty == 10:
      difficulty = 4

     


    # 查找对应的歌曲信息
    song_info = next((item for item in lib if item["id"] == song_id), None)
    if not song_info:
        continue

    # 获取歌曲名称和难度信息
    song_name = song_info["name"]
    ds = float(song_info.get(f"level{difficulty}", "0").replace(',', '.'))

    # 根据 isnew 设置 clip_id
    if isnew:
        clip_id = f"new_{new_counter}"
        new_counter += 1
    else:
        clip_id = f"best_{best_counter}"
        best_counter += 1

    # 构造 output
    output = {
        "achievements": score,
        "ds": ds,
        "fc": "",
        "fs": "sync",
        "level": calculate_dengji(ds),  # 固定值
        "level_index": difficulty,
        "level_label": "Master" if difficulty == 3 else "Lunatic",
        "ra": cauculate_rating(score,ds), 
        "rate": "sss",  # 固定值
        "song_id": song_id,
        "title": song_name,
        "type": "SD",
        "clip_id": clip_id,  # 根据 isnew 动态生成
        "video_info_list": [],  # 空
        "video_info_match": {}  # 空
    }
    output_list.append(output)

# 输出结果
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_list, f, indent=2, ensure_ascii=False)