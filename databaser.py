from sqlalchemy import Table, Column, BigInteger, DATETIME, Numeric, String, MetaData, create_engine
from sqlalchemy.orm import sessionmaker


class DBaser:
    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine("sqlite:///db", echo=True)
        self.tables = {key: self.create_table(key) for key in ("master", "slave")}
        self.session = sessionmaker(bind=self.engine)()
        self.create_all()
        print("Database created")

    def table_is_empty(self, table="master"):
        return self.session.query(self.tables[table]).first() is not None

    def create_table(self, name: str):
        return Table(name, self.meta,
                     Column("id", BigInteger, primary_key=True, unique=True),
                     Column("message_id", BigInteger, primary_key=True, unique=True),
                     Column("chat_id", BigInteger),
                     Column("channel", String),
                     Column("date", DATETIME),
                     Column("message", String),
                     Column("views", Numeric),
                     Column("replies", Numeric),
                     Column("forwards", Numeric),
                     )

    def create_all(self):
        self.meta.create_all(self.engine)
