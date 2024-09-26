'''
This code is by Yeuda via https://t.me/m100achuz

Dependencies:
- Pyrogram
Install: pip install Pyrogram
'''

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Fetch API credentials from environment variables
api_id = int(os.environ.get("API_ID", 12345))  # Replace 12345 with default or leave as-is for environment
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

# Ensure API credentials are provided
if not api_id or not api_hash or not bot_token:
    raise ValueError("Missing required environment variables: API_ID, API_HASH, or BOT_TOKEN")

# Initialize the Pyrogram client
app = Client("remove_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Messages
STARTED = 'Start removing users...'
FINISH = 'Done, {} users were removed from the group.'
ERROR = 'An error occurred: {}'
ADMIN_NEEDED = "I need to be an admin with the necessary permissions!"
PRIVATE = '''Hi, I'm a bot that helps remove all users from your group.

Add me to a group and ensure I have the appropriate admin permissions.
Then, send /kick in the group, and I'll begin my task.'''

# Command to remove users
@app.on_message(filters.group & filters.command("kick"))
def main(_, msg: Message):
    chat = msg.chat
    user = chat.get_member(msg.from_user.id)
    me = chat.get_member(app.get_me().id)
    
    # Print permissions for debugging
    print(f"User Permissions: {user.status}, Can Manage Chat: {getattr(user, 'can_manage_chat', 'N/A')}")
    print(f"Bot Permissions: {me.status}, Can Restrict Members: {me.can_restrict_members}, Can Delete Messages: {me.can_delete_messages}")
    
    if user.can_manage_chat and me.can_restrict_members and me.can_delete_messages:
        try:
            msg.reply(STARTED.format(chat.members_count))
            count_kicks = 0
            for member in chat.iter_members():
                if not member.can_manage_chat:
                    chat.kick_member(member.user.id)
                    count_kicks += 1
            msg.reply(FINISH.format(count_kicks))
        except Exception as e:
            msg.reply(ERROR.format(str(e)))
    else:
        msg.reply(ADMIN_NEEDED)


# Automatically delete service messages
@app.on_message(filters.group & filters.service, group=2)
def delete_service_messages(_, msg: Message):
    msg.delete()

# Handle private chat (when bot is messaged directly)
@app.on_message(filters.private)
def start_private_chat(_, msg: Message):
    msg.reply(PRIVATE, reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("Source Code", url="https://www.github.com/samadii/remove-all-members")
    ]]))

# Run the bot
if __name__ == "__main__":
    app.run()
