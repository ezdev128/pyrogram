import time
from string import ascii_lowercase

from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait

"""
This is an improved version of get_participants.py

Since Telegram will return at most 10.000 users for a single query, this script
repeats the search using numbers ("0" to "9") and all the available ascii letters ("a" to "z").

This can be further improved by also searching for non-ascii characters (e.g.: Japanese script),
as some user names may not contain ascii letters at all.
"""

client = Client("example")
client.start()

target = "username"  # Target channel/supergroup username or id
users = {}  # To ensure uniqueness, users will be stored in a dictionary with user_id as key
limit = 200  # Amount of users to retrieve for each API call (200 is the maximum)

# "" + "0123456789" + "abcdefghijklmnopqrstuvwxyz" (as list)
queries = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)

for q in queries:
    print("Searching for '{}'".format(q))
    offset = 0  # For each query, offset restarts from 0

    while True:
        try:
            participants = client.send(
                functions.channels.GetParticipants(
                    channel=client.resolve_peer(target),
                    filter=types.ChannelParticipantsSearch(q),
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )
        except FloodWait as e:
            # Very large chats could trigger FloodWait.
            # When happens, wait X seconds before continuing
            print("Flood wait: {} seconds".format(e.x))
            time.sleep(e.x)
            continue

        if not participants.participants:
            print("Done searching for '{}'".format(q))
            print()
            break  # No more participants left

        # User information are stored in the participants.users list.
        # Add those users to the dictionary
        users.update({i.id: i for i in participants.users})

        offset += len(participants.participants)

        print("Total users: {}".format(len(users)))

client.stop()
