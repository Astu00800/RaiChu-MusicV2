from Process.Cache.admins import admins
from Process.main import call_py
from pyrogram import filters
from Process.decorators import authorized_users_only
from Process.filters import command, other_filters
from Process.queues import QUEUE, clear_queue
from Process.main import bot as Client
from Process.utils import skip_current_song, skip_item
from RaiChu.config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL, IMG_5
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from RaiChu.inline import stream_markup

bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Go Back", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 Close", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ Bot 𝐑𝐄𝐋𝐎𝐀𝐃𝐄𝐃 correctly !\n✅ **𝐀𝐃𝐌𝐈𝐍 𝐋𝐈𝐒𝐓** has **updated !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Mᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• Cʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐏𝐋𝐀𝐘𝐈𝐍𝐆.")
        elif op == 1:
            await m.reply("✅ __Queues__ **is empty.**\n\n**• userbot leaving voice chat**")
        elif op == 2:
            await m.reply("🗑️ **Clearing the Queues**\n\n**• userbot leaving voice chat**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **𝐒𝐊𝐈𝐏𝐏𝐄𝐃 𝐓𝐎 𝐓𝐇𝐄 𝐍𝐄𝐗𝐓 𝐓𝐑𝐀𝐂𝐊.**\n\n🏷 **𝐍𝐀𝐌𝐄:** [{op[0]}]({op[1]})\n💭 **𝐂𝐇𝐀𝐓:** `{chat_id}`\n💡 **𝐒𝐓𝐀𝐓𝐔𝐒:** `Playing`\n🎧 **𝐑𝐄𝐐𝐔𝐄𝐒𝐓𝐄𝐃 𝐁𝐘:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **𝐑𝐄𝐌𝐎𝐕𝐄𝐃 song from queue:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ The 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 has 𝐃𝐈𝐒𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐄𝐃 from the Video chat.")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆.**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **𝐓𝐑𝐀𝐂𝐊 𝐏𝐀𝐔𝐒𝐄𝐃.**\n\n• **To 𝐑𝐄𝐒𝐔𝐌𝐄 the stream, use the**\n» /resume command."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆.**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **Track 𝐑𝐄𝐒𝐔𝐌𝐄𝐃.**\n\n• **To 𝐏𝐀𝐔𝐒𝐄 the stream, use the**\n» /pause command."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆.**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐌𝐔𝐓𝐄𝐃.**\n\n• **To 𝐔𝐍𝐌𝐔𝐓𝐄 the userbot, use the**\n» /unmute command."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆.**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐔𝐍𝐌𝐔𝐓𝐄𝐃.**\n\n• **To 𝐌𝐔𝐓𝐄 the userbot, use the**\n» /mute command."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆.**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ 𝐓𝐇𝐄 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐀𝐒 𝐏𝐀𝐔𝐒𝐄𝐃", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ 𝐓𝐇𝐄 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐀𝐒 𝐑𝐄𝐒𝐔𝐌𝐄𝐃", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **𝐓𝐇𝐄 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆 𝐇𝐀𝐒 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 𝐄𝐍𝐃𝐄𝐃**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 𝐌𝐔𝐓𝐄𝐃", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 𝐔𝐒𝐄𝐑𝐁𝐎𝐓 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 𝐔𝐍𝐌𝐔𝐓𝐄𝐃", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **Volume set To** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆**")

@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await query.answer("❌ 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 𝐈𝐒 𝐂𝐔𝐑𝐑𝐄𝐍𝐓𝐋𝐘 𝐒𝐓𝐑𝐄𝐀𝐌𝐈𝐍𝐆", show_alert=True)
    elif queue == 1:
        await query.answer("» There's no more Music in Queue to Skip, Userbot leaving Video Chat.", show_alert=True)
    elif queue == 2:
        await query.answer("🗑️ Clearing the **Queues**\n\n» **Userbot** leaving Video Chat.", show_alert=True)
    else:
        await query.answer("goes to the next track, proccessing...")
        await query.message.delete()
        buttons = stream_markup(user_id)
        requester = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = query.from_user.id
        gcname = query.message.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await _.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"⏭ **𝐒𝐊𝐈𝐏𝐏𝐄𝐃 𝐓𝐎 𝐓𝐇𝐄 𝐍𝐄𝐗𝐓 𝐓𝐑𝐀𝐂𝐊.\n\n🗂 **𝐍𝐀𝐌𝐄:** [{queue[0]}]({queue[1]})\n💭 **𝐂𝐇𝐀𝐓:** `{chat_id}`\n🧸 **𝐑𝐄𝐐𝐔𝐄𝐒𝐓𝐄𝐃 𝐁𝐘:** {requester}",
        )
        remove_if_exists(image)
