# Add-danmaku

B站录播加弹幕 Add danmaku to live recordings

这个工具本是专为给[B站录播姬](https://rec.danmuji.org/)生成的录播视频加弹幕而写的，后面又完善了一些功能。

本脚本的功能有：

- 用 B站录播姬 生成的录播文件生成带弹幕的录播视频
- 为视频添加 `.ass` 格式的字幕
- 将 flv 转换为 mp4
- 计算直播流水

本脚本用到的工具: [ffmpeg](https://github.com/FFmpeg/FFmpeg) [DanmakuFactory](https://github.com/hihkm/DanmakuFactory)

**注意：该脚本目前只能在 Windows 下运行**

依赖：

- 配置好 `ffmpeg` 的环境变量
- 安装 `ffmpeg-python` : `pip install ffmpeg-python`

用法：

```shell
python autotrans.py -folder [folder 视频文件夹] -b [码率（单位：kbps）]
```

只要指定文件夹，脚本能自动识别到文件夹下所有视频，批量加弹幕。
完成后会在原视频目录下生成和原视频同名的 `.mp4` 格式视频，同时在控制台输出直播流水。

其它脚本的功能：

```shell
# flv 转 mp4 格式，速度极快，不需要指定码率（和原视频一致）
python flv2mp4.py -folder [folder 视频文件夹]

# mp4 格式加 ass 字幕，生成 mp4，新生成的文件会在源文件后面加 "_ass" 后缀
python mp4tomp4withass.py -folder [folder 视频文件夹] -b [码率（单位：kbps）]

# flv 格式加 ass 字幕，生成 mp4，ass 字幕文件需要与视频在同一文件夹下且与视频同名
python flv2mp4withass.py -folder [folder 视频文件夹] -b [码率（单位：kbps）]

# 计算文件夹内直播内容的总流水
python incomestat.py -folder [folder 视频文件夹]
```

## Todo

* [ ] 支持Linux
* [ ] 优化代码结构与执行效率
* [ ] 发布至 pypi，实现命令行直接调用
