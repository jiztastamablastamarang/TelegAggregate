import credentials
import config
from typing import List
from telethon.sync import TelegramClient, events
import pandas as pd
from datetime import datetime, timedelta


async def grabber(channel_list, offset_days=7) -> None:
    channel_list = [c.split("/")[-1] if c.count("/") else c  # clean channel name
                    for c in channel_list if c]

    print("\033[1;31;40mMonitor channels:\t\033[1;37;40m")
    print(*channel_list, sep="\n")

    offset_date = int((datetime.now() - timedelta(days=offset_days)).timestamp())

    for channel in channel_list:
        async for m in client.iter_messages(entity=channel,
                                            offset_date=offset_date,
                                            reverse=True):
            raw.append((m.id,
                        m.chat_id,
                        m.chat.username,
                        m.date,
                        m.raw_text,
                        m.views,
                        m.replies.replies if m.replies else None,
                        m.forwards,))


def filter_data(df: pd.DataFrame, column: str, keywords: set):
    return df.loc[df[column].str.contains("|".join(keywords),
                                          case=False,
                                          regex=True,
                                          na=False)]


if __name__ == '__main__':
    client: TelegramClient = TelegramClient('name', credentials.API_ID, credentials.API_HASH)
    raw: List = []
    with client:
        client.loop.run_until_complete(grabber(config.CHANNELS))

    data = pd.DataFrame(raw, columns=["id", "chat_id", "chanel", "date", "message", "views", "replies", "forwards"])
    filtered = filter_data(df=data,
                           column="message",
                           keywords=config.KEYWORDS)
