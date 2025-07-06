import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent

# dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY', '')


async def run_search():
    agent = Agent(
        task=(
            '1. 打开 https://www.xiaohongshu.com/explore'
            '2. 点击登录按钮，等待我扫码登录'
            "3. 在搜索框中搜索 '漂亮小姐姐' "
            "4. 点击第一个图片"
        ),
        llm=ChatOpenAI(
            base_url='http://172.31.114.167',
            api_key=SecretStr(api_key),
            model="gpt-4o"
        ),
        use_vision=False,
    )

    await agent.run()


if __name__ == '__main__':
    asyncio.run(run_search())
