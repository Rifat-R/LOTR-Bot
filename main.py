import disnake
from disnake.ext import commands

intents = disnake.Intents.default() # Enable all intents except for members and presences
intents.members = True  # Subscribe to the privileged members intent.
client = commands.Bot(command_prefix = '.', intents=intents)

with open("api_key.txt","r") as f:
    api_key_list = []
    for i in f.readlines():
        api_key_list.append(i.strip())
    API_KEY = api_key_list[0]

cogs_load = (
	"listeners.py",
	"lotr_stats.py"
	)


for file in cogs_load:
	client.load_extension(f"cogs.{file[:-3]}")
	print(f"Loaded up file : cogs.{file}")	                                                                                                                                   


client.run(API_KEY)
