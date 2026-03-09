from datetime import datetime, timedelta, timezone
import config
import database
import sqlite3


def setup_tracker(bot):

    @bot.event
    async def on_message(message):

        if message.author == bot.user:
            return

        if message.channel.id != config.INVITE_CHANNEL_ID:
            await bot.process_commands(message)
            return

        if "invited by" not in message.content:
            await bot.process_commands(message)
            return

        if not message.mentions:
            await bot.process_commands(message)
            return

        try:
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
                print("Failed to parse invite message:", message.content)
                await bot.process_commands(message)
                return

            conn = database.get_connection()
            cursor = conn.cursor()

            # check rejoin
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

            conn.commit()
            conn.close()

            print(
                f"Stored invite | user={joined_user} | inviter={inviter_name} | rejoin={rejoin} | alt={alt}"
            )

        except sqlite3.Error as e:
            print("Database error:", e)

        except Exception as e:
            print("Tracker error:", e)

        await bot.process_commands(message)