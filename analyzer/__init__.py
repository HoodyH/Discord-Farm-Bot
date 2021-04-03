from typing import List
from discord import Message
from datetime import datetime, timedelta


class AnalyzerInterface:
    """
    Class to collect reply messages after an automated command, to analyze and do actions with the received messages
    """
    messages: List[Message] = []

    creation_time = datetime.now()
    reply_time_range = 500
    target_user_id = None
    target_channel_id = None

    @property
    def is_active(self) -> bool:
        if datetime.now() < self.creation_time + timedelta(seconds=self.reply_time_range):
            return True
        return False

    def identify_message(self, message: Message) -> bool:
        if message.channel.id == self.target_channel_id and message.author.id == self.target_user_id:
            return True
        return False

    def add_message(self, message: Message):
        self.messages.append(message)
