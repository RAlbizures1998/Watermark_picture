from instagrapi import Client
from instabot import Bot
from pathlib import Path

cl = Client()
bot = Bot()

cl.login(username="r.albizures",password="NorD3!t42320")
# bot.login(username="r.albizures",password="NorD3!t42320")

# media = cl.photo_upload(path=Path("C:\\Users\\Rodrigo\\Desktop\\COURSERA\\Watermark_picture\\watermark\\DSC_3809_watermark.JPG"), caption="First Python upload / project test #python_dev #photo_upload")

media = cl.album_upload(paths=[Path("C:\\Users\\Rodrigo\\Desktop\\COURSERA\\Watermark_picture\\watermark\\DSC_5206_watermark.JPG"), Path("C:\\Users\\Rodrigo\\Desktop\\COURSERA\\Watermark_picture\\watermark\\DSC_4059_watermark.JPG")], caption="Album upload test #python_dev #photo_upload #norway")

# bot.upload_photo(photo=Path("C:\\Users\\Rodrigo\\Desktop\\COURSERA\\Watermark_picture\\watermark\\DSC_3809_watermark.JPG"), caption="First Python upload / project test #python_dev #photo_upload")
