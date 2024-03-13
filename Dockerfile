FROM sunnycapt/cx_oracle-python
ENV LANG C.UTF-8

WORKDIR /home/platform

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .
 
CMD ["sh", "pf.sh"]
# CMD ["nameko","run","--config","amqp.yaml","Service:PlatformService"]