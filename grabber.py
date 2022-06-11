import asyncio
import credentials
from typing import List
from telethon.sync import TelegramClient
from datetime import datetime, timedelta


def grabber(channel_list: List,
            offset_days: int) -> List:
    """Grab channels by OFFSET_DAYS"""
    client: TelegramClient = TelegramClient('name',
                                            credentials.API_ID,
                                            credentials.API_HASH)
    with client:
        data = client.loop.run_until_complete(asya(channel_list=channel_list,
                                                   offset_days=offset_days,
                                                   client=client))

    return data


async def asya(channel_list: List,
               offset_days: int,
               client: TelegramClient) -> asyncio.coroutines:
    """Asynchronous data collection"""
    channel_list = [c.split("/")[-1] if c.count("/") else c  # clean channel name
                    for c in channel_list if c]
    raw: List = []
    print("\033[1;31;40m"
          "Monitor channels:"
          "\t\033[1;37;40m")
    print(*channel_list, sep="\n", end="\033[0m\n")

    offset_date = int((datetime.now() - timedelta(days=offset_days)).timestamp())

    for channel in channel_list:
        async for m in client.iter_messages(entity=channel,
                                            offset_date=offset_date,
                                            reverse=True):
            raw.append((
                m.id,
                m.chat_id,
                m.chat.username,
                m.date,
                m.raw_text,
                m.views,
                m.replies.replies if m.replies else None,
                m.forwards,
            ))
    return raw
