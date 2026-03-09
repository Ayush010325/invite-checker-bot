import database
import sqlite3


def setup_verifier(bot):

    @bot.command()
    async def verifyrange(ctx, inviter_name: str, start: int, end: int):

        try:
            # open connection safely
            conn = database.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT rejoin, alt
                FROM invites
                WHERE inviter_name = ?
                AND invite_number > ?
                AND invite_number <= ?
                """,
                (inviter_name, start, end)
            )

            rows = cursor.fetchall()

            conn.close()

        except sqlite3.Error as e:
            await ctx.send("❌ Database error occurred.")
            print(f"Database error: {e}")
            return

        # no results case
        if not rows:
            await ctx.send("⚠️ No invites found in that range.")
            return

        # calculations
        total = len(rows)
        rejoins = sum(1 for r in rows if r[0] == 1)
        alts = sum(1 for r in rows if r[1] == 1)
        legit = sum(1 for r in rows if r[0] == 0 and r[1] == 0)

        message = f"""
⚽ **Invite Verification**

Inviter: {inviter_name}
Range Checked: {start+1} → {end}

Total Joins Logged: {total}
Rejoins: {rejoins}
Alt Accounts: {alts}

✅ Legit Invites: {legit}
"""

        try:
            await ctx.send(message)
        except Exception as e:
            print(f"Discord send error: {e}")