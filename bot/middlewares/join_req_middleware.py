from typing import Any, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class JoinRequirementMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.CHANNEL_IDS = [-1002636831304]

    async def __call__(self, handler, event: Message | CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any:
        if event.callback_query or event.message or event.callback_query.data == "is_join_chekker":
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
            if unsubscribers:
                ikb = InlineKeyboardBuilder()
                for channel_id in unsubscribers:
                    channel = (await bot.get_chat(channel_id)).model_dump()
                    ikb.add(
                        InlineKeyboardButton(text=channel['title'], url=channel["invite_link"])
                    )
                ikb.add(InlineKeyboardButton(text="A'zo bo'ldim✅", callback_data="is_join_chekker"))
                ikb.adjust(1, repeat=True)
                if event.callback_query:
                    try:
                        await event.callback_query.message.edit_reply_markup(reply_markup=ikb.as_markup())
                    except:
                        await event.callback_query.answer("Hali hammasiga a'zo bo'lmading ALDAYSANKU SARDOR!")
                else:
                    await event.message.answer("Oldin kanallarga a'zo bo'ling👇", reply_markup=ikb.as_markup())
                    return
            else:
                if event.callback_query:
                    await event.callback_query.message.delete()
                    await event.callback_query.message.answer("Muvofaqqiyatliy tekshirildingiz qayta boshlash ➡ /start")
        return await handler(event, data)
