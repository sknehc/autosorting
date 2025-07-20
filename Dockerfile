# 第一阶段：构建依赖
FROM python:3.8-slim-bullseye AS builder

# 设置工作目录
WORKDIR /app

# 安装编译工具（仅构建阶段需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段：运行环境（体积更小）
FROM python:3.8-alpine

# 设置工作目录
WORKDIR /app

# 安装必要的运行时依赖
RUN apk add --no-cache \
    libstdc++  # 可能需要的运行时库

# 复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 复制应用代码
COPY *.py /app/

# 设置环境变量
ENV PATH="/opt/venv/bin:$PATH"

# 运行脚本
CMD ["python", "script.py"]
