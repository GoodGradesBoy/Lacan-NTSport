'''Coming Soon!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import discord
from discord.utils import get
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    def check(self, author, channel):
        def inner_check(message):
            return message.author == author and message.channel.id == message.author.id
        return inner_check
    async def wait_for_msg(self, ctx):
        try:
            client=self.client
            purchaser = await client.fetch_user(ctx.author.id)
            msg = await self.client.wait_for('message', check=self.check(ctx.author, ctx.author.id), timeout=30)
            return True, msg
        except TimeoutError:
            embed = Embed('Error!', 'You didn\'t answer in time!')
            return False, embed
    
    @commands.command()
    async def purchase(self, ctx):
        # Variables
        client = self.client
        print(ctx.author.id)
        purchaser = await client.fetch_user(ctx.author.id)
        guildid = str(ctx.guild.id)
        premtype = str('command')
        dbclient = DBClient()
        collection = dbclient.db.premium
        data = await dbclient.get_big_array(collection, 'premium')
        for x in data['premium']:
            if x['serverID'] == str(ctx.author.guild.id):
                embed = Embed('Error!', 'This server is already premium!', 'warning')
                return await embed.send(ctx)
        else:
          embed=Embed(':coin: Purchase Premium: Step 1 :coin:', f'You are about to purchase premium for the server **{str(ctx.guild.name)}** with the id `{str(ctx.guild.id)}` Is this the server you want to buy premium for?.\n\n*Please answer with `y` or `yes` if the statement is true for you and with `n` or `no` if you don\'t fulfill the statement.*')
          print(purchaser)
          await purchaser.send(embed=embed.default_embed())
          print('purchase embed sent')
          msg = await self.wait_for_msg(ctx)
          print('Checking for message...')
          if msg[0] == False:
              print('No message sent...')
              return msg[1].send(ctx)
          else:
            print('Success')
            msg = msg[1]
          list1 = ['y', 'Y', 'yes', 'Yes', 'ye', 'Ye', 'yeah', 'Yeah']
          cancel = ['cancel', 'Cancel', 'stop', 'Stop']
          print(msg.content)
          if msg.content in list1:
            pass
          if msg.content in cancel:
              print('cancel?')
              embed=Embed('Are you sure you want to cancel the purchasement?\n\n*Please answer with `y` or `yes` if the statement is true for you and with `n` or `no` if you don\'t fulfill the statement.*')
              await purchaser.send(embed=embed.default_embed())
              msg = await self.wait_for_msg(ctx)
              if msg[0] == False:
                return msg[1].send(ctx)
              else:
                msg = msg[1]
            
def setup(client):
    client.add_cog(Command(client))