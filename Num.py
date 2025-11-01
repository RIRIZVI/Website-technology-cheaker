# check_telegram.py
import asyncio
import sys
from telethon import TelegramClient, functions, types
from telethon.errors import FloodWaitError, SessionPasswordNeededError, RPCError

# ==== CONFIGURE THESE ====
API_ID = 28901087        # আপনার api_id
API_HASH = '324596247754d4146da74750877344ce'  # আপনার api_hash
SESSION_NAME = 'my_session'      # session ফাইলের নাম (অপশনাল)
# ==========================

async def check_number(target_phone, login_phone=None):
    """
    target_phone: string, like '+8801xxxxxxxxx'
    login_phone: optional — ফোনটি যেই নম্বরে টেলিগ্রামে লগইন হবে (আপনি সাধারণত নিজের নম্বর দেবেন)
    """
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start(phone=login_phone)  # যদি প্রথমবার হয়, কোড পাঠাবে এবং আপনি কনসোলে প্রবেশ করাবেন
    except SessionPasswordNeededError:
        print("Two-step verification is enabled. Provide your password when prompted by Telethon.")
        await client.connect()
    except Exception as e:
        print("Login/start error:", e)
        return

    try:
        # Create a temporary InputPhoneContact
        contact = types.InputPhoneContact(client_id=0, phone=target_phone, first_name='Temp', last_name='')

        # Import contact
        res = await client(functions.contacts.ImportContactsRequest([contact]))

        # res.users contains matching users (if any)
        if res.users and len(res.users) > 0:
            user = res.users[0]
            uname = getattr(user, 'username', None)
            print(f"[FOUND] {target_phone} is registered on Telegram.")
            print(f"  user_id: {user.id}")
            print(f"  first_name: {user.first_name}")
            print(f"  last_name: {user.last_name}")
            print(f"  username: {uname}")
            # Remove the temporary contact to clean up
            try:
                input_ent = await client.get_input_entity(user)
                await client(functions.contacts.DeleteContactsRequest(id=[input_ent]))
            except Exception:
                # best-effort delete; ignore if fails
                pass
        else:
            print(f"[NOT FOUND] {target_phone} does NOT appear to be registered on Telegram.")
    except FloodWaitError as fw:
        print(f"Flood wait: need to wait {fw.seconds} seconds. Try later.")
    except RPCError as err:
        print("Telegram RPC error:", err)
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        await client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_telegram.py +8801xxxxxxxxx [your_login_phone_optional]")
        sys.exit(1)

    target = sys.argv[1]
    login = sys.argv[2] if len(sys.argv) >= 3 else None

    asyncio.run(check_number(target, login))