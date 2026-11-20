import discord
from discord.ext import commands
import os
from collections import defaultdict
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# KATA JOROK
KATA_JOROK = ["anjing", "bangsat", "tolol", "goblok", "bego", "kontol", "memek", "kampret", "bajingan", "asu", "jancuk", "pepek", "babi", "monyet"]

peringatan = defaultdict(int)
spam_data = defaultdict(list)

@bot.event
async def on_ready():
    print(f"Bot CIOO JAGO sudah ONLINE! {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # === ANTI SPAM : 10x DALAM 5 DETIK = MUTE 5 MENIT ===
    user_id = message.author.id
    sekarang = time.time()
    spam_data[user_id].append(sekarang)
    spam_data[user_id] = [t for t in spam_data[user_id] if sekarang - t < 5]

    if len(spam_data[user_id]) >= 10:
        try:
            await message.channel.purge(limit=10, check=lambda m: m.author == message.author)
        except:
            pass
        try:
            await message.author.timeout(duration=300, reason="Spam 10x")
        except:
            pass
        spam_data[user_id] = []
        return

    # === ANTI KATA JOROK : 5x BARU BAN, BOT CUMAN JAGO BAE ===
    isi = message.content.lower()
    for kata in KATA_JOROK:
        if kata in isi:
            try:
                await message.delete()
            except:
                pass

            peringatan[user_id] += 1
            jumlah = peringatan[user_id]

            if jumlah == 3 or jumlah == 4:
                # Mute 5 menit, biar Carl Bot yang kasih paham
                try:
                    await message.author.timeout(duration=300, reason="Ngomong jorok")
                except:
                    pass
            elif jumlah >= 5:
                try:
                    await message.author.ban(reason="5x ngomong jorok")
                except:
                    pass
                peringatan[user_id] = 0
            return

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    await ctx.send("CIOO JAGO aktif! Mode jago bae!")

@bot.command()
async def reset(ctx, member: discord.Member):
    peringatan[member.id] = 0
    await ctx.send(f"Peringatan {member.mention} di-reset!")

@bot.command()
async def cek(ctx, member: discord.Member):
    jumlah = peringatan[member.id]
    await ctx.send(f"{member.mention} : {jumlah}/5")

bot.run(os.getenv("DISCORD_TOKEN"))
