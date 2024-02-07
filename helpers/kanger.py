# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserDeactivatedBan
from helpers.forwarder import ForwardMessage



async def Kanger(c: Client, m: Message):
    try:
        forward_from_chat = await c.get_chat(chat_id=Config.FORWARD_FROM_CHAT_ID[0])
        await m.edit(text=f"Successfully linked with `{forward_from_chat.title}`!")
    except Exception as err:
        await m.edit(text=f"Sorry, can't get the forward from chat!\n\nError: `{err}`")
        return

    for chat_id in Config.FORWARD_TO_CHAT_ID:
        try:
            forward_to_chat = await c.get_chat(chat_id=chat_id)
            if not forward_to_chat.permissions.can_send_messages:
                await m.edit(text=f"Sorry, you don't have permission to send messages in {forward_to_chat.title}!")
                return
            await m.edit(text=f"Successfully linked with `{forward_to_chat.title}`!")
        except Exception as err:
            await m.edit(text=f"Sorry, can't get the forward to chat!\n\nError: `{err}`")
            return

    await m.edit(text="Trying to forward now...")
    async for message in c.iter_history(chat_id=Config.FORWARD_FROM_CHAT_ID[0], reverse=True):
        await asyncio.sleep(Config.SLEEP_TIME)
        try:
            await ForwardMessage(c, message)
        except UserDeactivatedBan:
            await c.send_message(chat_id="me", text="Your account has been banned!")
            break
        except Exception as err:
            await c.send_message(chat_id="me", text=f"#ERROR: `{err}`")

    await m.edit(text="Channel files successfully kanged!\n\n©️ A Forwarder Userbot by @AbirHasan2005")
