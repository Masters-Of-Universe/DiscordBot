import discord

def isAdmin(member):
	isAdmin = False
	for role in member.roles:
		if (str(role.name) == "@admin"):
			isAdmin = True
	return isAdmin
	