## 音击b45生成器

### 1. 介绍
根据b50生成器修改了一天，做出的比较丑陋的b45生成。

### 2. 使用流程
1. 将自己的rating结构化。可以使用各种小脚本中的东西。
tovideo.py可以将特定格式的rating结构转换为可以用的rating。格式与本家有所不同！！！！
2. 将output.json塞进b50_datas文件夹，强制替换b50为b45。
3. 访问rin服面板 https://portal.naominet.live/ongeki/rating ， ctrl+s保存，获得曲绘文件（要求小号曲绘的webp文件；如果您需要输入其他曲绘文件也可以，请在util/util.py里面修改！），放入images/Jackets文件夹。

4. 运行服务器，执行第一步的图片生成。建议先将images/b50videobase图片替换成自己想要的。本人提供了psd文件可以直接修改。
可以在st_pages/1_Setup_Achivments中st_generate_b50_images修改最佳曲目数量，新曲数量，以及prefix这种东西（"ベスト" if index < 30 else "新曲"）

5. 图片生成完毕后，由于bug原因，需要对其批量改名为best_xx和new_xx。

6. 搜索视频。
若对搜索关键词不满意，可以在pre_gen.py中的get_keyword方法，进行修改。

7. 视频的大小尽量为谱面确认/nif的手元。这两种视频来源都可以直接拼接。
若确实需要改变视频的大小或位置，请调整gene_video.py中create_video_segment方法的“#计算位置”参数。

8. 如果撰写评论的页面出现问题，可以参照控制台。

7.Enjoy！（哎想想就气，本人一忙忙了一天）
