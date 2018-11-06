FROM python:3

RUN mkdir -p /opt/news_aggregator
WORKDIR /opt/news_aggregator

# Copy in python package for this app
ADD news_aggregator /opt/news_aggregator/news_aggregator
ADD news_aggregator_api /opt/news_aggregator/news_aggregator_api
ADD requirements.txt /opt/news_aggregator/
ADD manage.py /opt/news_aggregator/

RUN pip install -r requirements.txt
