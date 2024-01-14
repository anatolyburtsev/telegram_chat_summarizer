import asyncio
import os
from datetime import datetime, timedelta

import click
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

client = TelegramClient("/tmp/fetch_data_session", api_id, api_hash)


@click.command()
@click.option("--chat_name", required=True, help="Chat name to download messages from.")
@click.option(
    "--days_back",
    default=7,
    type=click.IntRange(min=1),
    help="Number of days back to fetch messages. Must be a positive integer.",
)
@click.option(
    "--file_name",
    default="chat_backup.txt",
    help="File name for saving data. Default is chat_backup.txt",
)
def cli(chat_name, days_back, file_name):
    asyncio.run(download_chat(chat_name, days_back, file_name))


async def download_chat(chat_name, days_back, file_name):
    async with client:
        await client.start()
        chat = await client.get_entity(chat_name)
        today = datetime.now()
        start_date = today - timedelta(days=days_back)

        with open(file_name, "w") as file:
            async for message in client.iter_messages(chat):
                message_date = message.date.replace(tzinfo=None)
                if start_date > message_date:
                    break
                file.write(
                    f"{message_date:%Y-%m-%d %H:%M:%S} {message.sender.first_name} {message.sender.last_name}: "
                    f"{message.text}\n"
                )
        print(f"Messages fetched and saved to {file_name}")


if __name__ == "__main__":
    cli()
