from asyncio.windows_events import NULL
import sys
import discord
import asyncio
import re
import time
import threading
from discord.message import Message
import youtube_dl
import os
import random
from discord import Intents
from youtube_dl import YoutubeDL
from discord.utils import get
from random import randint
import codecs

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwd = 'C:/Users/Huawei MateBook D 14/source/iyo_localrepo/iyo'
        self.ffmpeg_path = 'C:/Windows/System32/ffmpeg.exe'
        self.token='Nzc4MjM4MzAxODAyNzI1NDA4.X7PE5g.hSDuamRf_wKMo0tEavXRQ01DwM0'
        self.MuteRole = 585150174276354055
        self.channel = None
        self.AllTimers=list()
        self.AllTimersLock = threading.Lock()
        self.bg_task = self.loop.create_task(self.BackgroundCheckExpire())
        self.ERIDMembersList = list()
        self.CurrentTimerId=0
        self.URL_list = list()
        self.YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.KanekiURL = 'https://sun9-83.userapi.com/impg/GUG-spJd7eam8fljlKFgZyW0HVlqdCOa1hPz_g/4eduociL74g.jpg?size=820x1381&quality=96&sign=0cfad40967a49ae7335628519df4a154&type=album'
        self.PodpivasURL = 'https://sun9-39.userapi.com/impg/8nFT8PPZSly90j2XGz7CzoGoa2eDf-KKMJxj-w/14bnh6CilaE.jpg?size=846x709&quality=96&sign=d8aa6874af91f4d2ed2ccadfed3b49eb&type=album'

    def OnMessage(self,TheMessage:discord.Message) ->str:
        RequestedDuration = TheMessage.content
        MatchObject = re.match(r'^-!set\s*([\d]{1,2}[hms]){1}\s*([\d]{1,2}[hms]){0,1}\s*([\d]{1,2}[hms]){0,1}', RequestedDuration)
        DurationTime=0
        if(MatchObject):
            Items=MatchObject.groups()
            for Group in Items:
                if(Group):
                    GroupMatch = re.match(r'([\d]+)([hms])', Group)
                    if(GroupMatch):
                        TimeValue=int(GroupMatch.group(1))
                        if(TimeValue>60):TimeValue=60
                        TimeSign=GroupMatch.group(2)
                        if(TimeSign=='m'):
                            TimeValue=TimeValue*60
                        if(TimeSign=='h'):
                            if(TimeValue>12):TimeValue=12
                            TimeValue=TimeValue*3600
                        DurationTime+=TimeValue
            ExpireUnixTime = time.time() + DurationTime
            self.CurrentTimerId+=1
            TimerDiscriptor={'expire':ExpireUnixTime,'author':TheMessage.author.mention,'id':self.CurrentTimerId,'channel':TheMessage.channel}
            self.AllTimersLock.acquire()
            if(len(self.AllTimers)<10000):
                self.AllTimers.append(dict(TimerDiscriptor))
                self.AllTimers.sort(key = lambda TimerDiscriptorItem: TimerDiscriptorItem['expire'])
                self.AllTimersLock.release()
                return '{0} Timer [ID {1}] set to {2} MSK'.format(TheMessage.author.mention,
                                                            TimerDiscriptor['id'],
                                                            time.strftime('%H:%M:%S',time.gmtime(ExpireUnixTime + 10800)))
            else:
                return '{0} Bot overloaded!'.format(TheMessage.author.mention)
        else:
            return '{0} Wrong command format, see -!help command'.format(TheMessage.author.mention)

    async def GetHelpMessage(self):
        cmdlist = ['-!set[arg][arg][arg]', '-!play[link]', '-!next', '-!leave', '-!zxc', '-!roll[arg][arg]']
        filelist = ['set', 'play', 'next', 'leave', 'zxc', 'roll']
        emb=discord.Embed(title="Instruction", color=0x7300ff)
        for i in range(len(cmdlist)):
            with codecs.open ('{0}/help/{1}.txt'.format(self.pwd, filelist[i]), encoding='utf-8') as temp_file:
                data = temp_file.read()
                emb.add_field(name = cmdlist[i], value = data, inline = False)
        return emb

    async def dota(self, MembersList) -> str:
        MentionStr = '{0}\n{1}\n{2}\n{3}\n{4}\n'.format(MembersList[0].mention,
                                                           MembersList[1].mention,
                                                           MembersList[2].mention,
                                                           MembersList[3].mention,
                                                           MembersList[4].mention,)
        return MentionStr

    async def on_ready(self):
        AllChannels=[TheChannel.id for TheChannel in self.get_all_channels() if(type(TheChannel).__name__=='TextChannel')]
        ERIDGuildList = [TheGuild for TheGuild in self.guilds if TheGuild.id==358724016929767424]
        if(len(ERIDGuildList)>0):
            ERIDUsers=[308179526838648833, 299975192011341824, 289851818329243649, 299975899787427841, 299996064084393985]
            self.ERIDMembersList=[ERIDGuildList[0].get_member(UserId) for UserId in ERIDUsers]
        print('Logged in as:')
        print('Name: ',self.user.name)
        print('ID: ',self.user.id)
        print('|--------------------------------|')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="с детьми в подвале"))

    async def phonk(self, message):
        await message.author.voice.channel.connect(reconnect=True)
        voice = discord.utils.get(self.voice_clients, guild=message.guild)
        path ="{0}/phonk".format(self.pwd)
        filelist = []
        for root, dirs, files in os.walk(path):
           for file in files:
               filelist.append(os.path.join(root,file))
        random.shuffle(filelist)
        i = 0
        while i < len(filelist):
            if(voice.is_connected()):
                voice.play(discord.FFmpegPCMAudio(executable = self.ffmpeg_path, source = filelist[i]))
            i+=1
            while voice.is_playing():
                await asyncio.sleep(1)
        await voice.disconnect()
      
    async def queue(self, message):
        MatchObject = re.search(r'https://www.youtube.com/\S+', message.content)
        if (MatchObject):
            pass
        else:
            await message.channel.send('ERROR: the message does not contain a link')
            return
        await message.add_reaction("🎵")
        arg = MatchObject.group(0)
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(arg, download=False)
        URL = info['formats'][0]['url']
        self.URL_list.append(URL)

    async def play(self, message):
        await self.queue(message)
        try:
            await message.author.voice.channel.connect(reconnect=True)
            voice = discord.utils.get(self.voice_clients, guild=message.guild)
        except:
            pass
        if(len(self.URL_list) > 1):
            return
        length = len(self.URL_list)
        while length > 0:
            try:
                voice.play(discord.FFmpegPCMAudio(executable = self.ffmpeg_path, source = self.URL_list[0], **self.FFMPEG_OPTIONS))
            except:
                pass
            while voice.is_playing():
                await asyncio.sleep(1)
            try:
                del self.URL_list[0]
            except:
                pass
            length = len(self.URL_list)
        await asyncio.sleep(5)
        await voice.disconnect()

    async def leave(self, message):
        voice = discord.utils.get(self.voice_clients, guild=message.guild)
        try:
            await voice.stop()
        except:
            pass
        await voice.disconnect()

    async def next(self, message):
        voice = discord.utils.get(self.voice_clients, guild=message.guild)
        try:
            await voice.stop()
            await asyncio.sleep(1)
        except:
            pass
        try:
             await voice.resume()
        except:
            pass

    async def dices(self, message) ->str:
        size = 9
        sides = 6
        total = 0
        i = 1
        current = 0
        color=0x7300ff
        cubes_matrix = []
        MatchObject = re.findall(r'roll\s?(\d+)?\s?(\[\d+\])?', message.content)
        if (len(MatchObject[0][0]) > 0) or (len(MatchObject[0][1]) > 0):
            if (len(MatchObject[0][0]) > 0):
                if(int(MatchObject[0][0]) != 0) and (int(MatchObject[0][0]) <= 20):
                    size = int(MatchObject[0][0])*3
            if (len(MatchObject[0][1]) > 0):
                CurrentMatchObject = re.findall(r'\d+', MatchObject[0][1])
                if (int(CurrentMatchObject[0]) != 0) and (int(CurrentMatchObject[0]) <= 100):
                    sides = int(CurrentMatchObject[0])
        while i < size:
            cubes_matrix.append('[')
            current = (randint(1, sides))
            cubes_matrix.append(str(current))
            cubes_matrix.append('] ')
            total += current
            i+=3
        string = ''.join(cubes_matrix)
        Dices = []
        for j in range(int(size/3)):
            Dices.append('🎲')
        Dices_string = ''.join(Dices)
        if (size == 9) and (sides == 6):
            if (total >= 17):
                color = 0xDC143C
            elif (total <= 4):
                color = 0x00FF00
        emb=discord.Embed(title=" ", color=color)
        emb.add_field(name = 'Dices:', value = string, inline = False)
        emb.add_field(name = 'Total: {}'.format(total), value = Dices_string, inline = True)
        if ((total == 17) or (total == 18)) and (size == 9) and (sides == 6):
            try:
                emb.set_image(url = self.KanekiURL)
            except:
                print('image not found')
        if ((total == 3) or (total == 4)) and (size == 9) and (sides == 6):
            try:
                emb.set_image(url = self.PodpivasURL)
            except:
                print('image not found')
        return emb

    def count_lines(self, addres):
        count = 0
        with open(addres, 'r') as file:
            for line in file:
                count += 1
        return count

    def numerate(self, addres): 
        strings = list()
        with open(addres, 'r', encoding='utf-8') as file:
          for line in file:
               strings.append(line.strip())
        with open(addres, 'w', encoding='utf-8') as file:
            counter = 1
            for line in strings:
                print('{0} :: {1}'.format(counter, line), file = file)
                counter += 1

    async def create_character(self, message):
        MatchObject = re.findall(r'[a-z]+', message.content)
        emb=discord.Embed(title=" ", color=0x7300ff)
        flag = False
        with open('{0}/characters/{1}/test.txt'.format(self.pwd ,MatchObject[1]), 'r') as file:
            for line in file:
              if(line.strip() == 'false'):
                flag = True
        for j in range(int(6)):
            files = ['0_char', '1_stats', '2_perks', '3_adv', '4_disadv', '5_inventory']
            modules = ['Character', 'Stats', 'Perks', 'Advantages', 'Disdvantages', 'Inventory']
            with codecs.open ('{0}/characters/{1}/{2}.txt'.format(self.pwd, MatchObject[1], files[j]), encoding='utf-8') as temp_file:
                if(flag == True and (j in [2, 5])):
                    self.numerate('{0}/characters/{1}/{2}.txt'.format(self.pwd, MatchObject[1], files[j]))
                data = temp_file.read()
                emb.add_field(name = '{0}'.format(modules[j]), value = data, inline = False)
        if (flag == True):
            with open('{0}/characters/{1}/test.txt'.format(self.pwd, MatchObject[1]), 'w') as file:
                print('true', file = file)
            flag = False
        return emb

    async def add_field(self, message):
        MatchObject = re.findall(r'(\[\D+\])(\{\D+\})', message.content)
        target = re.findall(r'[^\[\]]+',MatchObject[0][0])
        argument = re.search(r'[^\{\}]+',MatchObject[0][1])
        character_name = target[0]
        character_category = target[1]
        character_content = argument[0]
        if(character_category == 'perk'):
            character_category = '2_perks'
        elif(character_category == 'inv'):
            character_category = '5_inventory'
        else:
            await message.channel.send('{} Wrong category!'.format(message.author.mention))
            return
        path = '{0}/characters/{1}/{2}.txt'.format(self.pwd, character_name,character_category)
        count = self.count_lines(path)
        strings = list()
        with open(path, 'r', encoding = 'utf-8') as file:
          for line in file:
               strings.append(line.strip())
        strings.append('{} :: {}'.format(count + 1, character_content))
        with open(path, 'w', encoding = 'utf-8') as file:
            for line in strings:
                file.write(line)
                file.write('\n')

    async def on_message(self, message):
        if(message.author.id == self.user.id):
            return
        try:
            if(message.author.top_role.id == self.MuteRole):
                await message.delete()
                await message.channel.send('{} Никто вас не слышит.'.format(message.author.mention))
        except:
             await message.channel.send('ERROR')
             return
        if(message.content.startswith('-!set')):            
            await message.channel.send(self.OnMessage(message))
        else:
            if(message.content.startswith('-!help')):
                await message.channel.send(embed = await self.GetHelpMessage())
            else:
                if(message.content.startswith('-!dota')):
                    if(message.author.guild.id == 358724016929767424):
                        await message.channel.send(self.dota(self.ERIDMembersList))
                    else:
                        await message.channel.send('ERROR')
                else:
                    if(message.content.startswith('-!zxc')):
                        if(message.author.voice):
                            try:
                                await self.phonk(message)
                            except:
                                await message.channel.send('{} ERROR: Allready connected.'.format(message.author.mention))
                        else:
                            await message.channel.send('{} ERROR: You are not in channel.'.format(message.author.mention))
                    else:
                        if(message.content.startswith('-!play')):
                            if(message.author.voice):
                                try:
                                    await self.play(message)
                                except:
                                    pass
                            else:
                                await message.channel.send('{} ERROR: You are not in channel.'.format(message.author.mention))
                        else:
                            if(message.content.startswith('-!leave')):
                                try:
                                    await self.leave(message)
                                    await message.add_reaction("👋")
                                except:
                                    pass
                            else:
                                if(message.content.startswith('-!next')):
                                    try:
                                        await self.next(message)
                                    except:
                                        pass
                                else:
                                    if(message.content.startswith('-!roll')):
                                        try:
                                            await message.channel.send('{}'.format(message.author.mention), embed = await self.dices(message))
                                        except:
                                            await message.channel.send('{}wrong format, try: -!roll[number of dices][number of sides]'.format(message.author.mention))
                                    else:
                                        if(message.content.startswith('-!char')):
                                            try:
                                                await message.channel.send('{}'.format(message.author.mention), embed = await self.create_character(message))
                                            except:
                                                await message.channel.send('{}wrong character name'.format(message.author.mention))
                                        else:
                                            if(message.content.startswith('-!add')):
                                                try:
                                                    await self.add_field(message)
                                                    await message.channel.send('{}Character was updated!'.format(message.author.mention), embed = await self.create_character(message))
                                                except:
                                                     await message.channel.send('{}Syntax error, try: -!add[name][category]{}'.format(message.author.mention, '{content}'))
                                            else:
                                                if(message.content.startswith('-!restart')):
                                                    try:
                                                        await self.leave(message)
                                                    except:
                                                        pass
                                                    sys.exit()
                                                else:
                                                     pass

    async def BackgroundCheckExpire(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                Message=None
                self.AllTimersLock.acquire()
                if(len(self.AllTimers)>0):
                    CurrentUnixTime = time.time()
                    TimerDescriptor=self.AllTimers[0]
                    if(TimerDescriptor['expire']<=CurrentUnixTime):
                        self.AllTimers.pop(0)
                        Message='{0} Timer [ID {1}] is up at {2} MSK'.format(TimerDescriptor['author'],
                                                                       TimerDescriptor['id'],
                                                                       time.strftime('%H:%M:%S',time.gmtime(CurrentUnixTime + 10800)))
                self.AllTimersLock.release()
                if(Message):
                    await TimerDescriptor['channel'].send(Message)
                await asyncio.sleep(0.1)
            except Exception as SomeError:
                print(str(SomeError))

intents = discord.Intents.default()
intents.members = True
client = MyClient(intents=intents)
client.run(client.token)
#test