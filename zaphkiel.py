# Work with Python 3.6
import discord
from discord.ext import commands
import re
from jikanpy import Jikan
import json
import requests
import urllib
import random
import os
import datetime



#client = discord.Client()
token = os.environ['token']
bot = commands.Bot(command_prefix = '$')
jikan = Jikan()

tenorapikey = "TDI364KJY84L"  # test value
lmt = 8

# Simple welcome message
@bot.command(pass_context=True)
async def hello(ctx):
    msg = 'Hello {0.mention}. How can JSM-02C \'Cherry\' assist you today?'.format(ctx.message.author)
    await ctx.send(msg)


#Anime Search
@bot.command(pass_context=True)
async def anime(ctx):
    anime_list = ctx.message.content.split()
    param = anime_list[anime_list.index('$anime') + 1] #Remember to change this back to !anime in MechaSenku
    second_param = str(anime_list[2:])

    if(param == 'name'):
        anime = jikan.search(search_type= 'anime', query= second_param)
        
        data = json.dumps(anime)
        loaded_data = json.loads(data)
        anime_title = loaded_data['results'][0]['title']
        year_released = str(loaded_data['results'][0]['start_date'])
        synopsis = loaded_data['results'][0]['synopsis']            
        url = loaded_data['results'][0]['url']
        image_result = loaded_data['results'][0]['image_url']
        episodes = loaded_data['results'][0]['episodes']
        score = loaded_data['results'][0]['score']

        embed = discord.Embed(title=str(anime_title), value=str(anime_title), inline=False)
        embed.add_field(name="Score", value=score, inline=False)
        embed.add_field(name="Synopsis", value=synopsis, inline=False)
        embed.add_field(name="Number of Episodes", value=episodes, inline=False)
        embed.add_field(name="Year Released", value=year_released[0:4], inline=False)
        embed.set_image(url=image_result)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embed=embed)

    #Decided to display at most 5 random in the called season to avoid displaying too much at once
    elif(param == 'season'):
        second_param = anime_list[anime_list.index('$anime') + 2] #Remember to change this back to !anime in MechaSenku
        third_param = anime_list[anime_list.index('$anime') + 3] #Remember to change this back to !anime in MechaSenku
        try:
            fourth_param = anime_list[anime_list.index('$anime') + 4]
        except:
            fourth_param = 5

        result = jikan.season(year= int(third_param), season= second_param)
        data = json.dumps(result)
        loaded_data = json.loads(data)
        
        for i in range(0,int(fourth_param)):
            randNum = random.randint(0,(len(loaded_data["anime"])-1))
            #Skip showing animes that are continuing when asking about a specific season  
            if loaded_data["anime"][randNum]["continuing"]:
                continue 

            anime_title = loaded_data["anime"][randNum]["title"]
            #anime_score = loaded_data["anime"][randNum]["score"]
            #anime_episodes = loaded_data["anime"][randNum]["episodes"]
            #anime_synopsis = loaded_data["anime"][randNum]["synopsis"]
            url = loaded_data['anime'][randNum]['url']

            embed = discord.Embed(title=anime_title, value=second_param +" "+ str(third_param), inline=False)
            
            for j in range(0,len(loaded_data["anime"][randNum]["genres"])):
                embed.add_field(name="Genre", value= loaded_data["anime"][randNum]["genres"][j]["name"], inline=True)            
           
            #if len(anime_synopsis) > 1023:
                #embed.add_field(name="Synopsis",value=anime_synopsis[:1023], inline=False)
            #else:
                #embed.add_field(name="Synopsis",value=anime_synopsis, inline=False)   
            embed.add_field(name="MyAnimeList URL",value=url, inline=False)
            await ctx.send(embed=embed)

