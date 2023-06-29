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

COPY --chown=bot_user:bot_user . /bot

ENTRYPOINT ["python3", "bot.py"]
