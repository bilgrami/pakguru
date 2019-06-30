FROM bilgrami/python-base:latest
LABEL Name=pakguru Version=0.1.1 maintainer="Syed Bilgrami <bilgrami@gmail.com>"


ARG PROJECT_ROOT=/usr/local/project
ARG CONFIG_ROOT=$PROJECT_ROOT/config
ENV VIRTUAL_ENV=$PROJECT_ROOT/.virtualenvs/myproject_env


# Create virtual environment
RUN mkdir -p $PROJECT_ROOT; \
    mkdir -p $VIRTUAL_ENV; \ 
    python -m venv $VIRTUAL_ENV; 

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PROJECT_ROOT $PROJECT_ROOT
# install python packages
WORKDIR $PROJECT_ROOT
COPY requirements.txt requirements.txt
RUN  python -m pip install --upgrade pip && \
     pip install -r requirements.txt; 
ADD ./project $PROJECT_ROOT 


# **** Server ****
ENV SERVER_PORT=5000
ENV iPYTHON_NOTEBOOK_PORT=8888
ENV UWSGI_INI=uwsgi.ini
ENV STATIC_URL=/static/
ENV LISTEN_PORT=5000
ENV PYTHONUNBUFFERED 1
EXPOSE $SERVER_PORT
EXPOSE $iPYTHON_NOTEBOOK_PORT
STOPSIGNAL SIGINT

RUN \
 apt-get update && \
 apt-get install -qy --no-install-recommends \
   openssh-server redis-tools && \
 rm -rf /var/lib/apt/lists/* && \
 mkdir -p /home/LogFiles /opt/startup && \
 echo "root:Docker!" | chpasswd 

COPY docker/startup /opt/startup
COPY docker/startup/sshd_config /etc/ssh/

COPY docker/startup/ssh_setup.sh /tmp
RUN chmod -R +x /opt/startup \
   && chmod -R +x /tmp/ssh_setup.sh \
   && (sleep 1;/tmp/ssh_setup.sh 2>&1 > /dev/null) \
   && rm -rf /tmp/* \
   && cd /opt/startup

ENV SSH_PORT 2222
EXPOSE 80 2222
ENV PRODUCT_VERSION 0.1.1

ENTRYPOINT ["/opt/startup/init_container.sh"]
