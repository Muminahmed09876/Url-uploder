import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers import progress_bar

API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

bot = Client("url_uploader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_thumbs = {}

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply(
        "হ্যালো! আমি URL থেকে ফাইল আপলোড করতে পারি।

"
        "ব্যবহার:
"
        "`/upload https://example.com/file.mp4`

"
        "**Thumbnail Commands**
"
        "`/set_thumb` (Send image)
"
        "`/view_thumb`
"
        "`/del_thumb`"
    )

@bot.on_message(filters.command("set_thumb") & filters.private)
async def set_thumb(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("দয়া করে একটি ছবির রিপ্লাই দিন।")
    
    path = f"thumb_{message.from_user.id}.jpg"
    await message.reply_to_message.download(file_name=path)
    user_thumbs[message.from_user.id] = path
    await message.reply("Thumbnail সেট হয়েছে!")

@bot.on_message(filters.command("view_thumb") & filters.private)
async def view_thumb(client, message):
    path = user_thumbs.get(message.from_user.id)
    if path and os.path.exists(path):
        await message.reply_photo(photo=path)
    else:
        await message.reply("কোনো থাম্বনেইল পাওয়া যায়নি।")

@bot.on_message(filters.command("del_thumb") & filters.private)
async def del_thumb(client, message):
    path = user_thumbs.get(message.from_user.id)
    if path and os.path.exists(path):
        os.remove(path)
        user_thumbs.pop(message.from_user.id)
        await message.reply("Thumbnail মুছে ফেলা হয়েছে।")
    else:
        await message.reply("কোনো থাম্বনেইল সেট ছিল না।")

@bot.on_message(filters.command("upload") & filters.private)
async def upload_file(client, message):
    if len(message.command) < 2:
        return await message.reply("দয়া করে একটি লিংক দিন।
উদাহরণ: `/upload https://example.com/file.mp4`")

    url = message.command[1]
    msg = await message.reply("ডাউনলোড শুরু হয়েছে...")

    try:
        filename = url.split("/")[-1].split("?")[0]
        r = requests.get(url, stream=True)
        total = int(r.headers.get("content-length", 0))

        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    await progress_bar(downloaded, total, msg, filename)

        thumb = user_thumbs.get(message.from_user.id)
        await client.send_document(
            chat_id=message.chat.id,
            document=filename,
            thumb=thumb if thumb and os.path.exists(thumb) else None,
            caption=f"**Filename:** `{filename}`
**Size:** {total / (1024*1024):.2f} MB"
        )
        await msg.edit("আপলোড সম্পন্ন হয়েছে!")

        os.remove(filename)

    except Exception as e:
        await msg.edit(f"ত্রুটি হয়েছে: `{str(e)}`")

bot.run()
