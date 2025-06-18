<h1 align="center">
    ──「 TheTechSavage File Store Bot 」──
</h1>

<p align="center">
  <img src="https://graph.org/file/8581e33195ed8183a3253.jpg">
</p>

A powerful and customizable Telegram bot to store files in a private channel and share them via special links. Built with Pyrogram and MongoDB, and designed for easy deployment and management.

---
## ✨ FEATURES
---

- Dynamic Customization: Admins can change the bot's welcome message, picture, about/help text, and buttons directly from the Telegram interface using simple commands.
- Persistent & Reliable: Deploys as a `systemd` service, ensuring the bot is always online and automatically restarts on crash or server reboot.
- Multi-Channel Force Subscribe: Require users to join one or more channels before they can use the bot.
- Link Generation: Supports batch, custom batch, and single-file link generation.
- Admin & User Management: Full control over bot admins and the ability to ban/unban users.
- And more... Broadcasts, auto-deleting files, bot stats, etc.

---
## 🚀 DEPLOYMENT GUIDE
---

This guide will walk you through deploying the bot on a standard Ubuntu server.

### 1. PREREQUISITES

Before you begin, ensure your server has the following installed:
- Ubuntu Server (22.04 or later is recommended).
- `git`, `python3.10` or higher, and `python3-pip`.

You can install them with this command:
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip -y


### 2. INSTALLATION STEPS

1. Clone the Repository
Log into your server via SSH and clone this repository.
git clone https://github.com/thetechsavage96/FileStore.git
cd FileStore

2. Install Python Dependencies
Install all the required Python libraries using the `requirements.txt` file.
pip3 install -r requirements.txt

3. Configure Environment Variables
Create your personal configuration file by copying the provided example template.
cp .env.example .env

Now, edit the new .env` file with your own credentials and settings.
nano .env

Fill in all the required variables listed in the file. Save your changes by pressing Ctrl+X, then Y, then Enter.

### 3. RUNNING THE BOT (PRODUCTION METHOD)

We will use `systemd` to run the bot as a persistent background service. This is the most reliable method.

1. Create the Service File
Use the `nano` editor to create a service configuration file.
sudo nano /etc/systemd/system/filestore-bot.service

2. Paste the Service Configuration
Copy the entire block below and paste it into the editor.

IMPORTANT: You MUST replace `<your_username>` with your actual username on the server (e.g., `root`, `ubuntu`) and `/path/to/your/FileStore` with the correct full path (e.g., `/home/dondcoder/FileStore`).

--- START OF SERVICE FILE CONTENT ---
[Unit]
Description=FileStore Telegram Bot
After=network.target

[Service]
User=<your_username>
WorkingDirectory=/path/to/your/FileStore
ExecStart=/usr/bin/python3 /path/to/your/FileStore/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
--- END OF SERVICE FILE CONTENT ---

Save and exit the file (Ctrl+X, Y, Enter).

3. Start and Enable the Service
Run these commands to start your bot and enable it to launch automatically every time the server boots.
sudo systemctl daemon-reload
sudo systemctl enable filestore-bot.service
sudo systemctl start filestore-bot.service

4. Check the Status
Verify that the bot is running correctly.
sudo systemctl status filestore-bot.service

You should see a green `active (running)` message. You can press Q to exit the status screen. Your bot is now live!

### 4. BOT USAGE & CUSTOMIZATION

- Go to your bot on Telegram and send `/start`.
- As the bot owner/admin, send the `/commands` command to see a full list of all management and customization commands.
- You can now customize the bot's appearance by using commands like `/set_start_text`, `/set_start_pic`, etc., directly in your chat with the bot.

---
### CREDITS
---
- [Codeflix Bots](https://t.me/codeflix_bots)
- TheTechSavage
