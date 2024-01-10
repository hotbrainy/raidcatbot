#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

import tweepy 
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Twitter API keys
consumer_key = 'miqfeWSlpAZOUVopwede6HhuX'
consumer_secret = 'KEYb7fhxdZeyBeqKPHDIkKjnFuega5ainQTsJ7gzzLPNqDIOfN'
access_token = '935370572590088192-wWMvL0U3rX8fIfc2Z1qZcG5cfRkCKLb'
access_token_secret = '5uPY7gC3QkSgoAdQQlpBEwGxG9pziKQWVmFq32o8DeCCN'
bearer_token='AAAAAAAAAAAAAAAAAAAAAClUrwEAAAAAiQ%2BZ16WbFzD%2BJ2W1JPFzWCHtJ0Y%3DdMoC7TlupgzdNLljUMfalOvcQp8PBSl3YBuMT7snQgFuuKEK4Q'
client_secret='RBVtM0qXgHA3r7oWNwCJoyJbPPqihqy-1vL13aA9P_Z-5pxhNc'
client_id='TlBDLWFwNmxrUTVVNWtvLTlZbU06MTpjaQ'
app_id='28267561'
# Set up Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Store the access token directly in memory (for this simplified example)
access_tokens = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Website", callback_data="website"),
            InlineKeyboardButton("Twitter", callback_data="twitter"),
            InlineKeyboardButton("Button 3", callback_data="button_3")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.message.from_user
    username = user.username if user.username else "Anonymous"
    print("="*80)
    print(username)
    print("="*80)
    await update.message.reply_text(f"Hey {username}!\nWelcome to USD Cat Bot", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    user = query.from_user
    match query.data :
        case "website":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "twitter":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "button_3":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "like":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "retweeet":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "comment":
            return await query.edit_message_text(text=f"Selected option: {query.data}")
        case "bookmark":
            return await query.edit_message_text(text=f"Selected option: {query.data}")


async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Like", callback_data="like"),
            InlineKeyboardButton("Retweet", callback_data="retweet")
        ],
        [
            InlineKeyboardButton("Comment", callback_data="comment"),
            InlineKeyboardButton("Bookmark", callback_data="bookmark")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    args = context.args
    if len(args) != 5:
        await update.message.reply_text("Invalid number of arguments. Usage: /raid <link> X Y Z B")
        return
    
    tweet_link, target_likes, target_retweets, target_replies, target_bookmarks = args
    print (tweet_link)
    print (args)
    # Extract tweet ID from the link
    tweet_id = tweet_link.split('/')[-1].split('?')[0]
    print (tweet_id)
    try:
        tweet = api.get_status(tweet_id)
        achieved_likes = 6
        achieved_retweets = 10
        achieved_replies = 0
        achieved_bookmarks = 0
        
        # Generate response message
        response = f"Link: {tweet_link}\n"
        response += "Raid targets:\n"
        response += f"Likes: {achieved_likes}/{target_likes}\n"
        response += f"Retweets: {achieved_retweets}/{target_retweets}\n"
        response += f"Comments: {achieved_replies}/{target_replies}\n"
        response += f"Bookmarks: {achieved_bookmarks}/{target_bookmarks}\n"
        
        # Perform actions like liking, retweeting, replying, and bookmarking based on targets
        # For example:
        # api.create_favorite(tweet_id)
        # api.retweet(tweet_id)
        # api.update_status(f"@{tweet.user.screen_name} Your reply message", in_reply_to_status_id=tweet_id)
        # api.create_bookmark(tweet_id)

        await update.message.reply_text(response, reply_markup=reply_markup)
    except Exception as e:
        print(e)
        await update.message.reply_text(f"Error occurred: {e}")

 

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    
    oauth_verifier = update.message.text  # Assuming the user sends the OAuth verifier code
    print(oauth_verifier)
    auth.request_token['oauth_verifier'] = oauth_verifier
    access_token = auth.get_access_token(oauth_verifier)
    
    # Store access_token and associate it with the Telegram user in your dictionary or database
    user_id = update.message.from_user.id
    access_tokens[user_id] = access_token
    
    await update.message.reply_text("Twitter account linked successfully!")
    return 0

async def link_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Generate OAuth URL as described earlier
    # redirect_url = ...
    print(update.message.text)
    auth = tweepy.OAuth2UserHandler(
        client_id=client_id,
        redirect_uri="https://t.me/usdcatbot",
        scope=["Scope here", "Scope here"],
        # Client Secret is only necessary if using a confidential client
        client_secret=client_secret
    )
    auth.set_access_token(access_token, access_token_secret)
    redirect_url = auth.get_authorization_url()
    # Send the OAuth URL to the user via Telegram
    await update.message.reply_text(f"Click this link to link your Twitter account: {redirect_url}")
    return 0


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    response = "Help Commands:\n"
    response += "/start - start this bot\n"
    response += "/raid <link> X Y Z B - raid the link\n"
    response += "/link_twitter - link your twitter account to bot\n"
    await update.message.reply_text(response)


async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("invalid code")
    return 0

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    application = Application.builder().token("6847086506:AAFcQkBOb-bD7qqHIb6ZYLgP4cUyxTlJ_1U").persistence(persistence).build()
   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("raid", raid))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("link_twitter", link_twitter))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("link_twitter", link_twitter)],
        states={
            0: [
                MessageHandler(
                      filters.Regex("^[0-9]{7,7}$") & ~ filters.COMMAND, handle_callback
                )
            ]
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, error_callback)],
        name="my_conversation",
        persistent=True,
    )

    application.add_handler(conv_handler)
    # application.add_handler(CallbackQueryHandler(handle_callback))

    # application.add_handler(CallbackQueryHandler(list_button))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
