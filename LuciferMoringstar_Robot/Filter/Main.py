# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔰 𝖩𝗈𝗂𝗇 𝖴𝗉𝖽𝖺𝗍𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 🔰", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🎬 Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**Uploaded by {message.chat.title}**"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAERhFFhaQSXCzKNIIKARo316F0o6s4gmQACPgMAAs-71A4nKqplyD3cWCEE')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 𝗣𝗔𝗚𝗘𝗦 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝗡𝗘𝗫𝗧 ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 𝗣𝗔𝗚𝗘𝗦 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🎬 Title : {search}**\n**⭐ Rating : {random.choice(RATING)}**\n**🎭 Genre : {random.choice(GENRES)}**\n**Uploaded by {message.chat.title}**"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                file_name = file.file_name
                file_size = get_size(file.file_size)
                file_link = f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}"
                btn.append(
                    [
                      InlineKeyboardButton(text=f"{file_name}", url=f"{file_link}"),
                      InlineKeyboardButton(text=f"{file_size}", url=f"{file_link}")
                    ]
                )
        else:
            LuciferMoringstar=await client.send_message(
            chat_id = message.chat.id,
            text=f"""
<b>👋Hey {message.from_user.mention}</b>

<b>Sorry, No Movie/Series Related to the Given Word Was Found 🥺</b>

<b>Please Go to Google and Confirm the Correct Spelling 🙏</b>

<b>Click Here To 👉 <a href='https://www.google.com'>🔍 Search 🔎</a> </b>

<b>✍Or Your Spelling Is Correct Report To Admins For Add Requested File :- @admins</b>""",
            
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 𝗣𝗔𝗚𝗘𝗦 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="𝗡𝗘𝗫𝗧 ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 𝗣𝗔𝗚𝗘𝗦 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["ʙʏᴛᴇs", "ᴋʙ", "ᴍʙ", "ɢʙ", "ᴛʙ", "ᴘʙ", "ᴇʙ"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝗕𝗔𝗖𝗞", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 𝗣𝗔𝗚𝗘𝗦 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝗕𝗔𝗖𝗞", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("𝗡𝗘𝗫𝗧 ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 𝗣𝗔𝗚𝗘𝗦 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("𝗡𝗘𝗫𝗧 ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 𝗣𝗔𝗚𝗘𝗦 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ 𝗕𝗔𝗖𝗞", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝗡𝗘𝗫𝗧 ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 𝗣𝗔𝗚𝗘𝗦 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('𝖮𝗐𝗇𝖾𝗋', url='t.me/darkz_angel'),
                InlineKeyboardButton('2 𝖮𝗐𝗇𝖾𝗋', url="https://t.me/elon_musk3")
                ],[
                InlineKeyboardButton('𝖢𝗁𝖺𝗇𝗇𝖾𝗅', url='t.me/movies_hub66')
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('𝖮𝗐𝗇𝖾𝗋', url='t.me/darkz_angel'),
                    InlineKeyboardButton('2 𝖮𝗐𝗇𝖾𝗋', url="https://t.me/elon_musk3")
                ]
                ]
            await query.message.edit(text=f"{ABOUT}".format(TUTORIAL), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "eby":
            buttons = [
                [
                    InlineKeyboardButton('𝖠𝗎𝗍𝗈 𝖥𝗂𝗅𝗍𝖾𝗋', callback_data="auto"),
                    InlineKeyboardButton('𝖠𝖻𝗈𝗎𝗍', callback_data="about")
                ],
                [
                    InlineKeyboardButton('𝖡𝖺𝗌𝗂𝖼', callback_data="basic"),
                    InlineKeyboardButton('𝖤𝗑𝗍𝗋𝖺', callback_data="ebm")
                ],
                [
                    InlineKeyboardButton('𝖨𝗇𝖿𝗈', callback_data="info"),
                    InlineKeyboardButton('𝖲𝗈𝗎𝗋𝖼𝖾', callback_data="source")
                ],
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>എന്നെ കൊണ്ട് ചെയ്യാൻ കഴിയുന്ന കുറച്ചു കാര്യങ്ങൾ ആണ് താഴേ കൊടുത്തിട്ടുള്ളത്..</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "auto":
            buttons = [
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="eby"),
                    InlineKeyboardButton('🏘️ 𝖧𝗈𝗆𝖾', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>Help for auto filter\n\nHere Is the available commands in auto filter\n\n• /index -  add a files to data base\n• /channel - get the  connected channels</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "home":
            buttons = [
                [
                    InlineKeyboardButton('➕ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ➕', url= "https://t.me/MH_AUTO_FILTER_5BOT?startgroup=true")
                ],
                [
                    InlineKeyboardButton('🔍 𝖲𝖾𝖺𝗋𝖼𝗁 𝖧𝖾𝗋𝖾', switch_inline_query_current_chat=''),
                    InlineKeyboardButton('updates', url='https://t.me/movieshub_group')
                ],
                [
                    InlineKeyboardButton('🕵️‍♂️ 𝖢𝗋𝖾𝖺𝗍𝗈𝗋', callback_data="dev"),
                    InlineKeyboardButton('ℹ️ 𝖧𝖾𝗅𝗉', callback_data="eby")
                ]
                ]
            await query.message.edit(text="<b>ʏᴏ.. ʏᴏ..🙋 ɪ'ᴍ [sᴏɴɪᴄ](https://t.me/mh_auto_filter_5bot), ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ᴀs ᴀ ᴀᴜᴛᴏ-ғɪʟᴛᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ....\n\nɪᴛs ᴇᴀsʏ ᴛᴏ ᴜsᴇ ᴍᴇ; ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀs ᴀᴅᴍɪɴ, ᴛʜᴀᴛs ᴀʟʟ, ɪ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴍᴏᴠɪᴇs ᴛʜᴇʀᴇ...🤓\n\nᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ [ᴅᴀʀᴋ ᴀɴɢᴇʟ](https://t.me/darkz_angel)</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "ebm":
            buttons = [
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="eby"),
                    InlineKeyboardButton('🏘️ 𝖧𝗈𝗆𝖾', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>ʙᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ\n\n◯ /broadcast ʀᴇᴘʟᴀʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴏʀ ᴍᴇᴅɪᴀ\n\n◯ /total ʜᴏᴡ ᴍᴀɴʏ ғɪʟᴇs ᴀᴅᴅᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ\n\n◯ /logger ɢᴇᴛ ʟᴏɢs\n\n◯ /delete ᴅᴇʟᴇᴛᴇ ғɪʟᴇ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "basic":
            buttons = [
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="eby"),
                    InlineKeyboardButton('🏘️ 𝖧𝗈𝗆𝖾', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>ʙᴀsɪᴄ ᴄᴏᴍᴍᴀɴᴅs\n\n◯ /start : ᴄʜᴇᴄᴋ ɪғ ᴀᴍ ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ\n\n◯ /about : ᴀʙᴏᴜᴛ ᴍᴇ</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "info":
            buttons = [
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="eby"),
                    InlineKeyboardButton('🏘️ 𝖧𝗈𝗆𝖾', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>ᴜsᴇʀ ɪɴғᴏ\n\n◯/info = ɢᴇᴛ ᴜsᴇʀ ɪɴғᴏ</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "dev":
            buttons = [
                [
                    InlineKeyboardButton('1 𝖣𝖾𝗏', url='https://t.me/darkz_angel'),
                    InlineKeyboardButton('2 𝖣𝖾𝗏', url='https://t.me/elon_musk3')
                ],
                [
                    InlineKeyboardButton('«« 𝖡𝖺𝖼𝗄', callback_data="eby"),
                    InlineKeyboardButton('🏘️ 𝖧𝗈𝗆𝖾', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>ᴍʏ ᴅᴇᴠs 👇👇</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('𝖢𝗁𝖺𝗇𝗇𝖾𝗅', url='t.me/movies_hub66')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('𝖢𝗁𝖺𝗇𝗇𝖾𝗅', url='t.me/movies_hub66')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)

