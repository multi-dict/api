FROM python:3.5
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY src/ /src/
WORKDIR /src
EXPOSE 8000
CMD python main.py
