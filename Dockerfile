############################################################
# Dockerfile
############################################################

FROM python:3.5

MAINTAINER contact.botigo@gmail.com

# Get the pip packages and clean up
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -rf /root/.cache/pip/*

COPY . /botigo

CMD ["python", "bot/manage.py", "runserver"]
