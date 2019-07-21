FROM python:3.6.9-slim
MAINTAINER Filip Hans
ADD . .
VOLUME ["/settings"]
RUN pip install -r requirements.txt
CMD ["python", "./bot.py"]