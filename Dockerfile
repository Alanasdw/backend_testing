FROM golang:1.13.6

RUN apt update && \
    export PATH=$PATH:/usr/local/go/bin && \
    go get -u -v github.com/gocelery/gocelery && \
    apt install -y gcc-multilib

CMD tail -f /dev/null
EXPOSE 8787