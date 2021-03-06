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
                            InlineKeyboardButton("π° π©πππ π΄ππ½πΊππΎ π’ππΊπππΎπ π°", url=invite_link.invite_link)
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
        mo_tech_yt = f"**π¬ Title:** {search}\n**β­ Rating:** {random.choice(RATING)}\n**π­ Genre:** {random.choice(GENRES)}\n**Uploaded by {message.chat.title}**"
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
                [InlineKeyboardButton(text="π π£ππππ¦ 1/1",callback_data="pages")]
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
            [InlineKeyboardButton(text="π‘ππ«π§ β©",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"π π£ππππ¦ 1/{data['total']}",callback_data="pages")]
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
        mo_tech_yt = f"**π¬ Title : {search}**\n**β­ Rating : {random.choice(RATING)}**\n**π­ Genre : {random.choice(GENRES)}**\n**Uploaded by {message.chat.title}**"
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
<b>πHey {message.from_user.mention}</b>

<b>Sorry, No Movie/Series Related to the Given Word Was Found π₯Ί</b>

<b>Please Go to Google and Confirm the Correct Spelling π</b>

<b>Click Here To π <a href='https://www.google.com'>π Search π</a> </b>

<b>βOr Your Spelling Is Correct Report To Admins For Add Requested File :- @admins</b>""",
            
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
                [InlineKeyboardButton(text="π π£ππππ¦ 1/1",callback_data="pages")]
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
            [InlineKeyboardButton(text="π‘ππ«π§ β©",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"π π£ππππ¦ 1/{data['total']}",callback_data="pages")]
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

    units = ["ΚΚα΄α΄s", "α΄Κ", "α΄Κ", "Ι’Κ", "α΄Κ", "α΄Κ", "α΄Κ"]
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
                    [InlineKeyboardButton("βͺ ππππ", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"π π£ππππ¦ {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("βͺ ππππ", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("π‘ππ«π§ β©", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"π π£ππππ¦ {int(index)+2}/{data['total']}", callback_data="pages")]
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
                    [InlineKeyboardButton("π‘ππ«π§ β©", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"π π£ππππ¦ {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("βͺ ππππ", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("π‘ππ«π§ β©", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"π π£ππππ¦ {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('π?πππΎπ', url='t.me/darkz_angel'),
                InlineKeyboardButton('2 π?πππΎπ', url="https://t.me/elon_musk3")
                ],[
                InlineKeyboardButton('π’ππΊπππΎπ', url='t.me/movies_hub66')
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('π?πππΎπ', url='t.me/darkz_angel'),
                    InlineKeyboardButton('2 π?πππΎπ', url="https://t.me/elon_musk3")
                ]
                ]
            await query.message.edit(text=f"{ABOUT}".format(TUTORIAL), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "eby":
            buttons = [
                [
                    InlineKeyboardButton('π πππ π₯ππππΎπ', callback_data="auto"),
                    InlineKeyboardButton('π π»πππ', callback_data="about")
                ],
                [
                    InlineKeyboardButton('π‘πΊπππΌ', callback_data="basic"),
                    InlineKeyboardButton('π€ππππΊ', callback_data="ebm")
                ],
                [
                    InlineKeyboardButton('π¨ππΏπ', callback_data="info"),
                    InlineKeyboardButton('π²ππππΌπΎ', callback_data="source")
                ],
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>ΰ΄ΰ΄¨ΰ΅ΰ΄¨ΰ΅ ΰ΄ΰ΅ΰ΄£ΰ΅ΰ΄ΰ΅ ΰ΄ΰ΅ΰ΄―ΰ΅ΰ΄―ΰ΄Ύΰ΅» ΰ΄ΰ΄΄ΰ΄Ώΰ΄―ΰ΅ΰ΄¨ΰ΅ΰ΄¨ ΰ΄ΰ΅ΰ΄±ΰ΄ΰ΅ΰ΄ΰ΅ ΰ΄ΰ΄Ύΰ΄°ΰ΅ΰ΄―ΰ΄ΰ΅ΰ΄ΰ΅Ύ ΰ΄ΰ΄£ΰ΅ ΰ΄€ΰ΄Ύΰ΄΄ΰ΅ ΰ΄ΰ΅ΰ΄ΰ΅ΰ΄€ΰ΅ΰ΄€ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΅ΰ΄³ΰ΅ΰ΄³ΰ΄€ΰ΅..</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "auto":
            buttons = [
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="eby"),
                    InlineKeyboardButton('ποΈ π§πππΎ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>Help for auto filter\n\nHere Is the available commands in auto filter\n\nβ’ /index -  add a files to data base\nβ’ /channel - get the  connected channels</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "home":
            buttons = [
                [
                    InlineKeyboardButton('β π π½π½ π¬πΎ π³π πΈπππ π¦ππππ β', url= "https://t.me/MH_AUTO_FILTER_5BOT?startgroup=true")
                ],
                [
                    InlineKeyboardButton('π π²πΎπΊππΌπ π§πΎππΎ', switch_inline_query_current_chat=''),
                    InlineKeyboardButton('updates', url='https://t.me/movieshub_group')
                ],
                [
                    InlineKeyboardButton('π΅οΈββοΈ π’ππΎπΊπππ', callback_data="dev"),
                    InlineKeyboardButton('βΉοΈ π§πΎππ', callback_data="eby")
                ]
                ]
            await query.message.edit(text="<b>Κα΄.. Κα΄..π Ιͺ'α΄ [α΄ΙͺΚα΄s](https://t.me/movie_2robot), Κα΄α΄ α΄α΄Ι΄ α΄sα΄ α΄α΄ α΄s α΄ α΄α΄α΄α΄-?ΙͺΚα΄α΄Κ ΙͺΙ΄ Κα΄α΄Κ Ι’Κα΄α΄α΄ ....\n\nΙͺα΄s α΄α΄sΚ α΄α΄ α΄sα΄ α΄α΄; α΄α΄sα΄ α΄α΄α΄ α΄α΄ α΄α΄ Κα΄α΄Κ Ι’Κα΄α΄α΄ α΄s α΄α΄α΄ΙͺΙ΄, α΄Κα΄α΄s α΄ΚΚ, Ιͺ α΄‘ΙͺΚΚ α΄Κα΄α΄ Ιͺα΄α΄ α΄α΄α΄ Ιͺα΄s α΄Κα΄Κα΄...π€\n\nα΄α΄ΙͺΙ΄α΄α΄ΙͺΙ΄α΄α΄ ΚΚ [α΄α΄Κα΄ α΄Ι΄Ι’α΄Κ](https://t.me/darkz_angel)</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "ebm":
            buttons = [
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="eby"),
                    InlineKeyboardButton('ποΈ π§πππΎ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>Κα΄α΄ α΄α΄‘Ι΄α΄Κ α΄Ι΄ΚΚ\n\nβ― /broadcast Κα΄α΄Κα΄Κ α΄Ι΄Κ α΄α΄ssα΄Ι’α΄ α΄Κ α΄α΄α΄Ιͺα΄\n\nβ― /total Κα΄α΄‘ α΄α΄Ι΄Κ ?ΙͺΚα΄s α΄α΄α΄α΄α΄ ΙͺΙ΄ α΄α΄α΄α΄Κα΄sα΄\n\nβ― /logger Ι’α΄α΄ Κα΄Ι’s\n\nβ― /delete α΄α΄Κα΄α΄α΄ ?ΙͺΚα΄ ?Κα΄α΄ α΄α΄α΄α΄Κα΄sα΄</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "basic":
            buttons = [
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="eby"),
                    InlineKeyboardButton('ποΈ π§πππΎ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>Κα΄sΙͺα΄ α΄α΄α΄α΄α΄Ι΄α΄s\n\nβ― /start : α΄Κα΄α΄α΄ Ιͺ? α΄α΄ α΄ΚΙͺα΄ α΄ α΄Κ α΄α΄α΄α΄\n\nβ― /about : α΄Κα΄α΄α΄ α΄α΄</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "info":
            buttons = [
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="eby"),
                    InlineKeyboardButton('ποΈ π§πππΎ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>α΄sα΄Κ ΙͺΙ΄?α΄\n\nβ―/info = Ι’α΄α΄ α΄sα΄Κ ΙͺΙ΄?α΄</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "dev":
            buttons = [
                [
                    InlineKeyboardButton('1 π£πΎπ', url='https://t.me/darkz_angel'),
                    InlineKeyboardButton('2 π£πΎπ', url='https://t.me/elon_musk3')
                ],
                [
                    InlineKeyboardButton('Β«Β« π‘πΊπΌπ', callback_data="home")
                ]
                ]
            await query.message.edit(text="<b>α΄Κ α΄α΄α΄ s ππ</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

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
                        InlineKeyboardButton('π’ππΊπππΎπ', url='t.me/movies_hub66')
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
                await query.answer("I Like Your Smartness, But Don't Be Oversmart π",show_alert=True)
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
                        InlineKeyboardButton('π’ππΊπππΎπ', url='t.me/movies_hub66')
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
            await query.answer("ΰ΄ΰ΅ΰ΄€ΰ΅ΰ΄ΰ΅ΰ΄ ΰ΄²ΰ΅ΰ΄Άΰ΄ ΰ΄ΰ΅ΰ΄ΰ΅ΰ΄€ΰ΅½ ΰ΄ΰ΄£ΰ΄²ΰ΅ΰ΄²ΰ΅π",show_alert=True)

        elif query.data == "source":
            await query.answer("ΰ΄Ήΰ΄Ύΰ΄―ΰ΅ ΰ΄ΰ΄¨ΰ΅ΰ΄€ΰ΄Ύ ΰ΄Έΰ΅ΰ΄΄ΰ΅ΰ΄Έΰ΅ ΰ΄ΰ΅ΰ΄‘ΰ΅ ΰ΄΅ΰ΅ΰ΄£ΰ΅ ΰ΄ΰ΄ͺΰ΅ΰ΄ͺΰ΅ ΰ΄ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΅ΰ΄ ΰ΄΅ΰ΅ΰ΄―ΰ΄Ώΰ΄±ΰ΅ΰ΄±ΰ΅ ΰ΄ΰ΅ΰ΄―ΰ΅ ΰ΄ΰ΄¨ΰ΅ΰ΄€ΰ΅ ΰ΄ΰ΄€ΰ΅ΰ΄΅ΰ΄°ΰ΅ ΰ΄ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΄Ώΰ΄―ΰ΄Ώΰ΄²ΰ΅ΰ΄²ΰ΅ ΰ΄ΰ΄¨ΰ΅ΰ΄¨ ΰ΄ͺΰ΅ΰ΄ΰ΅ΰ΄ΰ΅ π",show_alert=True)
