import os

from dotenv import load_dotenv
from pyrogram import Client, filters


load_dotenv()

CHAT_ID = int(os.getenv('OWNER_CHAT_ID'))


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

app = Client('redirecter', api_id=api_id, api_hash=api_hash)


@app.on_message(filters.chat(CHAT_ID) & filters.command('redirect'))
def redirect(client, message):
    data = message.text
    message = data.replace('/redirect', '/send_deadlines')
    return app.send_message(chat_id=CHAT_ID, text=message)


app.run()
