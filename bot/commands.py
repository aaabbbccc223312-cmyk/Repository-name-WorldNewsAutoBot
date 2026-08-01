from telegram import Update

from telegram.ext import ContextTypes

from config import ADMIN_ID

from database import (

    add_channel,

    remove_channel,

    pause_channel,

    resume_channel,

    get_channels,

    total_channels,

    total_users,

)


def is_admin(

    user_id,

):

    return user_id == ADMIN_ID


async def addchannel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    if len(

        context.args

    ) < 1:

        await update.message.reply_text(

            "Usage:\n/addchannel @channel"

        )

        return

    username = context.args[0]

    category = (

        context.args[1]

        if len(context.args) > 1

        else "world"

    )

    await add_channel(

        username,

        category,

    )

    await update.message.reply_text(

        f"✅ Added {username}"

    )
async def removechannel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    if len(

        context.args

    ) < 1:

        await update.message.reply_text(

            "Usage:\n/removechannel @channel"

        )

        return

    username = context.args[0]

    await remove_channel(

        username,

    )

    await update.message.reply_text(

        f"🗑 Removed {username}"

    )


async def pausechannel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    if len(

        context.args

    ) < 1:

        await update.message.reply_text(

            "Usage:\n/pausechannel @channel"

        )

        return

    username = context.args[0]

    await pause_channel(

        username,

    )

    await update.message.reply_text(

        f"⏸ Paused {username}"

    )
async def resumechannel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    if len(

        context.args

    ) < 1:

        await update.message.reply_text(

            "Usage:\n/resumechannel @channel"

        )

        return

    username = context.args[0]

    await resume_channel(

        username,

    )

    await update.message.reply_text(

        f"▶️ Resumed {username}"

    )


async def channels(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    rows = await get_channels()

    if not rows:

        await update.message.reply_text(

            "No channels found."

        )

        return

    text = "📢 Channels\n\n"

    for row in rows:

        text += (

            f"{row['username']}"

            f" ({row['category']})\n"

        )

    await update.message.reply_text(

        text

    )


async def stats(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    if not is_admin(

        update.effective_user.id,

    ):

        return

    users = await total_users()

    channels = await total_channels()

    await update.message.reply_text(

        f"👥 Users: {users}\n"

        f"📢 Channels: {channels}"

    )
