from typing import Any, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, CallbackQuery


class JoinRequirementMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.CHANNEL_IDS = [-1002636831304]

    async def __call__(self, handler, event: Message | CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any:
        if event.callback_query or event.message:
            bot: Bot = data['bot']
            if event.callback_query:
                user = event.callback_query.from_user
            else:
                user = event.message.from_user
            unsubscribers = []
            for channel_id in self.CHANNEL_IDS:
                member = await bot.get_chat_member(channel_id, user.id)
                if member.status == ChatMemberStatus.LEFT:
                    unsubscribers.append(channel_id)
        return await handler(event, data)
