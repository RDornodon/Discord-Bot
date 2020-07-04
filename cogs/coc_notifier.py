from discord.ext import commands
import discord
from urllib.parse import urlparse
import re


class COCAnnouncer(commands.Cog, name='CoC Announcer'):
    def __init__(self, bot):
        self.bot = bot
        self.COC_CHANNEL = 0
        self.COC_ROLE = 0
    
    @commands.group(name='coc')
    async def coc(self, ctx):
        """CoC group command. Gives info about all commands within group"""
        embed = discord.Embed(
            title='CoC Commands',
            description='A list of CoC commands'
        )
        embed.add_field(name='t.coc invite', value='Invite everyone who is online with the CoC role to clash or coward.')
        embed.add_field(name='t.coc iubscribe', value='Subscribe to listen for invites. You\'re given the CoC role.')
        embed.add_field(name='t.coc insubscribe', value='Unsubscribe from invites. The CoC role is removed.')
        embed.add_field(name='t.coc afk', value='Temporarily removed the CoC role for a given amount of seconds. Default is one day.')
        embed.add_field(name='t.coc list', value='A list of everyone with the role. Doesn\'t tag them')
        
        await ctx.send(embed=embed)
        
    @coc.command(name='help')
    async def coc_help(self, ctx):
        """Help command, returns same thing as the group command"""
        
        embed = discord.Embed(
            title='CoC Commands',
            description='A list of CoC commands'
        )
        embed.add_field(name='t.coc invite', value='Invite everyone who is online with the CoC role to clash or coward.')
        embed.add_field(name='t.coc iubscribe', value='Subscribe to listen for invites. You\'re given the CoC role.')
        embed.add_field(name='t.coc insubscribe', value='Unsubscribe from invites. The CoC role is removed.')
        embed.add_field(name='t.coc afk', value='Temporarily removed the CoC role for a given amount of seconds. Default is one day.')
        embed.add_field(name='t.coc list', value='A list of everyone with the role. Doesn\'t tag them')
        
        await ctx.send(embed=embed)
    
    @coc.command(name='inv', aliases=['invite', 'i', 'start', 'play')
    async def invite(self, ctx: commands.Context, *, url: str = None):
        """invite all active COC Group members to compete"""
        if ctx.channel is None or ctx.channel.id != self.COC_CHANNEL:
            return
        await ctx.message.delete()
        if url is None:
            embed = discord.Embed(
                    title='COC Invite',
                    description=f'You\'d need to provide a valid URL for the invite.',
                    footer='Self destruct in 30s')
            await ctx.send(embed=embed, delete_after=30)
        res, parsed = check_url(url)
        if not res:
            embed = discord.Embed(
                    title='COC Invite',
                    description=parsed,
                    footer='Self destruct in 30s')
            await ctx.send(embed=embed, delete_after=30)
        else:
            mentions = []
            guild = ctx.guild
            role = guild.get_role(self.COC_ROLE)
            for user in role.members:
                if user.status in [discord.Status.online, discord.Status.idle]:
                    mentions.append(f'<@{user.id}>')
            if len(mentions) > 0:
                embed = discord.Embed(
                        title='COC Invite',
                        description=f'Join COC at {parsed}',
                        footer='Self destruct in 5 mins.')
                embed.add_field(name='Invitees', value=", ".join(mentions), inline=False)
                await ctx.send(embed=embed, delete_after=300)
                
    @coc.command(name='subscribe', aliases=['s', 'sub', 'r', 'register', 'reg'])
    async def subscribe(self, ctx):
        """Adds author to role"""
        await ctx.author.add_roles(ctx.guild.get_role(self.COC_ROLE))
       
    @coc.command(name='unsubscribe', aliases=['u', 'unsub', 'ur', 'unreg', 'unregister'])
    async def stop_notify(self, ctx):
        """Removes author from role"""
        await ctx.author.remove_roles(ctx.guild.get_role(self.COC_ROLE))
                          
    @coc.command(name='list', aliases=['subscribed']
    async def list(self, ctx):
        """Returns a list of people with the role"""
        await ctx.send(',\n'.join([user.display_name for user in ctx.guild.get_role(self.COC_ROLE).members]))

    @coc.command(name='afk')
    async def afk(self, ctx, time:int=86400):
        """Temporarily removes author for role for the given of seconds. Default is one day."""
        await ctx.author.remove_roles(ctx.guild.get_role(self.COC_ROLE))
        await asyncio.sleep(time)
        await ctx.author.add_roles(ctx.guild.get_role(self.COC_ROLE))

def check_url(text):
    urls = re.findall(r"(https?://[^\s]+)", text, flags=re.IGNORECASE)
    if len(urls) == 0:
        return False, 'Please provide a valid url'  # Not a URL
    elif len(urls) > 1:
        return False, 'Please provide a single url'  # devour multiple URLs
    elif urlparse(urls[0]).netloc != 'www.codingame.com':
        return False, 'Only CoC URLs are supported'  # Not a valid URL
    return True, urls[0]


def setup(bot):
    bot.add_cog(COCAnnouncer(bot))
