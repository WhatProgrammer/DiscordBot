import discord
from discord.ext import commands
from datetime import date

class Admin(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.modLog = bot.get_channel(593902073062359153)

	# Function
	async def is_mod(ctx):
		if "Staff" in [y.name for y in ctx.message.author.roles]:
			return True
		else:
			return False

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		await bot.change_presence(status=discord.Status.idle, activity=discord.Game("with you"))

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send("This command ain't for you, my guy!")

	# Commands
	@commands.command(name="ban", help="ban [MEMBER] [REASON]", brief="For banning members.")
	@commands.check(is_mod)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason)
		msg = discord.Embed(title=f"Ban")
		msg.add_field(name="User:", value=f"⠀{member}", inline=False)
		msg.add_field(name="Moderator:", value=f"⠀{ctx.message.author}", inline=False)
		msg.add_field(name="Reason:", value=f"⠀{reason}", inline=False)
		msg.add_field(name="Date:", value="⠀" + today.strftime("%m/%d/%y"), inline=False)
		await self.bot.get_channel(593902073062359153).send("", embed=msg)

	@ban.error
	async def ban_error(aelf, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify who you want to ban!")

	@commands.command(name="unban", help="unban [MEMBER] [REASON]", brief="Unban a member.")
	@commands.check(is_mod)
	async def unban(self, ctx, *, member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')

		for ban_entry in banned_users:
			user = ban_entry.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await self.kbuMsg("unban", member, ctx.message.author, reason)
				return

	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify who you want to unban!")

	@commands.command(name="kick", help="kick [MEMBER] [REASON]", brief="Kicks a member out of the server.")
	@commands.check(is_mod)
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		await member.kick(reason=reason)
		await self.kbuMsg("Kick", member, ctx.message.author, reason)

	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please specify who you want to kick!")

	@commands.command(name="clear", help="clear [MSG AMT = ALL]", brief="Deletes a certain amount of messages in a channel.")
	@commands.check(is_mod)
	async def clear(self, ctx, amount=10000000):
		await ctx.channel.purge(limit=amount + 1)

	@commands.command(name="logout", help="logout", brief="For shutting down the bot.")
	@commands.check(is_mod)
	async def logout(self, ctx):
		await ctx.send("Logged Out!")
		await self.bot.close()


	# Functions
	async def kbuMsg(self, type, user, mod, reason):
		today = date.today()
		msg = discord.Embed(title=type)
		msg.add_field(name="User:", value=f"⠀{user}", inline=False)
		msg.add_field(name="Moderator:", value=f"⠀{mod}", inline=False)
		msg.add_field(name="Reason:", value=f"⠀{reason}", inline=False)
		msg.add_field(name="Date:", value="⠀" + today.strftime("%m/%d/%y"), inline=False)
		await self.bot.get_channel(593902073062359153).send("", embed=msg)



def setup(bot):
	bot.add_cog(Admin(bot))
