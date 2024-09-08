import os
import re
import shutil
import datetime
import time
from tinytag import TinyTag
from pathlib import Path

def log_message(message):
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 打印日志信息，包含时间戳
    print(f"{current_time} - 日志信息: {message}")

def get_first_artist(artist):
    delimiters = ['、', '&']
    # 初始化变量
    current_substring = ""
    found = False
    # 遍历字符串中的每个字符
    for char in artist:
        if char not in delimiters:
            # 如果字符不是分隔符，开始构建子字符串
            if not found:
                current_substring = char
                found = True
            else:
                current_substring += char
        else:
            # 如果遇到分隔符，且已经找到第一个非分隔符的子字符串，则跳出循环
            if found:
                break
    return current_substring.strip()

def get_music_file_info(file_path):
    song_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma']
    file_type = os.path.splitext(file_path)[1]
    file_name = os.path.basename(file_path)

    if file_type.lower() in song_extensions:
        try:
            audio = TinyTag.get(file_path)
            # 子目录
            zpath = get_first_artist(audio.artist) if audio.artist else "未知歌手"
            # 获取歌手信息
            artist = audio.artist if audio.artist else "未知歌手"
            # 获取专辑信息
            album = audio.album if audio.album else "未知专辑"
            # 获取歌名
            title = audio.title
            # 返回信息
            return {
                '是否音乐': 1,
                '歌手目录': zpath,
                '歌手': artist,
                '歌名': title,
                '专辑': album,
                '源文件名': file_name,
                '文件类型': file_type
            }
        except Exception as e:
            log_message("无法读取文件 "+ file_path)
    return {
        '是否音乐': 0
    }

def auto_sorting(source_dir, output_dir):
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # 遍历音乐目录
    for subdir, _, files in os.walk(source_dir):
        for filename in os.listdir(subdir):
            try:
                filepath = os.path.join(subdir, filename)
                #print(filepath)
                if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
                    # 读取文件信息
                    info = get_music_file_info(filepath)
                    # 是音乐文件则处理
                    if info['是否音乐'] == 1:
                        artistpath = info['歌手目录']
                        artist = info['歌手']
                        title = info['歌名']
                        album = info['专辑']
                        filetname = info['源文件名']
                        filetype = info['文件类型']
                        # 去除非法字符
                        illegal_chars_pattern = re.compile(r'[^\w_ -]')
                        safe_artistpath = illegal_chars_pattern.sub('', artistpath)
                        safe_album = illegal_chars_pattern.sub('', album)

                        # 创建艺术家和标题的子目录
                        album_dir = os.path.join(output_dir, safe_artistpath, safe_album)

                        if  artist == "未知歌手" and artist == "未知专辑":
                            new_filename = os.path.join(album_dir, filetname)
                        else:
                            new_filename = os.path.join(album_dir, artist+' - '+title+filetype)

                        Path(album_dir).mkdir(parents=True, exist_ok=True)

                        # 移动文件到相应子目录
                        try:
                            shutil.move(filepath, new_filename)
                            log_message(filepath +" ===已成功")
                        except Exception as e:
                            log_message(filename+"：整理时意外错误")
            except Exception as e:
                log_message(filename+"：整理时意外错误")
    log_message("定时任务执行已完成")

if __name__ == "__main__":
    while True:
        time.sleep(30)
        auto_sorting("/input", "/output")