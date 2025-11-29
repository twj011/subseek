FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config/ ./config/
COPY main.py .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露数据目录为卷
VOLUME ["/app/data"]

# 设置入口点
CMD ["python", "-m", "src.main"]
