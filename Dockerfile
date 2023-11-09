FROM python:3.10-alpine

RUN addgroup discord_bot && adduser -D -G  discord_bot discord_bot

WORKDIR /home/discord_bot

COPY ./ezcampus ./ezcampus
COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

USER discord_bot

ENV PATH="${PATH}:/home/discord_bot/"

RUN pip install -r requirements.txt

ENTRYPOINT ["/home/discord_bot/entrypoint.sh"]
