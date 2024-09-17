import os
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

#递归地删除给定目录下的所有空子目录
def del_emptydir(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # 如果是目录，则递归调用
            del_emptydir(item_path)
            # 再次检查目录是否为空
            if os.listdir(item_path):
                try:
                    # 如果为空，则删除
                    os.rmdir(item_path)
                    log_message("已删除空目录: " + item_path)
                except Exception as e:
                    log_message("删除空目录失败 "+ item_path)
                    print(repr(e))
def get_music_file_info(file_path):
    song_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma']
    file_type = os.path.splitext(file_path)[1]
    file_name = os.path.basename(file_path)

    if file_type.lower() in song_extensions:
        try:
            audio = TinyTag.get(file_path)
            # 对应歌手目录
            zpath = audio.artist.split('/')[0] if audio.artist else "未知歌手"
            # 所有歌手名称，用顿号拼接
            artist = audio.artist.replace('/', '、') if audio.artist else "未知歌手"
            # 获取专辑信息
            album = audio.album if audio.album else "未知专辑"
            # 获取歌名
            title = audio.title

            if  artist == "未知歌手" and artist == "未知专辑":
                # 未知歌曲保留原来的文件名
                n_title = file_name
            else:
                # 重命名后的歌曲名称
                n_title = artist + " - "+ title + file_type

            # 返回信息
            return {
                '歌手目录': zpath,
                '专辑目录': album,
                '歌名': n_title
            }
        except Exception as e:
            log_message("无法读取文件 "+ file_path)
            print(repr(e))
    return None

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
                    if info is not None:
                        artistpath = info['歌手目录']
                        album = info['专辑目录']
                        title = info['歌名']

                        # 创建子目录
                        album_dir = os.path.join(output_dir, artistpath, album)
                        n_filepath = os.path.join(album_dir,title)
                        Path(album_dir).mkdir(parents=True, exist_ok=True)

                        try:
                            # 移动文件到相应子目录
                            shutil.move(filepath, n_filepath)
                            log_message(filepath +" ===已移动成功")
                        except Exception as e:
                            log_message(filepath+"：移动时意外错误")
                            print(repr(e))
            except Exception as e:
                log_message(filepath+"：整理时意外错误")
                print(repr(e))
    del_emptydir(source_dir)
    log_message("定时任务执行已完成")

if __name__ == "__main__":
    while True:
        auto_sorting("/input", "/output")
        time.sleep(120)