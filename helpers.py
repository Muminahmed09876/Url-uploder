import math
from pyrogram.types import Message

def human_readable_size(size):
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}"

async def progress_bar(current, total, message: Message, filename):
    percent = f"{(current / total) * 100:.1f}"
    progress = f"[{'=' * int(float(percent)//5)}{' ' * (20 - int(float(percent)//5))}]"
    await message.edit(
        text=f"Uploading `{filename}`

{progress} {percent}%
{human_readable_size(current)} of {human_readable_size(total)}"
    )
