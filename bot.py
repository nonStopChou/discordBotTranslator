import os

import discord
import random
from dotenv import load_dotenv

from googletrans import Translator



translator = Translator()

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
LANGS = os.getenv("TARGET_LANGUAGES")

targets = LANGS.split(",")
client = discord.Client()



@client.event
async def on_ready():

	for guild in client.guilds:
		if guild.name == GUILD:
			break

	# guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
	guild = discord.utils.get(client.guilds, name=GUILD)
	print(f'{client.user} has connected to Discord!' )
	print(f'{guild.name} (id: {guild.id})')
 

@client.event
async def on_message(message):
	if message.author == client.user:
		return 

	username = message.author.name.split("#")[0]
	orgText = message.content
	srcLang = translator.detect(orgText).lang
	tarLangs = [lang for lang in targets if lang != srcLang]

	response = f"{username} : {orgText}\n"
	print("tarLangs : " + " ".join(tarLangs))
	for lang in tarLangs:	
		print("lang : " + lang)
		if lang == 'zh-CN':
			translatedText = translator.translate(orgText, src=srcLang, dest='zh-tw').text
		else:
			translatedText = translator.translate(orgText, src=srcLang, dest=lang).text
		if lang == 'en':
			response += f'\nTranslated : {translatedText}'
		elif lang == "zh-tw" or lang == "zh-CN":
			response += f'\n翻譯 : {translatedText}'
		elif lang == "de":
			response += f'\nÜbersetzung : {translatedText}'
		

	await message.channel.send(response)


		
client.run(TOKEN)

# translated = translator.translate('Hello', src='en', dest='zh-Cn')
# print(translated.text)