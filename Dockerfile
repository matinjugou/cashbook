FROM python:3.6
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /app
ENTRYPOINT python app.py
