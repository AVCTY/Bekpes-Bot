# bot.py
import os
import discord
import random
import asyncio

from dotenv import load_dotenv
from random import choice
from pretty_help import PrettyHelp, Navigation

# importing commands from discord.ext
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents(messages=True, members=True, guilds=True)

bot = commands.Bot(command_prefix=";", case_insensitive=True, intents=intents, help_command=PrettyHelp())

nav = Navigation("⬇", "⬆")
no_category = "Fun"

bot.help_command = PrettyHelp(navigation=nav, show_index=False, no_category=no_category)

#=========================================================================================================================================

@bot.event
async def on_ready():
    # Setting `Listening` status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=";help"))

#=========================================================================================================================================

# Bekpes command targetted at random users
@bot.command(name="Bekpes", help="Bekpes a random person or someone you've tagged.")
async def bekpes(ctx, *, message=None, user: discord.Member = None):
    bekpes_quotes = [
        "is my BEKPES",
        "kenak ku BEKPES",
        "BEKPES AH",
        "imagine getting bekpes",
        "DOWN LA BODO",
        "hate em",
        "xtnYk",
        "SORRY LORRR UUUUEEEEEE",
        "cornelius.",
        "FUCKINGG SMACKKK",
        "can't be arsed",
        "HAA?",
        "BEKPES CAKK BISSS",
        "is gay",
        "kenak PAMPES",
        "FAK LOR",
        "come on mayne"
    ]

    if user!=None and message==None:
        await ctx.send(f"{user.mention} {random.choice(bekpes_quotes)}")
    elif user==None and message!=None:
        await ctx.send(f"{message} {random.choice(bekpes_quotes)}")
    else:
        user = choice(ctx.message.channel.guild.members)
        await ctx.send(f"{user.mention} {random.choice(bekpes_quotes)}")

#=========================================================================================================================================

# Poke command which selects a random user to poke
@bot.command(name="Poke", help="Pokes a random or tagged user. Oldschool Facebook style.")
async def poke(ctx, user: discord.Member=None):
    if user!=None:
        await ctx.send(f"{ctx.message.author.mention} poked {user.mention}")
    else:
        user = choice(ctx.message.channel.guild.members)
        await ctx.send(f"{ctx.message.author.mention} poked {user.mention}")

#=========================================================================================================================================

# Random ban command which will randomly
# select a user to ban from the server
@bot.command(name="Randomban", help="Randomly bans a user in the server hehe.")
async def ban(ctx, reason=None):
    await ctx.send(f"Do you wanna randomban? y or n (reply within 10 seconds)")
    
    # ensures that response will only be registered if these
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=10) # 10 seconds timer before timeout
        
        if msg.content == "y" or msg.content == "Y" or msg.content == "yes" or msg.content == "Yes" or msg.content == "YES":
            await ctx.send("You answered yes, its bekpes time")
            
            # Gets random user from server members list
            user = choice(ctx.message.channel.guild.members)

            # Checks if user is empty or is the message author
            if user == None or user == ctx.message.author:
                # Returns failed ban message if user is empty or is the message author
                await ctx.send("You cannot ban yourself BODO!")
                return
            if reason == None:
                # Sets a default reason if none is given
                reason = "Kenak ku BEKPES ah!"

            # Prints out ban message
            message = f"You were banned from {ctx.guild.name} for {reason}"
            await ctx.guild.ban(user, reason=reason)
            await ctx.channel.send(f"{user} has been bekpes!")
        elif msg.content == "n" or msg.content == "N" or msg.content == "no" or msg.content == "No" or msg.content == "NO":
            await ctx.send("You answered no, guess no one is getting bekpes today")
            return
        elif msg.content != "y" or msg.content != "n" or msg.content == "yes" or msg.content == "no" or msg.content == "Yes" or \
        msg.content == "No" or msg.content == "YES" or msg.content == "NO":
            await ctx.send("That was not a valid answer bodo")
            return
    except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")

#=========================================================================================================================================

# Emote command to send an emote to the tagged person in chat
@bot.command(name="Emote", help="Shows appreciation to a random or tagged user.")
async def imagine(ctx, user: discord.Member=None):
    imagine_quotes = [
        "<:MAX:760740764933816330>",
        "<:KEKW:750782709911126149>",
        "<:AhegaoForLoren:765606891014979615>",
        "<:PeepoLove:762214856312356874>",
        "that's not very <:POGCHAMP:750782710116515908> of you",
        "<:lickfoot:761941939561168936>"
    ]

    response = choice(imagine_quotes)
    if user!=None:
        await ctx.send(f"{ctx.author.mention} " + response + f" {user.mention}")
    else:
        user = choice(ctx.message.channel.guild.members)
        await ctx.send(f"{ctx.author.mention} " + response + f" {user.mention}")

#=========================================================================================================================================

