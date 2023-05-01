FROM alpine:latest

RUN apk update \
    && apk upgrade \
    && apk add \
       python3 \
       py3-pip \
       py3-wheel

RUN adduser -D bot_user
USER bot_user
WORKDIR /bot

RUN pip install --user pytelegrambotapi

ENV PATH="/home/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser . /bot

ENTRYPOINT ["python3", "bot.py"]
