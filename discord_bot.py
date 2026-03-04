import discord
from discord.ext import commands
import subprocess
import asyncio
import os

# ==========================================
# 🔑 Discord設定
# ==========================================
# BotのTokenは環境変数または .env 等から読み込みます（GitHub等へプッシュするため直書き厳禁）
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

# 実行を許可するチャンネルのID（数値）
ALLOWED_CHANNEL_ID = int(os.environ.get("DISCORD_CHANNEL_ID", "1477176779906089053"))  # ご自身のチャンネルIDに書き換えてください

# インテントの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Discordボットが起動しました。ログインユーザー: {bot.user}")
    print("「!update」とDiscordで送信すると、ニュースの更新が開始されます。")

@bot.command()
async def update(ctx):
    # 指定したチャンネル以外での実行を防ぐ
    if ctx.channel.id != ALLOWED_CHANNEL_ID:
        return

    # 処理開始のメッセージを送信
    await ctx.send("🔄 **ニュースの更新を開始します！**\nAIの分析が終わるまで、約2〜3分ほどお待ちください...")

    try:
        # update_news.pyを実行（非同期でサブプロセスとして実行）
        process = await asyncio.create_subprocess_exec(
            "/Users/yuki_mcd/anaconda3/bin/python", "update_news.py",
            cwd="/Users/yuki_mcd/Desktop/NewsSummary",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await ctx.send("✅ **ニュースの更新が完了しました！**\nご自宅のPCの `index.html` が最新状態になっています。")
        else:
            error_msg = stderr.decode('utf-8')
            await ctx.send(f"❌ **エラーが発生しました:**\n```{error_msg[:1900]}```")

    except Exception as e:
        await ctx.send(f"❌ **予期せぬエラーが発生しました:**\n{e}")

if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("エラー: 環境変数 DISCORD_BOT_TOKEN が設定されていません。")
    else:
        bot.run(DISCORD_BOT_TOKEN)
