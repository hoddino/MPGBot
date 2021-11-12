
#!/bin/sh

# Get the base directory and switch into it
basedir=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')");
cd "$basedir";

# Make sure the name file exists
if [ ! -f "bot.name" ]
then
    echo "[SETUP] Name file not found! Try running install.sh ...";
    exit;
fi

# Get the name of the bot
read -r name < bot.name;

# Check if the bot is in the process list
if pm2 list | grep "$name" >/dev/null 2>&1
then
    sh restart.sh
else
    # Start the bot
    pm2 start main.py --name "$name" --interpreter python3 --cron '0 3 * * *' --no-autorestart;

    echo "[OK] "$name" started!";
fi
