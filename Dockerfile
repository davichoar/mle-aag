FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
    
ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

COPY . /app

EXPOSE 8080

CMD ["bash", "pipeline_and_deploy.sh"]