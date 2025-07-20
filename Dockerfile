# 第一阶段：构建环境（可选）
FROM python:3.8-slim-bullseye as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# 第二阶段：运行环境
FROM python:3.8-slim-bullseye
WORKDIR /app

# 从构建阶段复制依赖（若使用多阶段构建）
# COPY --from=builder /root/.local /root/.local

# 复制应用文件
COPY . .

# 安装依赖
RUN pip install --no-cache-dir --trusted-host pypi.tuna.tsinghua.edu.cn \
    tinytag==1.10.1 -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    adduser -D appuser && chown -R appuser /app

# 环境变量
ENV PATH=/root/.local/bin:$PATH
USER appuser

# 启动命令
CMD ["python", "script.py"]