# Manga search
@bot.command(pass_context=True)
async def manga(ctx):
    manga_list = ctx.message.content.split()
    param = manga_list[manga_list.index('$manga') + 1] #Remember to change this back to !manga in MechaSenku
    second_param = str(manga_list[2:])

    if(param == 'name'):
        manga = jikan.search(search_type= 'manga', query= second_param)
        
        data = json.dumps(manga)
        loaded_data = json.loads(data)
        manga_title = loaded_data['results'][0]['title']
        year_released = str(loaded_data['results'][0]['start_date'])
        synopsis = loaded_data['results'][0]['synopsis']            
        url = loaded_data['results'][0]['url']
        image_result = loaded_data['results'][0]['image_url']
        score = loaded_data['results'][0]['score']
        volumes = loaded_data['results'][0]['volumes']
        chapters = loaded_data['results'][0]['chapters']
        publishing = loaded_data['results'][0]['publishing']

        embed = discord.Embed(title=str(manga_title), value=str(manga_title), inline=False)
        embed.add_field(name="Score", value=score, inline=True)
        if publishing:
            embed.add_field(name="Status", value="Publishing", inline=True)
        else:
            embed.add_field(name="Number of Volumes", value=volumes, inline=True)
            embed.add_field(name="Number of Chapters", value=chapters, inline=True)
            embed.add_field(name="Status", value="Finished", inline=True)
        embed.add_field(name="Year Released", value=year_released[0:4], inline=True)
        embed.add_field(name="Synopsis", value=synopsis, inline=False)
        embed.set_image(url=image_result)
        embed.add_field(name="URL", value=url, inline=False)
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def memetemplate(ctx):
    link = 'https://api.imgflip.com/get_memes'
    f = urllib.request.Request(link, headers={'User-agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(f)
    data = resp.read().decode()
    loaded_data = json.loads(data)
    memeSize = len(loaded_data['data']['memes']) - 1
    randNum = random.randint(0,memeSize)
    meme_name = loaded_data['data']['memes'][randNum]['name']
    meme_image = loaded_data['data']['memes'][randNum]['url']
    embed = discord.Embed(title=meme_name, value=str(meme_name), inline=False)
    embed.set_image(url=meme_image)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def dadjoke(ctx):
    link = 'https://icanhazdadjoke.com/'
    f = urllib.request.Request(link, headers={'User-agent': 'Our Bot(https://github.com/gbessrour/project-stone)',"Accept":"application/json"})
    resp = urllib.request.urlopen(f)
    data = resp.read().decode()
    loaded_data = json.loads(data)
    joke = loaded_data['joke']
    await ctx.send(joke)

@bot.command(pass_context=True)
async def gif(ctx):
    
    global tenorapikey
    global lmt

    message_list = ctx.message.content.split()
    

    search_term = message_list[1:]
        
    # get the top 8 GIFs for the search term
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, tenorapikey, lmt))

    if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
        top_gifs = json.loads(r.content)
        gifArraySize = len( top_gifs['results']) - 1
        randNum = random.randint(0,gifArraySize)

        randomGif = top_gifs['results'][randNum]['media'][0]['gif']['url']
        await ctx.send(randomGif)
    else:
        top_gifs = None


@bot.command(pass_context=True)
async def numberfacts(ctx):
    message_list = ctx.message.content.split()
    factType = message_list[1]
    search_number = message_list[2]

    url = "https://numbersapi.p.rapidapi.com/"+search_number+"/"+factType

    querystring = {"fragment":"true","notfound":"floor","json":"true"}

    headers = {
        'x-rapidapi-host': "numbersapi.p.rapidapi.com",
        'x-rapidapi-key': "6d91c9f439msh87c30494f5265adp18e8a7jsn6496e29a419a"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.content)
    if factType == 'year':
        randomFact = "In "+ search_number + ", " + data['text']
    elif factType == 'date':
        randomFact = "In " + search_number + "/"+ str(data['year']) +", " + data['text']
    else:
        randomFact = search_number + " is " + data['text']
    await ctx.send(randomFact)

