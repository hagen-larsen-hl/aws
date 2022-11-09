FROM python:3.7
COPY consumer.py /consumer.py
COPY tools /tools
COPY widget /widget
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "/consumer.py", "sqs", "https://sqs.us-east-1.amazonaws.com/713236084914/cs5260-requests", "s3", "usu-cs5260-hagen-requests"]