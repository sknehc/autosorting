# 基础镜像
FROM python:3.8-slim-bullseye

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY *.py /app/

# 运行脚本
CMD ["python", "script.py"]
