import os

from pyrogram import Client, filters


BOT_ID = int(os.getenv('BOT_ID'))


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

app = Client('redirecter', api_id=api_id, api_hash=api_hash)


@app.on_message(filters.chat(BOT_ID) & filters.command('redirect'))
def redirect(client, message):
    data = message.text
    return app.send_message(
        chat_id=BOT_ID,
        text=data.replace('/redirect', '/send_deadlines')
    )


app.run()
