import discord
from discord.ext import commands
from random import choice

class Everyone(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('Logged in as: {} ({})'.format(self.bot.user, self.bot.user.id))

	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = self.bot.get_channel(592333158762938369)
		welcomeMsg = [
					f"Welcome to the server, {member.mention}.",
					f"I saw you coming, {member.mention}!",
					f"Run!!! {member.mention} is here!",
					f"I've been expecting you, {member.mention}!",
					f"{member.mention} has finally arrived. Time for work.",
					f"{member.mention} has joined the server!",
					f"{member.mention} has something to say.",
					]
		msg = discord.Embed(description=choice(welcomeMsg), color=discord.Color.green())
		await channel.send("", embed=msg)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = self.bot.get_channel(592333158762938369)
		leaveMsg = [
					f"{member.mention} has ran away!",
					f"{member.mention} has escaped!",
					f"{member.mention} doesn't like me.",
					f"{member.mention} has left because he ain't cool.",
					f"{member.mention} left the server to find his toys.",
					f"{member.mention} needs to calm down and stop leaving.",
				   ]
		msg = discord.Embed(description=choice(leaveMsg), color=discord.Color.red())
		await channel.send("", embed=msg)

	# Commands
	@commands.command(name="ping", help="ping", brief="Checks bot reply speed.")
	async def ping(self, ctx):
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

	@commands.command(name="stats", help="stats", brief="Give stats about this server.")
	async def stats(self, ctx):
		online = 0
		idle = 0
		offline = 0

		server = self.bot.get_guild(592115872848412712)
		for m in server.members:
			if str(m.status) == "online":
				online += 1
			elif str(m.status) == "offline":
				offline += 1
			else:
				idle += 1
		await ctx.send(f"`Users: {server.member_count}\n  Online: {online}\n  Idle: {idle}\n  Offline: {offline}`")

	@commands.command(name='8ball', help="8ball [QUESTION]", brief="Answers a yes/no question.")
	async def _8ball(self, ctx, *, question=""):
		if question is not "":
			response = [
						"No U",
						"Maybe",
						"Yasss",
						"Hmmm",
						"Yes?",
						"NOO",
						"Definitely",
						"Obviously yes",
						"OK",
						"IDK",
						"Let me think...",
						"Very Likely",
						"Not Likely",
						"Time Will Tell",
						"Huh?!?!",
						]
			await ctx.send(f"{choice(response)}")
		else:
			await ctx.send("What's your question?")



def setup(bot):
	bot.add_cog(Everyone(bot))
