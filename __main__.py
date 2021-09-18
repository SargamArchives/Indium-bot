from better_bot import IndiumBot
from Config.config import BOT_TOKEN


def main():
    client = IndiumBot(True)
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
