import os
from dotenv import load_dotenv
from prefect.blocks.notifications import DiscordWebhook,MicrosoftTeamsWebhook
from pydantic import SecretStr

## load the .env file:
load_dotenv()


## a webhook that sends the message via Discord
def send_discord_message(message:str):
    """
    Docstring for send_discord_message
    
    :param message: the message sent to the discord server 
    :type message: str
    """
    ## get the webhook
    webhook_url=os.getenv("DISCORD_URL")

    ## get the webhook id and token:
    webhook_id=SecretStr(webhook_url.split("/webhook/")[1].split[0])
    webhook_token=SecretStr(webhook_url.split("/")[-1])

    ## connect to the Discord
    discord=DiscordWebhook(
        webhook_id=SecretStr(webhook_id),
        webhook_token=SecretStr(webhook_token)
    )

    ## send the message
    discord.notify(message)

## send the Microsoft Teams message:
def send_teams_message(message:str):
    """
    Docstring for send_teams_message
    
    :param message: Description
    :type message: str
    """
    webhook_url=os.getenv("MICROSOFT_URL")

    ## connect to Microsoft Teams:
    microsoft=MicrosoftTeamsWebhook(
        url=SecretStr(webhook_url)
    )

    ## send the message:
    microsoft.notify(message)
