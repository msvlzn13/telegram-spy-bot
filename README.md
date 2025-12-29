# 🕵️ Telegram Spyfall Bot

A lightweight Telegram bot to play the popular board game "Spyfall" (or "Spy") with friends without needing physical cards.

## How it works
- **Players:** Receive a card with a location (image).
- **The Spy:** One random player doesn't get the location and must figure it out by listening to others' questions.
- **Discussion:** Everyone asks questions to find the Spy, while the Spy tries to blend in.

## Features
- **Room System:** Create or join private rooms using a 4-digit ID.
- **Real-time Interaction:** Visual feedback on who is ready.
- **Media Support:** Sends random location cards as images for better immersion.
- **Play Again:** Quick lobby reset for consecutive rounds.

## Tech Stack
- **Language:** Python 3.11.4
- **Library:** [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- **Deployment:** Ready for local hosting or Raspberry Pi.

## Setup instructions
1. Clone the repository.
2. Install requirements: `pip install pyTelegramBotAPI`
3. Create a `foto/` folder and add your location images (.jpg, .png).
4. Rename `config_example.py` to `config.py` and add your bot token.
5. Run `python main.py`.
