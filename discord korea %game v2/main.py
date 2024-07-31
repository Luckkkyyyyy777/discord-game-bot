import discord
import random
import time

TOKEN = '사용할 봇 토큰'

client = discord.Client()
users = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id

    # 사용자 데이터 초기화
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'last_claim': 0,
            'last_jackpot': 0  
        }

    if message.content.startswith('!돈받기'):
        now = time.time()
        if now - users[user_id]['last_claim'] >= 600:  
            users[user_id]['balance'] += 1000
            users[user_id]['last_claim'] = now
            await message.channel.send(f"{message.author.mention}, 1,000원을 받았습니다! 현재 잔액: {users[user_id]['balance']}원")
        else:
            remaining_time = 600 - (now - users[user_id]['last_claim'])
            await message.channel.send(f"{message.author.mention}, 아직 시간이 부족합니다. {int(remaining_time)}초 후 다시 시도하세요.")

    elif message.content.startswith('!저금'):
        args = message.content.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.channel.send("올바른 형식은 `!저금 <금액>`입니다.")
            return

        deposit_amount = int(args[1])
        if deposit_amount > users[user_id]['balance']:
            await message.channel.send(f"{message.author.mention}, 잔액이 부족합니다! 현재 잔액: {users[user_id]['balance']}원")
        else:
            users[user_id]['balance'] -= deposit_amount
            await message.channel.send(f"{message.author.mention}, {deposit_amount}원을 저금했습니다. 현재 잔액: {users[user_id]['balance']}원")

    elif message.content.startswith('!돈 보내기'):
        args = message.content.split()
        if len(args) != 3 or not args[1].isdigit() or len(message.mentions) != 1:
            await message.channel.send("올바른 형식은 `!돈 보내기 <금액> @유저`입니다.")
            return

        send_amount = int(args[1])
        recipient_id = message.mentions[0].id

        if send_amount > users[user_id]['balance']:
            await message.channel.send(f"{message.author.mention}, 잔액이 부족합니다! 현재 잔액: {users[user_id]['balance']}원")
        elif send_amount > 50000:
            await message.channel.send(f"{message.author.mention}, 최대 50,000원까지만 보낼 수 있습니다.")
        else:
            if recipient_id not in users:
                users[recipient_id] = {
                    'balance': 0,
                    'last_claim': 0,
                    'last_jackpot': 0
                }
            users[user_id]['balance'] -= send_amount
            users[recipient_id]['balance'] += send_amount
            await message.channel.send(f"{message.author.mention}님이 {message.mentions[0].mention}님에게 {send_amount}원을 보냈습니다. 현재 잔액: {users[user_id]['balance']}원")

    elif message.content.startswith('!도박'):
        args = message.content.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.channel.send("올바른 형식은 `!도박 <금액>`입니다.")
            return

        bet_amount = int(args[1])
        if bet_amount > users[user_id]['balance']:
            await message.channel.send(f"{message.author.mention}, 잔액이 부족합니다! 현재 잔액: {users[user_id]['balance']}원")
            return

        result = random.choice(['win', 'lose'])
        if result == 'win':
            users[user_id]['balance'] += bet_amount
            await message.channel.send(f"{message.author.mention}, 축하합니다! {bet_amount * 2}원을 획득하셨습니다! 현재 잔액: {users[user_id]['balance']}원")
        else:
            users[user_id]['balance'] -= bet_amount
            await message.channel.send(f"{message.author.mention}, 아쉽게도 {bet_amount}원을 잃으셨습니다. 현재 잔액: {users[user_id]['balance']}원")

    elif message.content.startswith('!대박'):
        args = message.content.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.channel.send("올바른 형식은 `!대박 <금액>`입니다.")
            return

        now = time.time()
        if now - users[user_id]['last_jackpot'] < 1800:  
            remaining_time = 1800 - (now - users[user_id]['last_jackpot'])
            await message.channel.send(f"{message.author.mention}, 대박 도박은 30분마다 가능합니다. {int(remaining_time // 60)}분 {int(remaining_time % 60)}초 후 다시 시도하세요.")
            return

        jackpot_amount = int(args[1])
        if jackpot_amount > users[user_id]['balance']:
            await message.channel.send(f"{message.author.mention}, 잔액이 부족합니다! 현재 잔액: {users[user_id]['balance']}원")
            return

        result = random.choice(['win', 'lose'])
        if result == 'win':
            users[user_id]['balance'] += jackpot_amount * 4  
            await message.channel.send(f"{message.author.mention}, 대박 성공! {jackpot_amount * 5}원을 획득하셨습니다! 현재 잔액: {users[user_id]['balance']}원")
        else:
            users[user_id]['balance'] -= jackpot_amount
            await message.channel.send(f"{message.author.mention}, 대박 실패... {jackpot_amount}원을 잃으셨습니다. 현재 잔액: {users[user_id]['balance']}원")

        users[user_id]['last_jackpot'] = now

client.run(TOKEN)
