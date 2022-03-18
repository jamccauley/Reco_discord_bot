import os
import io
import random
import discord
from dotenv import load_dotenv
from PIL import Image, ImageFilter, ImageEnhance
import requests
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np

model = InceptionV3(weights='imagenet')

def predict_class(img):
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    top_pred = decode_predictions(preds, top=1)[0]

    return top_pred[0][1], top_pred[0][2]

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='resize', help='Have Reco resize an image for you. usage = "!resize 128 128"')
async def resizeimage(ctx, a, b):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
    else:
        return

    im = Image.open(requests.get(attachment, stream=True).raw)

    if (a != None) and (b != None):
        im = im.resize(a,b)
    elif (a != None):
        im = im.resize(a,a)

    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

@bot.command(name='thumb', help='Have Reco resize an image into a thumbnail for you.')
async def thumbimage(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
    else:
        return

    im = Image.open(requests.get(attachment, stream=True).raw)

    im = im.thumbnail()

    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

@bot.command(name='grey', help='Have Reco turn an image B&W for you.')
async def greyimage(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
    else:
        return

    im = Image.open(requests.get(attachment, stream=True).raw)

    im = im.convert('L')

    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

@bot.command(name='deepfry', help='Have Reco help you deep fry an image.')
async def getimage(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
    else:
        return

    im = Image.open(requests.get(attachment, stream=True).raw)
    im = im.filter(ImageFilter.GaussianBlur(3))
    im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=400, threshold=0))
    coloren = ImageEnhance.Color(im)
    im = coloren.enhance(4)
    brighten = ImageEnhance.Brightness(im)
    im = brighten.enhance(3)
    conten = ImageEnhance.Contrast(im)
    im = conten.enhance(3)
    im = coloren.enhance(4)
    im = brighten.enhance(3)
    im = conten.enhance(3)

    with io.BytesIO() as image_binary:
        im.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

@bot.command(name='predict', help='Gets Reco to predict what the attached image is!')
async def predictimage(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
    else:
        return

    im = Image.open(requests.get(attachment, stream=True).raw)
    im = im.resize((299,299))
    msg, confidence = predict_class(im)
    msg_parts = msg.split('_')
    vowels = ['a','e','i','o','u']
    if msg_parts[0][0] in vowels:
        aan = "an ";
    else:
        aan = "a "
    confidence = '{:.1%}'.format(confidence)
    msg_formatted = 'Reco thinks this image is ' + aan + ' '.join(msg_parts) + ' with ' + confidence + ' confidence.'
    await ctx.send(msg_formatted)

bot.run(TOKEN)
