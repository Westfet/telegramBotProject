@echo off

call %~dp0Telegram_bot\venv\Scripts\activate

cd %~dp0Telegram_bot

set TOKEN=6054239011:AAFKKqH1_LKIodhKxkx-Oax6c2QC9BUGjdA

python app.py

pause