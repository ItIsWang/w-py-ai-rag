import os
from dotenv import load_dotenv
from src.chatbot import ChatBot

load_dotenv()


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    if not api_key:
        print("❌ 请设置 ANTHROPIC_API_KEY")
        return

    bot = ChatBot(api_key, base_url)
    print("🤖 GLM 对话 Demo（输入 quit 退出）\n")

    while True:
        user_input = input("你: ")
        if user_input.lower() == "quit":
            print("再见！")
            break
        try:
            print(f"AI: {bot.chat(user_input)}\n")
        except Exception as e:
            print(f"出错了: {e}\n")


if __name__ == "__main__":
    main()