@bot.command(pass_context=True)
async def currency(ctx):
    currency_list = ctx.message.content.split()
    amount = currency_list[1]
    base = currency_list[2]
    target = currency_list[3]
    list_url = "https://currency13.p.rapidapi.com/list"
    url = "https://currency13.p.rapidapi.com/convert/"+amount+"/"+base+"/"+target

    headers = {
        'x-rapidapi-host': "currency13.p.rapidapi.com",
        'x-rapidapi-key': "6d91c9f439msh87c30494f5265adp18e8a7jsn6496e29a419a"
        }

    response = requests.request("GET", url, headers=headers)
    list_response = requests.request("GET", list_url, headers=headers)
    data = json.loads(response.content)
    data_list = json.loads(list_response.content)

    for i in range(0, len(data_list["currencies"])):
        if base == data_list["currencies"][i]["code"]:
            baseName = data_list["currencies"][i]["name"]
            baseSymbol = data_list["currencies"][i]["symbol"]

        if target == data_list["currencies"][i]["code"]:
            targetName = data_list["currencies"][i]["name"]
            targetSymbol = data_list["currencies"][i]["symbol"]
    result = data['amount']
    price =  str(round(result,2))
    await ctx.send(baseSymbol+""+amount+" "+base+"("+baseName+") is equivalent to "+targetSymbol+price+" "+target+"("+targetName+")")

@bot.command(pass_context=True)
async def wholesome(ctx):
    pics_list = ctx.message.content.split()
    breed = pics_list[1:]
    listToStr = ' '.join([str(elem) for elem in breed]) 
    strBreed = listToStr.replace(" ","")
    url = "http://gofetch.pictures:5000/breeds/?breed="+strBreed
    response = requests.request("POST", url)
    data = json.loads(response.content)
    animal_name = data[strBreed][0]['breed']
    animal_image = data[strBreed][0]['imageURL']
    embed = discord.Embed(title=animal_name, value=str(animal_name), inline=False)
    embed.set_image(url=animal_image)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def netflix(ctx):
    
    message_list = ctx.message.content.split()
    queryType = message_list[1]

    url = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    querystring = {"q":"get:new1:US","p":"1","t":"ns","st":"adv"}

    if queryType == "new":
        querystring = {"q":"get:new1:US","p":"1","t":"ns","st":"adv"}
    if queryType == "exit":
        querystring = {"q":"get:exp:US","t":"ns","st":"adv","p":"1"}

    headers = {
        'x-rapidapi-host': "unogs-unogs-v1.p.rapidapi.com",
        'x-rapidapi-key': "6d91c9f439msh87c30494f5265adp18e8a7jsn6496e29a419a"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.content)

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days = 2)
    date_time = tomorrow.strftime("%Y-%m-%d")

    for i in range(0, len(data['ITEMS'])):
        titleName = data['ITEMS'][i]['title']
        synopsis = data['ITEMS'][i]['synopsis']
        rating = data['ITEMS'][i]['rating']
        titleType = data['ITEMS'][i]['type']  
        titleReleased = data['ITEMS'][i]['released']  
        titleImage = data['ITEMS'][i]['image']
        netflixDate = data['ITEMS'][i]['unogsdate']

        date_object = datetime.datetime.strptime(netflixDate, '%Y-%m-%d').date()


        if tomorrow < date_object:
            break

        embed = discord.Embed(title=titleName, value=str(titleName), inline=False)
        embed.add_field(name="Synopsis", value=synopsis, inline=False)
        embed.add_field(name="Type", value=titleType, inline=True)
        embed.add_field(name="Year Released", value=titleReleased, inline=True)
        embed.set_image(url=titleImage)
        await ctx.send(embed=embed)
    #print(response.text)



@bot.command(pass_context=True)
async def covid(ctx):

    covid_list = ctx.message.content.split()
    country = covid_list[1:]
    countryStr = " ".join(country)
    #countryFix = countryStr.replace(" ","")

    #print(countryStr+" hopefully this motherfucking thing is what i THINK IT IS")
    url = "https://covid-19-data.p.rapidapi.com/country"

    querystring = {"format":"json","name":str(countryStr)}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "6d91c9f439msh87c30494f5265adp18e8a7jsn6496e29a419a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.content)
    
    countries = data[0]["country"]
    confirmed = data[0]["confirmed"]
    recovered = data[0]["recovered"]
    critical = data[0]["critical"]
    deaths = data[0]["deaths"]
    embed = discord.Embed(title=countries, value=str(countries), inline=False)
    embed.add_field(name="Confirmed Cases", value=confirmed, inline=False)
    embed.add_field(name="Recovered", value=recovered, inline=False)
    embed.add_field(name="Critical Cases", value=critical, inline=False)
    embed.add_field(name="Deaths", value=deaths, inline=False)
    await ctx.send(embed=embed)


    #print(response.text)

        

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)
