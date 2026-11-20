import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = 1572969170767716452  # Channel kamu #info-egg-spawn-sae
SOURCE_CHANNEL_ID = 1555090108942913586  # Channel SenZ #egg-spawns

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot {client.user} sudah ONLINE! Siap memantau Divine dan Eternal!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != SOURCE_CHANNEL_ID:
        return
    if not message.embeds:
        return

    embed = message.embeds[0]
    title = embed.title or ""

    # FILTER: HANYA DIVINE DAN ETERNAL SAJA!
    if "Divine Egg Spawned" not in title and "Eternal Egg Spawned" not in title:
        print(f"Lewati: {title}")
        return

    print(f"TELUR LANGKA DITEMUKAN! {title}")
    target = client.get_channel(TARGET_CHANNEL_ID)
    if not target:
        return

    desc = embed.description or ""
    
    # Tentukan warna dan judul sesuai jenis telur
    if "Divine" in title:
        warna = 0xFFD700
        judul = "‼️✨🥚 DIVINE EGG HAS SPAWNED! 🥚✨‼️"
        ping = "@everyone DIVINE MUNCUL!!"
    else:
        warna = 0xA020F0
        judul = "🔥🥚 ETERNAL EGG HAS SPAWNED! 🥚🔥"
        ping = "@everyone ETERNAL MUNCUL!!"

    new_embed = discord.Embed(
        title=judul,
        description=f"{desc}\n\n**BURUAN MASUK! SEBELUM KEDULUAN ORANG LAIN!**",
        color=warna
    )
    new_embed.add_field(name="🎮 JOIN GAME", value="[KLIK DI SINI UNTUK STEAL!](https://www.roblox.com/games/107778070777162/Steal-an-Egg)", inline=False)
    new_embed.set_footer(text="CIOO SPAWN NOTIF • Divine & Eternal Only • Dari SenZ V2")

    await target.send(content=ping, embed=new_embed)

client.run(TOKEN)
