import discord
import random

from os import getenv
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv(override=True)

token = getenv('DISCORD_BOT_TOKEN')

if not token:
    raise ValueError("No token provided. Please set the DISCORD_BOT_TOKEN environment variable.")

bot = Bot(
    command_prefix='PREFIX',
    intents=discord.Intents.all()
)

@bot.command()
async def play_game(ctx, bet: str):
    symbols = ['cherry', 'lemon', 'orange', 'plum', 'bell', 'bar', 'seven']
    result = [random.choice(symbols) for _ in range(3)]
    await ctx.send(f"Result: {' | '.join(result)}")

    # Convert bet to integer
    multipliers = {'k': 1_000, 'm': 1_000_000, 'g': 1_000_000_000, 't': 1_000_000_000_000, 'p': 1_000_000_000_000_000, 'e': 1_000_000_000_000_000_000, 'z': 1_000_000_000_000_000_000_000, 'y': 1_000_000_000_000_000_000_000_000}
    if bet[-1].lower() in multipliers:
        bet_amount = int(bet[:-1]) * multipliers[bet[-1].lower()]
    else:
        bet_amount = int(bet)

    # Determine payout ratio based on result
    if result.count(result[0]) == 3:
        payout_ratio = 500 if result[0] == 'cherry' else 25 if result[0] == 'lemon' else 5 if result[0] == 'orange' else 3 if result[0] == 'plum' else 2 if result[0] == 'bell' else 1 if result[0] == 'bar' else 3/4 if result[0] == 'seven' else 0
    elif result.count(result[0]) == 2 or result.count(result[1]) == 2:
        payout_ratio = 25 if 'cherry' in result else 10 if 'lemon' in result else 3 if 'orange' in result else 2 if 'plum' in result else 1 if 'bell' in result else 1 if 'bar' in result else 3/4 if 'seven' in result else 0
    else:
        payout_ratio = 0

    payout = bet_amount * payout_ratio
    await ctx.send(f"Payout: {payout}:1")

@bot.command()
async def vote_reward(ctx, vote_number: int):
    if 1 <= vote_number <= 20:
        multiplier = 1
        reward = 100_000
    elif vote_number == 21:
        multiplier = 3
        reward = 300_000
    elif 22 <= vote_number <= 41:
        multiplier = 2
        reward = 200_000
    elif vote_number == 42:
        multiplier = 6
        reward = 600_000
    elif 43 <= vote_number <= 62:
        multiplier = 3
        reward = 300_000
    elif vote_number == 63:
        multiplier = 9
        reward = 900_000
    elif 64 <= vote_number <= 83:
        multiplier = 4
        reward = 400_000
    elif vote_number == 84:
        multiplier = 12
        reward = 1_200_000
    else:
        await ctx.send("Invalid vote number.")
        return

    await ctx.send(f"Vote Number: {vote_number}, Multiplier: {multiplier}x, Reward: {reward}")

if __name__ == '__main__':
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print("Login failed: Improper token has been passed. Please check your DISCORD_BOT_TOKEN.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")