# Number guessing game
@bot.command(name="Guess", help="A random number guessing game.")
async def numberguess(ctx):
    await ctx.send("I'm guessing of a number between 1 to 10. Enter your guess")

    num = random.randrange(1, 11) # gets a random number from 1 to 10
    guesses = 3

    # ensures that response will only be registered if these
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        while guesses > 0:
            msg = await bot.wait_for("message", check=check, timeout=10)
            ans = int(msg.content)
            
            if ans < num:
                guesses -= 1
                await ctx.send("Your guess was small. Like ur brain. " + str(guesses) + " guesses left.")
            elif ans == num:
                await ctx.send("Bekpes! ez guess. Congrats. The number I was thinking of was: " + str(num))
                return
            elif ans > num:
                guesses -= 1
                await ctx.send("Your guess was big bodo. " + str(guesses) + " guesses left.")
        else:
            await ctx.send("Bekpes ah you really couldn't guess the number? Down la bodo I was thinking of the number: " + str(num))
    except asyncio.TimeoutError:
        await ctx.send("Oi bodo at least reply??")

#=========================================================================================================================================

# Magic 8-Ball
@bot.command(name="8Ball", help="Consult the Magic 8-Ball")
async def magic8ball(ctx, *, message=None):
    ball_quotes = [
        "Possibly so.",
        "That is unlikely",
        "Fortunately, that might happen",
        "As I see it, yes",
        "Cornelius.",
        "Outlook not so clear",
        "Ooo... that's not gonna happen",
        "Without a doubt",
        "Yep. Very much so",
        "My reply is no",
        "Cannot predict right now",
        "Most likely",
        "Yikes, you wish buddy",
        "Yea I guess that is possible",
        "Hell nah you trippin",
        "Fuck yea",
        "Yes..."
        ]

    exitReplies = [
        "OK then you fuck, I'll just take my business somewhere else",
        "Fine then, don't ask me about your lousy ass questions",
        "I'm a magic 8-ball, not your fucking personal assistant",
        "Fuck outta here with your yeeyee ass haircut, niigGGaaAA"
        ]
    
    response = random.choice(ball_quotes)
    
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    if message == None:
        await ctx.send("== Magic 8-Ball ==\n Enter your question for me (reply within 10 seconds)")
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=10)
            await ctx.send(f":8ball:: {ctx.author.mention} {response}")
        except asyncio.TimeoutError:
            await ctx.send(f"You didn't reply in time. {random.choice(exitReplies)}")
    else:
        if response == "Yes...":
            await ctx.send(f"== Magic 8-Ball ==\n:8ball:: {ctx.author.mention} {response}")
            await asyncio.sleep(2) # sleep for 2 seconds then send message again
            await ctx.send(":8ball:: SIKE")
        else:
            await ctx.send(f"== Magic 8-Ball ==\n:8ball:: {ctx.author.mention} {response}")

#=========================================================================================================================================
           
