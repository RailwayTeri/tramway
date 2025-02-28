import discord
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # Token načteme z Railway
URL = "https://tram.mobilnitabla.cz/api/positions"

intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Přihlášen jako {bot.user}")

@bot.command()
async def tramvaj(ctx, obeh: int):
    """Získá info o tramvaji podle oběhu."""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        for tram in data:
            if tram["obeh"] == obeh:
                lat, lon = tram["lat"], tram["lon"]
                await ctx.send(f"🚋 Tramvaj č. {obeh} je na souřadnicích: {lat}, {lon}")
                return
        await ctx.send("🚋 Tramvaj s tímto oběhem nebyla nalezena.")
    else:
        await ctx.send("❌ Nepodařilo se načíst data!")

bot.run(TOKEN)
