#! /usr/bin/env python3

from Config.config import BOT_TOKEN
from Utils.core.better_bot import IndiumBot


def main():
    client = IndiumBot(True)
    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
