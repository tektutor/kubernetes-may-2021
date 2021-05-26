FROM alpine:3.12

RUN apk add --no-cache python3 py3-pip

RUN pip3 install flask

COPY hello.py /hello.py

WORKDIR /

EXPOSE 80 

CMD [ "python3", "hello.py" ]
