from pytube import YouTube
import os
from pytube import Caption
from aiogram import Bot,Dispatcher,executor,types
import sqlite3
from config import API_TOKEN



#creating database
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
#create tables to database
cur.execute("""CREATE TABLE IF NOT EXISTS links(
    id INT,
    username TEXT,
    url TEXT
)""")
#saving database updates
con.commit()


#init telegram bot 
bot=Bot(API_TOKEN)
dp=Dispatcher(bot)
#creating start handler
@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    if message.chat.type=='private':
        await bot.send_message(message.from_user.id,text='Send me your youtube video link')
    else:
        await bot.send_message('Enter your gruop chat id, type : int',text='Send me your youtube video link')

@dp.message_handler()
async def image(message:types.Message):
    chat_id=message.from_user.id
    # creating conclusions to private chat: 
    if message.chat.type=='private':
        try:
            #geting url 
            if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
                link=message.text
                #add user_id to database
                cur.execute(f"INSERT INTO links VALUES(?,?,?)",(chat_id,message.from_user.username,link))
                
                con.commit()
                yt=YouTube(link)
                #reply in telegram chat
                await bot.send_message(message.from_user.id,text=f'Filesize: {str(yt.streams.first().filesize)[:-5]}\nChannel name: {yt.author}')

                await bot.send_message(message.from_user.id,text=f'Average download time: {float(yt.length)/float(2)} sec')
                if yt.streams.first().filesize<5000000:
                    #downloading file from url
                    for value in cur.execute("SELECT * FROM links"):
                        await bot.send_message(chat_id,text=value,disable_web_page_preview=True)
                    stream=yt.streams
                    yt.streams.get_highest_resolution().download()
                    
        
                    x=str(yt.streams.filter().first().default_filename).replace('3gpp','mp4')
                    video=open(f'{x}','rb')
        
     
                    #sending in telegram chat
                    await bot.send_video(message.from_user.id,video=video)
        
                    await bot.send_message(message.from_user.id,text=f'Completed ✅')
                    os.remove(str(yt.streams.filter().first().default_filename).replace('3gpp','mp4'))
                    
                else:
                    #replying error if file too big , for bots max=50 mb
                    await bot.send_photo(message.from_user.id,photo=photo)
                    await bot.send_message(message.from_user.id,text='File too big!!')
                    photo=open('docs.jpg','rb')

                    
            else:
                

                #replying error if message doesnt have url
                await bot.send_message(message.from_user.id,text=f"Please write correct link \nIf it doesn't work try restarting(/start) the bot then send the link")
        except:
            #trying again if pytube cant read streamfile

           if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
                link=message.text
                
                for value in cur.execute("SELECT * FROM links"):
                        await bot.send_message(chat_id,text=value,disable_web_page_preview=True)
                con.commit()
                yt=YouTube(link)
                await bot.send_message(message.from_user.id,text=f'Filesize: {str(yt.streams.first().filesize)[:-5]}\nChannel name: {yt.author}')

                await bot.send_message(message.from_user.id,text=f'Average download time: {float(yt.length)/float(2)} sec')
                if yt.streams.first().filesize<5000000:
                    
                    stream=yt.streams
                    yt.streams.get_highest_resolution().download()
                
                    

        
                    x=str(yt.streams.filter().first().default_filename).replace('3gpp','mp4')
                    video=open(f'{x}','rb')
        
     
        
                    await bot.send_video(message.from_user.id,video=video)
        
                    await bot.send_message(message.from_user.id,text=f'Completed ✅')
                    os.remove(str(yt.streams.filter().first().default_filename).replace('3gpp','mp4'))
                    
                else:
                    await bot.send_photo(message.from_user.id,photo=photo)
                    await bot.send_message(message.from_user.id,text='File too big!!')
                    photo=open('docs.jpg','rb')
                    


    else:
        #connecting with group chat

        try:
            chat_id='Enter your gruop chat id, type : int'
        

            if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
                link=message.text
                yt=YouTube(link)
        
                await bot.send_message(chat_id,text=f'Average download time: {float(yt.length)/float(2)} sec')
                if yt.streams.first().filesize<5000000:

                    yt.streams.get_highest_resolution().download()
                    x=str(yt.streams.filter().first().default_filename).replace('3gpp','mp4')
                    video=open(f'{x}','rb')
        
     
        
                    await bot.send_message(chat_id,text=f'Channel name: {yt.author}\nDescription: {yt.description}')
                    await bot.send_video(chat_id,video=video)
        
                    await bot.send_message(chat_id,text=f'Completed ✅')
                    os.remove(str(yt.streams.filter().first().default_filename).replace('3gpp','mp4'))
                else:
                    await bot.send_photo(message.from_user.id,photo=photo)
                    await bot.send_message(message.from_user.id,text='File too big!!')
                    photo=open('docs.jpg','rb')
        except:
            chat_id='Enter your gruop chat id, type : int'
        

            if message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
                link=message.text
                yt=YouTube(link)
        
                await bot.send_message(chat_id,text=f'Average download time: {float(yt.length)/float(2)} sec')
                if yt.streams.first().filesize<5000000:
                
                    yt.streams.get_highest_resolution().download()
                    
                    x=str(yt.streams.filter().first().default_filename).replace('3gpp','mp4')
                    video=open(f'{x}','rb')

     
        
                    await bot.send_message(chat_id,text=f'Channel name: {yt.author}\nDescription: {yt.description}')
                    await bot.send_video(chat_id,video=video)
        
                    await bot.send_message(chat_id,text=f'Completed ✅')
                    os.remove(str(yt.streams.filter().first().default_filename).replace('3gpp','mp4'))
                else:
                    await bot.send_photo(message.from_user.id,photo=photo)
                    await bot.send_message(message.from_user.id,text='File too big!!')
                    photo=open('docs.jpg','rb')
#launchining aiogram code with Dispatcher file as dp
if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True)