# Blackjack
@bot.command(name="Blackjack", help="Play some good'ol Blackjack, not with Jack Black unfortunately.")
async def blackjack(ctx):
    message = "Your Hand: "
    Dmessage = "Dealer's Hand: "
    
    # dictionary for card faces and their values
    deck = {
        "A":1,
        "2":2,
        "3":3,
        "4":4,
        "5":5,
        "6":6,
        "7":7,
        "8":8,
        "9":9,
        "10":10,
        "J":10,
        "Q":10,
        "K":10
    }

    # card suits
    suits = [
        "<:Spades:805169720340250644>",
        "<:Hearts:805169720252039188>",
        "<:Clubs:805169720290312272>",
        "<:Diamonds:805169719966695505>"
    ]

    # Class for dealer hand
    class Dhand:
        DealerSuit = None
        DealerFace = None
        DealerValue = 0

        def __init__(self, dsuit, dface, dvalue):
            self.DealerSuit = dsuit
            self.DealerFace = dface
            self.DealerValue = dvalue

    # generate cards for dealer
    def Dgenerate():
        ps = random.choice(suits) # saving suits to var
        pf = random.choice(list(deck.keys())) # saving card key to var
        pv = deck[pf] # getting value corresponding to the right key

        card = Dhand(ps, pf, pv)
        return card

    def Dhit(l):
        l.append(Dgenerate())

    # Class for player hand
    class hand:
        PlayerSuit = None
        PlayerFace = None
        PlayerValue = 0

        def __init__(self, psuit, pface, pvalue):
            self.PlayerSuit = psuit
            self.PlayerFace = pface
            self.PlayerValue = pvalue

    # generate cards for player
    def generate():
        ps = random.choice(suits) # saving suits to var
        pf = random.choice(list(deck.keys())) # saving card key to var
        pv = deck[pf] # getting value corresponding to the right key

        card = hand(ps, pf, pv)
        return card

    def hit(l):
        l.append(generate())

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        handcards = []
        dhandcards = []
        if len(handcards) == 0:
            total = 0

            # generate cards for the player
            await ctx.send("== Let's Play Some Blackjack (Without Jack Black) ==")
            hit(handcards)
            hit(handcards)

            # check if its Face cards or 10 with an Ace then set value of ace to 11 for a blackjack
            if handcards[0].PlayerFace == "K" and handcards[1].PlayerFace == "A":
                handcards[1].PlayerValue = 11

            elif handcards[0].PlayerFace == "Q" and handcards[1].PlayerFace == "A":
                handcards[1].PlayerValue = 11

            elif handcards[0].PlayerFace == "J" and handcards[1].PlayerFace == "A":
                handcards[1].PlayerValue = 11

            elif handcards[0].PlayerFace == "10" and handcards[1].PlayerFace == "A":
                handcards[1].PlayerValue = 11

            elif handcards[0].PlayerFace == "A" and handcards[1].PlayerFace == "K":
                handcards[0].PlayerValue = 11

            elif handcards[0].PlayerFace == "A" and handcards[1].PlayerFace == "Q":
                handcards[0].PlayerValue = 11

            elif handcards[0].PlayerFace == "A" and handcards[1].PlayerFace == "J":
                handcards[0].PlayerValue = 11

            elif handcards[0].PlayerFace == "A" and handcards[1].PlayerFace == "10":
                handcards[0].PlayerValue = 11

            for i in handcards:
                message += i.PlayerSuit + i.PlayerFace + "    "
                total += i.PlayerValue

            await ctx.send(message)

            await ctx.send(f"\nTotal: {total}") # prints out total sum of cards in hand

        # generate cards for the dealer
        if len(dhandcards) == 0:
            Dtotal = 0

            Dhit(dhandcards)
            Dhit(dhandcards)

            for i in dhandcards:
                Dmessage += i.DealerSuit + i.DealerFace + "    "
                Dtotal += i.DealerValue

        # checks player total for whether they blackjack or not
        if total == 21:
            for i in dhandcards:
                Dmessage += i.DealerSuit + i.DealerFace

            await ctx.send(f"Blackjack! You Win\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
            return
        while True:
            await ctx.send("[H]it or [S]tand? (Reply within 10 seconds)")

            msg = await bot.wait_for("message", check=check, timeout=10)

            if msg.content == "H" or msg.content == "h" or msg.content == "Hit" or msg.content == "hit" or msg.content == "HIT":
                hit(handcards)
                total = 0
                message = "Your Hand: "

                for i in handcards:
                    message += i.PlayerSuit + i.PlayerFace + "    "
                    total += i.PlayerValue

                await ctx.send(f"{message}\nTotal: {total}")

                if total > 21:
                    Dmessage = "Dealer's Hand: "
                    for i in dhandcards:
                        Dmessage += i.DealerSuit + i.DealerFace + "    "

                    await ctx.send(f"\nBust! You Lose!\n\n{Dmessage}\nDealer Total: {Dtotal}\nDealer Wins!") # printing out total sum of cards in hand
                    return
                elif total == 21:
                    Dmessage = "Dealer's Hand: "
                    for i in dhandcards:
                        Dmessage += i.DealerSuit + i.DealerFace + "    "

                    await ctx.send(f"\nBlackjack! You Win\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total sum of cards in hand
                    return
                elif total <= 21 and len(handcards) == 5:
                    Dmessage = "Dealer's Hand: "
                    for i in dhandcards:
                        Dmessage += i.DealerSuit + i.DealerFace + "    "

                    await ctx.send(f"\nFive card trick! You Win\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total sum of cards in hand
                    return
            elif msg.content == "S" or msg.content == "s" or msg.content == "Stand" or msg.content == "stand" or msg.content == "STAND":
                await ctx.send(f"{message}\nTotal: {total}") # printing out total sum of cards in hand

                while Dtotal < 17:
                    if Dtotal < total:
                        if Dtotal <= 16:
                            if total <= 16 or total < 21:
                                Dhit(dhandcards)
                                Dtotal = 0
                                Dmessage = "Dealer's Hand: "
                                for i in dhandcards:
                                    Dmessage += i.DealerSuit + i.DealerFace + "    "
                                    Dtotal += i.DealerValue

                if Dtotal > 21:
                    await ctx.send(f"Dealer Bust! You Win\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
                    return
                elif Dtotal == 21:
                    await ctx.send(f"Dealer Blackjack! You Lose!\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
                    return
                elif Dtotal > total and Dtotal <= 21:
                    await ctx.send(f"Dealer Wins!\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
                    return
                elif Dtotal == total:
                    await ctx.send(f"Draw!\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
                    return
                elif total > Dtotal and total <=21:
                    await ctx.send(f"You Win!\n\n{Dmessage}\nDealer Total: {Dtotal}") # printing out total of sum of cards in hand
                    return
    except asyncio.TimeoutError:
        await ctx.send(f"You didn't reply in time.")
        
bot.run(TOKEN)
