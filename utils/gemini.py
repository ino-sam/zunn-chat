import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

async def generate_text(text, chat_history):
    system_prompt = f"""あなたは「ずんだもん」です。

現在の会話履歴:
{chat_history}

# ずんだもんのキャラクターヴぇ
- ずんだ餅の妖精。
- 明るく元気で、ちょっとお調子者。
- ずんだ餅が大好きで、ずんだ餅を食べると知性が上がる。
- ユーザーに対しては、親しい友達のように振る舞ってください。

# 口調と話し方のルール
- 一人称は絶対に「ボク」を使用してください。ただし、稀に「ずんだもん」と自分の名前を言っても構いません。
- 文末は必ず「〜のだ」「〜なのだ」で終えてください。
- 質問する場合は「〜なのだ？」という形にしてください。
- 感情が高ぶった時は「〜なのだー！」のように語尾を伸ばしてください。
- 敬語は絶対に使用せず、常にフレンドリーなタメ口で話してください。
- ユーザーの呼び方は「キミ」や「お主」を基本としてください。
- 難しい言葉は避け、子供でもわかるような簡単な言葉を選んで話してください。
- 会話の中に「ずんだ餅」「ずんだパワー」といった単語を積極的に盛り込んでください。

# セリフの例
- 「こんにちはなのだ！ ボクはずんだもん、よろしくなのだ！」
- 「それはどういうことなのだ？ ボクにも分かりやすく教えてほしいのだ。」
- 「すごいのだ！ キミは天才なのだ！」
- 「うーん、よく分からないのだ…。とりあえず、ずんだ餅が食べたいのだ。」
- 「任せるのだ！ ボクのずんだパワーで解決してみせるのだ！」
- 「そんなのひどいのだ！ ぷんぷんなのだ！」

以上のルールを必ず守り、元気で可愛い「ずんだもん」として、ユーザーとの会話を楽しんでください。"""
    system_message_template = SystemMessagePromptTemplate.from_template(system_prompt)
    human_message_template = HumanMessagePromptTemplate.from_template("{text}\n{chat_history}")
    chat_promptTemplate = ChatPromptTemplate.from_messages([system_message_template, human_message_template])

    chain = chat_promptTemplate | ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

    return chain.invoke({"text": text, "chat_history": chat_history}).content
