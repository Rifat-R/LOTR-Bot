from tracemalloc import start
from disnake.ext import commands
import disnake
import requests

def parse_wiki(text, physical_attribiute):
    first_variation = text.find(f"{physical_attribiute} =")
    second_variation = text.find(f"|{physical_attribiute}")
    third_variation = text.find(f"| {physical_attribiute}")
    variations = [first_variation,second_variation,third_variation]
    for i in variations:
        if i != -1:
            starting_index = i
            break

    final_index = starting_index + 500
    final_index = text[starting_index:final_index].find(",,") + starting_index
    attribiute_line = text[starting_index:final_index]
    if attribiute_line[0] == "|":
        attribiute_line = attribiute_line[1:] #If the text is not formatted properly then the start of the line will start with a | in which we must remove.
    final_first_variation = attribiute_line.find("<ref")
    final_second_variation = attribiute_line.find("|") #Some will not end with \n but rather with |.
    original_final_second_variation = final_second_variation
    if final_second_variation >= 20: #Removes possibility if the attribiute starts with |.
        final_second_variation = -1
    else:
        final_second_variation = original_final_second_variation
        
    variations = [final_first_variation,final_second_variation]
    formatted_final_index = -1
    for i in variations:
        if i != -1:
            formatted_final_index = i
    formatted_index = attribiute_line.find("=") + 2
    parsed_text = attribiute_line[formatted_index-1:formatted_final_index]
    parsed_text = parsed_text.replace("[[","").replace("]]","").replace("{{","").replace("}}","")
    if len(parsed_text) <= 2:
        parsed_text = "N/A"
    return parsed_text

class Lotr_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def lotr(self, ctx, *, lotr_query):
        if lotr_query.find(" ") != -1:
            lotr_query = (lotr_query.lower()).title()
            
        capitalized_lotr_query = lotr_query.capitalize()
        url = f"https://lotr.fandom.com/api.php?action=query&prop=revisions&titles={lotr_query}&rvprop=content&format=json"
        response = requests.get(url)
        lotr_json = response.json()
        data = lotr_json["query"]["pages"]
        data = data[next(iter(data))]["revisions"][0]["*"].replace("\n","\n,,")
        race = parse_wiki(data,"race")
        hair = parse_wiki(data,"hair")
        eyes = parse_wiki(data,"eyes")
        embed = disnake.Embed(title = f"{capitalized_lotr_query}",color=0xfffff)
        embed.add_field(name="Race", value=f"{race}", inline=False)
        embed.add_field(name="Hair", value=f"{hair}", inline=False)
        embed.add_field(name="Eyes", value=f"{eyes}", inline=False)
        await ctx.send(embed=embed)


        
        
    @lotr.error
    async def lotr_error(self,ctx,error:commands.CommandError):
        msg = f"Not found"
        await ctx.send(f"**{ctx.message.content[6:]}** not found.")




def setup(bot):
    bot.add_cog(Lotr_stats(bot))