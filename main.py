import discord
from discord.commands import slash_command
from discord.ext import commands
import os
import requests

token = os.environ['DISCORD_TOKEN']

bot = commands.Bot(intents=discord.Intents.all(),)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')

extensions = ['cogs.ping', 'cogs.avatar', 'cogs.background']

if __name__ == '__main__':
  for extension in extensions:
    bot.load_extension(extension)
    print(extension)

class ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(guild_ids=[1211812480385290311, 1043949659971915897],
          name='ping',
          description='return bot latency')
  async def ping(self, ctx: discord.ApplicationContext):
    await ctx.respond(f"pong! ({self.bot.latency*1000:.2f} ms)")

class background(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(guild_ids=[1211812480385290311, 1043949659971915897],
          name='background',
          description='remove background from an image')
  async def background(self, ctx, url: discord.Option(discord.SlashCommandOptionType.string)):
    def remove_background(image_url):
      try:
        api_key = "FrV8nfqT6KSJSLmXjeBn5tRr"
        api_url = "https://api.remove.bg/v1.0/removebg"
        response = requests.post(api_url, data={'image_url': image_url}, headers={'X-Api-Key': api_key})
        if response.status_code == 200:
          with open("output.png", "wb") as f:
            f.write(response.content)
          return "output.png", None
        else:
          return None, f"Failed to remove background. Status code: {response.status_code}"
      except requests.exceptions.RequestException as e:
        return None, f"Error removing background: {e}"

    output_image, error_message = remove_background(url)

    if output_image:
      await ctx.respond(file=discord.File(output_image))
    else:
      await ctx.respond(error_message)

class avatar(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(guild_ids=[1211812480385290311, 1043949659971915897],
          name='avatar',
          description='get avatar items of a user')
  async def avatar(self, ctx, id: discord.Option(discord.SlashCommandOptionType.string)):
    def fetch_avatar_url(user_id):
      try:
        url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false"
        response = requests.get(url)
        if response.status_code == 200:
          data = response.json()
          return data['data'][0]['imageUrl']
        else:
          return None
      except requests.exceptions.RequestException as e:
        print("Error fetching avatar URL:", e)
        return None


    def fetch_username(user_id):
      try:
        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
        if response.status_code == 200:
          user_data = response.json()
          return user_data.get('displayName')
        else:
          return None
      except requests.exceptions.RequestException as e:
        print("Error fetching username:", e)
        return None


    def fetch_description(user_id):
      try:
        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
        if response.status_code == 200:
          user_data = response.json()
          return user_data.get('description')
        else:
          return None
      except requests.exceptions.RequestException as e:
        print("Error fetching username:", e)
        return None


    def construct_item_url(asset_id):
      base_url = "https://www.roblox.com/catalog/"
      return f"{base_url}{asset_id}/"

    r = requests.get("https://avatar.roblox.com/v1/users/" + id +
             "/currently-wearing")
    if r.status_code == 200:
      # Parse the JSON response
      json_data = r.json()

      # Access the list of asset IDs
      asset_ids = json_data['assetIds']
      with open("file.txt", "w") as text_file:
        for asset_id in asset_ids:
          # Construct the URL for each item
          item_url = construct_item_url(asset_id)
          text_file.write(item_url + "\n")
    with open("file.txt", "r") as f:
      avatarurl=fetch_avatar_url(id)
      username=fetch_username(id)
      desc=fetch_description(id)
      embed = discord.Embed(

bot.run(token)
