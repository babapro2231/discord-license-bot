import discord
from discord.ext import commands
import os
import json

TOKEN = os.getenv("DISCORD_TOKEN")  # Render ortam değişkeni

OYUNLAR_DOSYA = "oyunlar.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# JSON dosyasını yükle
def oyunlari_yukle():
    if not os.path.exists(OYUNLAR_DOSYA):
        return []
    with open(OYUNLAR_DOSYA, "r") as f:
        return json.load(f)

# JSON dosyasını kaydet
def oyunlari_kaydet(oyunlar):
    with open(OYUNLAR_DOSYA, "w") as f:
        json.dump(oyunlar, f, indent=4)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.command()
async def oyun_ekle(ctx, oyun_id: str):
    oyunlar = oyunlari_yukle()
    if oyun_id in oyunlar:
        await ctx.send("⚠️ Bu oyun zaten whitelist'te.")
    else:
        oyunlar.append(oyun_id)
        oyunlari_kaydet(oyunlar)
        await ctx.send(f"✅ Oyun eklendi: {oyun_id}")

@bot.command()
async def oyun_sil(ctx, oyun_id: str):
    oyunlar = oyunlari_yukle()
    if oyun_id in oyunlar:
        oyunlar.remove(oyun_id)
        oyunlari_kaydet(oyunlar)
        await ctx.send(f"🗑️ Oyun silindi: {oyun_id}")
    else:
        await ctx.send("❌ Bu oyun whitelist'te yok.")

@bot.command()
async def oyunlar(ctx):
    oyunlar = oyunlari_yukle()
    if oyunlar:
        await ctx.send("📜 Whitelist'teki oyunlar:\n" + "\n".join(oyunlar))
    else:
        await ctx.send("⚠️ Whitelist'te hiç oyun yok.")

bot.run(TOKEN)