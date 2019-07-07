import discord
import os
from discord.ext import commands

token = str(os.environ.get('BOT_TOKEN'))
bot = commands.Bot(command_prefix='--', description='The boss!')
bot.remove_command('help')

@bot.command(name="load", help="--load [COG/COMMAND GROUP]", brief="Loading in Cogs/Command Groups.")
async def load(ctx, extension):
	bot.load_extension(f"cogs.{extension}")
	await ctx.send(f"Cog *{extension}* loaded!")

@bot.command(name="unload", help="--unload [COG/COMMAND GROUP]", brief="Unloading Cogs/Command Groups.")
async def unload(ctx, extension):
	bot.unload_extension(f"cogs.{extension}")
	await ctx.send(f"Cog *{extension}* unload!")

for filename in os.listdir("./cogs"):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def help(ctx, *com):
	try:
		if not com:
			help = discord.Embed(title='Help', description=f'Use `{ctx.prefix}help *COMMAND*` to find out more about it!', color=discord.Color.gold())
			for aCog in bot.cogs:
				cmdsList = bot.get_cog(aCog).get_commands()
				if aCog == "Admin":
					for y in bot.walk_commands():
						if "load" in y.name:
							cmdsList.append(y)
				comList = ""
				for aCom in cmdsList:
					comList += "{}{} - *{}*".format(ctx.prefix, aCom.name, aCom.brief) + "\n"
				help.add_field(name=aCog, value=comList[0:len(comList) - 1], inline=False)
				cmds_desc = ''
			await ctx.send('', embed=help)
		else:
			if len(com) > 1:
				help = discord.Embed(title='Error!', description='Please specify one command at a time please.', color=discord.Color.red())
				await ctx.send('', embed=help)
			else:
				found = False
				if "load" in com[0]:
					for y in bot.walk_commands():
						if com[0].replace(ctx.prefix, "") == y.name:
							found = True
							cmdName = y.name
							cmdHelp = y.help
							cmdBrief = y.brief
				else:
					for aCog in bot.cogs:
						for cmds in bot.get_cog(aCog).get_commands():
							if not cmds.hidden and cmds.name == com[0].replace(ctx.prefix, ""):
								found = True
								cmdName = cmds.name
								cmdHelp = cmds.help
								cmdBrief = cmds.brief

				if found:
					help = discord.Embed(title=f"{ctx.prefix}{cmdName}", color=discord.Color.gold())
					help.add_field(name="Description:", value=f"⠀{cmdBrief}", inline=False)
					help.add_field(name="Usuage:", value=f"⠀`{ctx.prefix}{cmdHelp}`", inline=False)
				else:
					help = discord.Embed(title='Error!', description=f'{com[0]} is not a command!"?', color=discord.Color.red())
				await ctx.send('', embed=help)
	except:
		pass


bot.run(token)
