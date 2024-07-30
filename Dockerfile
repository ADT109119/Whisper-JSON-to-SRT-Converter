# 使用 Python slim 作為基礎映像
FROM python:3.10.12-slim

WORKDIR /app

ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
