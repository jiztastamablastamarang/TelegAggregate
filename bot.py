from credentials import API_ID, API_HASH, MY_ID
from telethon import TelegramClient


class Bot:
    def __init__(self, name, api_id=API_ID, api_hash=API_HASH):
        self.client = TelegramClient(name, api_id, api_hash)

    def send_message(self, receiver=MY_ID, message="Hey!"):
        with self.client:
            self.client.loop.run_until_complete(self.messenger(receiver=receiver, message=message))

    def forward_message(self, channel, message_id):
        with self.client:
            self.client.loop.run_until_complete(self.forwarder(channel=channel, message_id=message_id))

    async def messenger(self, receiver, message):
        await self.client.send_message(receiver, message)

    async def forwarder(self, channel, message_id):
        await self.client.forward_messages(entity=MY_ID, messages=message_id, from_peer=channel)
