# 使用官方Python 3.8镜像作为基础镜像
FROM python:3.8-alpine
# 设置工作目录
WORKDIR /app
# 复制当前目录下的所有文件到工作目录
COPY . /app
# 安装所需的依赖
RUN pip install tinytag==1.10.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
# 运行脚本
CMD ["/usr/local/bin/python", "/app/script.py"]