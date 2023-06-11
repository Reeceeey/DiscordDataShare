import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=None, intents=intents)

guilds_and_channels = [

    {"guild_id": 857870123728633927, "channel_id": 1095351766452813964},  # PantherX - #police-station
    {"guild_id": 404106811252408320, "channel_id": 816029607039074334},  # Helium - #report-scammers
    {"guild_id": 716311300132831232, "channel_id": 861889689246367794},  # Sensecap - #report-scammers
    {"guild_id": 860251893803384893, "channel_id": 860303397033869313},  # Bobcat - #report-scammers
    {"guild_id": 860768230024151041, "channel_id": 1006824617060614195},  # COTX - #report-scammer
    {"guild_id": 945281182243913799, "channel_id": 945289743921446946},  # PROTON - #getting-started
    {"guild_id": 911140846034898974, "channel_id": 1018227465400893540},  # Aitek - #scammers
    {"guild_id": 837312565956575302, "channel_id": 863941516060786709},  # Dragino - #report-scammers
    {"guild_id": 948759488230481970, "channel_id": 948811256872194068},  # Dunsun - #general
    {"guild_id": 847446196994048001, "channel_id": 915841835589578803},  # Heltec #know-and-report-scammers
    {"guild_id": 886964183495741462, "channel_id": 978289794843033700},  # Miner Support #scammer-report

    {"guild_id": 861971204143579166, "channel_id": 863122774821699584},  # LongAP - #report-scammers
    {"guild_id": 920883777138458755, "channel_id": 999525830931775580},  # Milesight - #report-scammers
    {"guild_id": 861996402569117727, "channel_id": 861996402569117727},  # Nebra - #scammers
    {"guild_id": 836238477057720350, "channel_id": 1017073846756577300},  # Pisces - #scammer-report
    {"guild_id": 859018795262410782, "channel_id": 899683146075881544},  # SyncroB.it - #general
    {"guild_id": 869890064182837258, "channel_id": 869890064287686763},  # RISINGHF #report-scammers
    {"guild_id": 886964183495741462, "channel_id": 978289794843033700},  # Miner Support #scammer-report
]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    if message.guild.id == 'CHANNEL_ID':  # Channel to listen to message.content
        if message.content.startswith('w!hb') or message.content.startswith('w!b'):
            parts = message.content.split(' ')
            if len(parts) >= 4:
                command = parts[0]
                banned_userid = parts[1]
                reason = ' '.join(parts[2:])

                if reason.startswith('?r'):
                    reason = reason[2:].strip()

                if "scammer" in reason.lower():
                    for guild_channel in guilds_and_channels:
                        guild = bot.get_guild(guild_channel['guild_id'])
                        if guild:
                            channel = await guild.fetch_channel(guild_channel['channel_id'])
                            if channel:
                                username = message.author.name
                                userid = message.author.id
                                server_name = message.guild.name

                                user_id = int(banned_userid)
                                creation_time = datetime.utcfromtimestamp(((user_id >> 22) + 1420070400000) / 1000)
                                account_age = datetime.utcnow() - creation_time

                                years = account_age.days // 365
                                months = (account_age.days % 365) // 30
                                days = (account_age.days % 365) % 30
                                hours, remainder = divmod(account_age.seconds, 3600)
                                minutes, seconds = divmod(remainder, 60)

                                user = await bot.fetch_user(user_id)
                                if user:
                                    username = user.name
                                    avatar_url = user.avatar.url

                                embed = discord.Embed(title="Ban Received", color=discord.Color.green())
                                embed.add_field(name="Banned User", value=f"{username} [{banned_userid}]", inline=False)
                                embed.add_field(name="Account Age",
                                                value=f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
                                                inline=False)
                                embed.add_field(name="Reason", value=reason, inline=False)
                                embed.add_field(name="Ban Issuer", value=f"{message.author.name} [{userid}]", inline=False)
                                embed.add_field(name="Server Banned From", value=server_name, inline=False)
                                embed.add_field(name="Ban Command", value=message.content, inline=False)

                                if avatar_url:
                                    embed.set_thumbnail(url=avatar_url)

                                await channel.send(embed=embed)

        return


bot.run('DISCORD_BOT_TOKEN')
