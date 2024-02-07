FROM sunnycapt/cx_oracle-python
ENV LANG C.UTF-8

WORKDIR /home/platform

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
 
# CMD ["sh", "shmp3.sh"]
CMD ["nameko","run","--config","amqp.yaml","Service:PlatformService"]