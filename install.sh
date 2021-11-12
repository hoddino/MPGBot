
#!/bin/sh

# Get the base directory and switch into it
basedir=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')");
cd "$basedir";

# Install package dependencies
echo "[SETUP] Installing package dependencies ...";
pip3 install -r requirements.txt;

# Check if the bot already has a name
if [ ! -f "bot.name" ]
then
    # Name of the bot
    echo "";
    echo "In case you want to run more than one bot, you need to enter a unique name for each!";
    echo "If you are already running a different bot, make sure you give this one another name!";
    echo "";
    echo -n "How do you want to call this bot: ";
    read -r name;

    # Make sure the name is valid
    while [ ! ${#name} -ge 1 ]
    do
        echo "Name invalid, try again: ";
        read -r name;
    done

    # Safe the name in a file
    echo "[SETUP] Saving name ...";
    echo "$name" > bot.name;
fi

echo "[SETUP] Done!";
