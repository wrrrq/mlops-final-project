# 使用 slim 版本的 Python 3.12，体积小
FROM python:3.12-slim

# 设置容器内的工作目录为 /app
WORKDIR /app

# 先只拷贝依赖文件，安装依赖。利用缓存，如果代码变了但依赖没变，这步不用重跑
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝应用代码和模型
COPY app/ ./app/


# 暴露 8000 端口（FastAPI 的默认端口）
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
