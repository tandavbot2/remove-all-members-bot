from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize your bot (replace 'my_bot' with your actual bot token and API details)
app = Client("my_bot")

# Function to check permissions before performing actions
async def check_permissions(client, message: Message):
    chat = message.chat
    bot_id = (await client.get_me()).id  # Get bot's user ID
    bot_member = await client.get_chat_member(chat.id, bot_id)

    # Check if the bot has the ability to delete messages
    if bot_member.can_delete_messages:
        return True
    else:
        await message.reply("Bot doesn't have permission to delete messages.")
        return False

# Service handler that attempts to delete a message
@app.on_message(filters.command("delete", prefixes="/") & filters.me)
async def service(client: Client, message: Message):
    # Ensure the bot has permission to delete messages
    if await check_permissions(client, message):
        try:
            await message.delete()
        except Exception as e:
            await message.reply(f"Failed to delete message: {str(e)}")

# Main function for handling user messages and checking bot permissions
@app.on_message(filters.command("start", prefixes="/") & filters.private)
async def main(client: Client, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    bot_member = await client.get_chat_member(chat.id, (await client.get_me()).id)

    # Fetch user's chat member info
    user_member = await client.get_chat_member(chat.id, user_id)

    # Check if the bot can restrict members and delete messages
    if bot_member.can_restrict_members and bot_member.can_delete_messages:
        await message.reply("Bot has sufficient permissions to manage this chat.")
    else:
        await message.reply("Bot does not have enough rights to manage this chat.")

# Start the bot
app.run()
