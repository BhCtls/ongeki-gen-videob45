import json

# 原始数据
data = {"propertyKey":"rating_base_new_best",
    "propertyValue":"1027:3:1002902,8169:10:1007246,1022:3:1006986,989:3:1005312,994:3:1006670,1028:3:1006083,1031:3:999603,848:3:1005841,944:3:1006039,8175:10:1002819,943:3:1002592,1003:3:1005031,1011:3:1004748,990:3:1000405,1035:3:1004535"},


# 拆分 propertyValue
entries = data["propertyValue"].split(',')

# 转换为目标格式
result = []
for entry in entries:
    id_, level, score = entry.split(':')
    result.append({
        "id": int(id_),
        "level": int(level),
        "score": int(score),
        "isnew": True
    })

# 输出结果
print(json.dumps(result, indent=2))



'''
[
  {
    "id": 728,
    "level": 3,
    "score": 1002645,
    "isnew": false
  },
  {
    "id": 803,
    "level": 3,
    "score": 1004126,
    "isnew": false
  },
  {
    "id": 8115,
    "level": 10,
    "score": 1005860,
    "isnew": false
  },
  {
    "id": 682,
    "level": 3,
    "score": 1004316,
    "isnew": false
  },
  {
    "id": 8089,
    "level": 10,
    "score": 1005680,
    "isnew": false
  },
  {
    "id": 830,
    "level": 3,
    "score": 1002914,
    "isnew": false
  },
  {
    "id": 766,
    "level": 3,
    "score": 1000984,
    "isnew": false
  },
  {
    "id": 585,
    "level": 3,
    "score": 1006989,
    "isnew": false
  },
  {
    "id": 764,
    "level": 3,
    "score": 1006889,
    "isnew": false
  },
  {
    "id": 736,
    "level": 3,
    "score": 1006685,
    "isnew": false
  },
  {
    "id": 890,
    "level": 3,
    "score": 1005069,
    "isnew": false
  },
  {
    "id": 540,
    "level": 3,
    "score": 1004829,
    "isnew": false
  },
  {
    "id": 98,
    "level": 3,
    "score": 1004832,
    "isnew": false
  },
  {
    "id": 740,
    "level": 3,
    "score": 996361,
    "isnew": false
  },
  {
    "id": 469,
    "level": 3,
    "score": 1004701,
    "isnew": false
  },
  {
    "id": 8163,
    "level": 10,
    "score": 1006201,
    "isnew": false
  },
  {
    "id": 391,
    "level": 3,
    "score": 1006016,
    "isnew": false
  },
  {
    "id": 590,
    "level": 3,
    "score": 995788,
    "isnew": false
  },
  {
    "id": 168,
    "level": 3,
    "score": 1005802,
    "isnew": false
  },
  {
    "id": 801,
    "level": 3,
    "score": 1000633,
    "isnew": false
  },
  {
    "id": 763,
    "level": 3,
    "score": 996422,
    "isnew": false
  },
  {
    "id": 969,
    "level": 3,
    "score": 1006307,
    "isnew": false
  },
  {
    "id": 470,
    "level": 3,
    "score": 1003014,
    "isnew": false
  },
  {
    "id": 484,
    "level": 3,
    "score": 1006079,
    "isnew": false
  },
  {
    "id": 758,
    "level": 3,
    "score": 1006129,
    "isnew": false
  },
  {
    "id": 522,
    "level": 3,
    "score": 1008166,
    "isnew": false
  },
  {
    "id": 496,
    "level": 3,
    "score": 1002695,
    "isnew": false
  },
  {
    "id": 565,
    "level": 3,
    "score": 1005235,
    "isnew": false
  },
  {
    "id": 870,
    "level": 3,
    "score": 1006390,
    "isnew": false
  },
  {
    "id": 765,
    "level": 3,
    "score": 1003200,
    "isnew": false
  }
]
'''