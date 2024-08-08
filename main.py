import logging
import asyncio
from telethon import TelegramClient, events

# Replace these with your own values
api_id = '21123447'
api_hash = 'a36950400e916896d127c7fd54c2d8d0'   
bot_token = '7408634138:AAG9U8awG_uuBf-bQfLvNqxbXL8W3TAfDNM'  # Your bot token
source_channel_usernames = ['@Shoppingo_Ajio_Shopsy_Deals', '@BestDealsInIND','@grocery_loot_deal','@Ajio_Myntra_Meesho_Deals_Offers']  # List of source channel usernames
destination_bot_username = '@INRDealsBot'  # The destination bot username

# Create the clients
personal_client = TelegramClient('personal', api_id, api_hash)
bot_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Change to DEBUG to see more details
logger = logging.getLogger(__name__)

@personal_client.on(events.NewMessage(chats=source_channel_usernames))
async def handler(event):
    # Get the message text
    message = event.message.message
    logger.info(f"Received message from source channel: {message}")
    
    # Forward the message to the destination bot using the personal client
    try:
        await personal_client.send_message(destination_bot_username, message)
        logger.info(f"Message forwarded to destination bot {destination_bot_username}")
    except Exception as e:
        logger.error(f"Failed to forward message to destination bot {destination_bot_username}: {e}")

async def main():
    logger.debug("Starting main function")
    
    # Start the personal client
    await personal_client.start()
    logger.debug("Personal client started")
    
    # If this is the first time running the script, it will ask for the phone number and login code
    if not await personal_client.is_user_authorized():
        logger.info("User not authorized, requesting login code...")
        await personal_client.send_code_request(phone=input("Enter your phone number: "))
        await personal_client.sign_in(phone=input("Enter your phone number: "), code=input("Enter the code: "))
    
    # Add a small delay to ensure setup is complete
    await asyncio.sleep(5)
    
    # Run both clients
    logger.info("Clients started and event handlers set up...")
    await asyncio.gather(
        personal_client.run_until_disconnected(),
        bot_client.run_until_disconnected()
    )

# Create a new event loop and run the main function
if __name__ == "__main__":
    logger.debug("Starting script")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    logger.debug("Script finished")
