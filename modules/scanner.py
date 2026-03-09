import config
import database
import sqlite3
import asyncio
from datetime import datetime, timedelta, timezone


def setup_scanner(bot):

    @bot.command()
    async def scan(ctx):

        await ctx.send("Starting invite scan... this may take a while.")

        channel = bot.get_channel(config.INVITE_CHANNEL_ID)

        if channel is None:
            await ctx.send("❌ Invite channel not found.")
            return

        count = 0

        try:
            conn = database.get_connection()
            cursor = conn.cursor()

            async for message in channel.history(limit=None):

                if "invited by" not in message.content:
                    continue

                try:
                    if not message.mentions:
                        continue

                    joined_user = message.mentions[0]
                    user_id = joined_user.id
                    msg_id = message.id

                    # safer parsing
                    try:
                        invite_number = int(
                            message.content.split("has now ")[1].split(" invites")[0]
                        )
                        inviter_name = message.content.split("invited by ")[1].split(" and")[0]
                    except Exception:
                        print("Failed to parse message:", message.content)
                        continue

                    # rejoin detection
                    cursor.execute(
                        "SELECT 1 FROM invites WHERE joined_user_id=?",
                        (user_id,)
                    )

                    existing = cursor.fetchone()
                    rejoin = 1 if existing else 0

                    # alt detection
                    account_age = datetime.now(timezone.utc) - joined_user.created_at
                    alt = 1 if account_age < timedelta(days=90) else 0

                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO invites
                        (message_id, joined_user_id, inviter_name, invite_number, rejoin, alt, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            msg_id,
                            user_id,
                            inviter_name,
                            invite_number,
                            rejoin,
                            alt,
                            str(message.created_at),
                        ),
                    )

                    count += 1

                    # commit every 100 messages (safer for big scans)
                    if count % 100 == 0:
                        conn.commit()
                        print(f"Processed {count} invites...")

                    # tiny delay to avoid rate limits
                    await asyncio.sleep(0.1)

                except Exception as e:
                    print("Message processing error:", e)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            await ctx.send("❌ Database error occurred.")
            print("Database error:", e)
            return

        await ctx.send(f"✅ Scan complete. Processed {count} invite messages.")