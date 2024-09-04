import discord
from discord import app_commands
from discord.ext import commands
from modules.screen.screenshot import mssScreenshot
import io

def discordBot(token, run):
    bot = commands.Bot(command_prefix="!b", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is Ready!")
        try:
            synced = await bot.tree.sync()
            print("Synced commands")
        except Exception as e:
            print(e)
    
    @bot.tree.command(name = "ping", description = "check if the bot is online")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
    
    @bot.tree.command(name = "screenshot", description = "Send a screenshot of your screen")
    async def screenshot(interaction: discord.Interaction):
        img = mssScreenshot()
        with io.BytesIO() as imageBinary:
            img.save(imageBinary, "PNG")
            imageBinary.seek(0)
            await interaction.response.send_message(file = discord.File(fp=imageBinary, filename="screenshot.png"))

    @bot.tree.command(name = "stop", description = "stop the macro")
    async def stop(interaction: discord.Interaction):
        if run.value == 3: 
            await interaction.response.send_mesasge("Macro is already stopped")
            return 
        run.value = 0
        await interaction.response.send_message("Stopping Macro")
        
    @bot.tree.command(name = "rejoin", description = "make the macro rejoin the game.")
    async def rejoin(interaction: discord.Interaction):
        run.value = 4
        await interaction.response.send_message("Macro is rejoining")

    @bot.tree.command(name = "rejoin", description = "make the macro rejoin the game.")
    async def rejoin(interaction: discord.Interaction):
        run.value = 4
        await interaction.response.send_message("Macro is rejoining")
        
    #start bot
    bot.run(token)
