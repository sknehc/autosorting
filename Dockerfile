# 基础镜像
FROM python:3.8-slim-bullseye

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app:${PATH}"

# 安装必要的运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY *.py /app/

# 运行脚本
CMD ["python", "script.py"]
