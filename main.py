from config import CHANNELS, OFFSET_DAYS, KEYWORDS
from databaser import DBaser
import pandas as pd
from grabber import grabber
from bot import Bot


def filter_data(df: pd.DataFrame,
                column: str,
                keywords: set = KEYWORDS) -> pd.DataFrame:
    """Filter dataframe by relevant KEYWORDS"""
    return df.loc[df[column].str.contains("|".join(keywords),
                                          case=False,
                                          regex=True,
                                          na=False)]


if __name__ == '__main__':
    # Aggregate data
    data = pd.DataFrame(data=grabber(channel_list=CHANNELS,
                                     offset_days=OFFSET_DAYS),
                        columns=["message_id", "chat_id",
                                 "channel", "date", "message",
                                 "views", "replies", "forwards"])

    # Create primary key
    data["id"] = (data["chat_id"].abs().map(str) + data["message_id"].map(str)).astype('int64')

    # Filter relevant data
    data_filtered = filter_data(df=data, column="message")

    # Create SQL database
    database = DBaser()

    if database.table_is_empty():
        target = "master"
    else:
        target = "slave"

    data_filtered.to_sql(name=target,
                         con=database.engine,
                         if_exists="replace",
                         index=False)

    # Detect new messages
    data_unique = pd.read_sql_query(sql="""SELECT * FROM slave WHERE id NOT IN (SELECT id FROM master);""",
                                    con=database.engine)

    # Insert new messages to master database
    data_unique.to_sql(name="master",
                       con=database.engine,
                       if_exists="append",
                       index=False)

    # Create bot and forward messages
    bot = Bot(name="hugh")

    for _, row in data_unique.iterrows():
        try:
            bot.forward_message(channel=row["channel"],
                                message_id=row["message_id"])
        except:
            bot.send_message(message=row["message"])