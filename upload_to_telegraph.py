import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

import os
import time
from config import Config
from helpers import progress
from telegraph import upload_file, Telegraph
from pyrogram import Client, filters


telegraphbot = Client("TELEGRAPH",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 parse_mode="markdown",
                 workers=100)


@telegraphbot.on_message(filters.command('start') & filters.incoming)
async def start_handlers(c, m):
    await m.reply_text(
        "𝘏𝘦𝘭𝘭𝘰 𝘜𝘴𝘦𝘳, I'm 𝐓𝐇𝐄 𝐒𝐈𝐍𝐋𝐎𝐀𝐃𝐄𝐑 ⸸ ✙\n\n"
        "✙ 𝙄 𝘼𝙢 𝘼 Telegraph.ph 𝙐𝙥𝙡𝙤𝙖𝙙𝙚𝙧.\n\n"
        "✙ 𝙄 𝘾𝙖𝙣 𝙐𝙥𝙡𝙤𝙖𝙙 𝙋𝙝𝙤𝙩𝙤𝙨 𝙏𝙤 𝙏𝙚𝙡𝙚𝙜𝙧𝙖.𝙥𝙝 𝘼𝙣𝙙 𝙂𝙞𝙫𝙚 𝙔𝙤𝙪 𝙏𝙝𝙚 𝙇𝙞𝙣𝙠 ✙\n"
        "✙ 𝗜 𝗖𝗮𝗻 𝗖𝗿𝗲𝗮𝘁𝗲 𝗔 𝗜𝗻𝘀𝘁𝗮𝗻𝘁 𝗩𝗶𝗲𝘄 𝗟𝗶𝗻𝗸 𝗙𝗼𝗿 𝗬𝗼𝘂𝗿 𝗧𝗲𝘅𝘁 ✙\n"
        "✙ 𝐈 𝐂𝐚𝐧 𝐂𝐫𝐞𝐚𝐭𝐞 𝐏𝐨𝐬𝐭 𝐈𝐧 Telegraph.ph 𝐈𝐟 𝐘𝐨𝐮 𝐒𝐞𝐧𝐝 𝐀𝐧𝐲 𝐓𝐞𝐱𝐭  ✙\n"
        "✙ ✙ 𝐂𝐡𝐞𝐜𝐤 𝐎𝐮𝐭 𝐎𝐮𝐫 𝐍𝐞𝐭𝐰𝐨𝐫𝐤 [𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦](https://t.me/The_Sinners_Empire)",
        disable_web_page_preview=True,
        quote=True
    )


@telegraphbot.on_message(filters.photo & filters.incoming)
async def telegraph(c, m):
    """Uploading to photo to telegra.ph 
       and sending photo link to user"""

    try:
        send_message = await m.reply_text(
            "Processing....⏳", 
            quote=True
        )
        location = f'./{m.from_user.id}{time.time()}/'
        start_time = time.time()
        file = await m.download(
            location,
            progress=progress,
            progress_args=(send_message, start_time)
        )
        try:
            media_upload = upload_file(file)
        except Exception as e:
            print('An Error occurred', e)
            await send_message.edit(f'**Error:**\n{e}')
        telegraph_link = f'https://telegra.ph{media_upload[0]}'
        await send_message.edit(
            telegraph_link
        )
    except:
        pass


@telegraphbot.on_message(filters.text & filters.incoming)
async def text_handler(c, m):
    """Creating instant view link
       by creating post in telegra.ph 
       and sending photo link to user"""

    try:
        short_name = "Ns Bots"
        new_user = Telegraph().create_account(short_name=short_name)
        auth_url = new_user["auth_url"]
        title = m.from_user.first_name
        content = m.text
        if '|' in m.text:
            content, title = m.text.split('|')
        content = content.replace("\n", "<br>")
        author_url = f'https://telegram.dog/{m.from_user.username}' if m.from_user.id else None

        try:
            response = Telegraph().create_page(
                title=title,
                html_content=content,
                author_name=str(m.from_user.first_name),
                author_url=author_url
            )
        except Exception as e:
            print(e)
        await m.reply_text("https://telegra.ph/{}".format(response["path"]))

    except:
        pass


telegraphbot.run()
