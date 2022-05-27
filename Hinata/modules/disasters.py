import html
import json
import os
from typing import Optional

from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

from Hinata import (
    HOKAGE_ID,
    GENINS,
    ACADEMY_USERS,
    NARUTO_ID,
    JONINS,
    CHUNINS,
    dispatcher,
)
from Hinata.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from Hinata.modules.helper_funcs.extraction import extract_user
from Hinata.modules.log_channel import gloggable

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "Hinata/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# radars =
# """ Text here """

# do not async, not a handler
# def send_radars(update):
#    update.effective_message.reply_text(
#        radars, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in JONINS:
        message.reply_text("This member is already a RedLion Disaster")
        return ""

    if user_id in CHUNINS:
        rt += "Requested HA to promote a Spryzon Disaster to RedLion."
        data["supports"].remove(user_id)
        CHUNINS.remove(user_id)

    if user_id in ACADEMY_USERS:
        rt += "Requested HA to promote a Luinor Disaster to RedLion."
        data["whitelists"].remove(user_id)
        ACADEMY_USERS.remove(user_id)

    data["sudos"].append(user_id)
    JONINS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully set Disaster level of {} to RedLion!".format(
            user_member.first_name
        )
    )

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in JONINS:
        rt += "Requested HA to demote this RedLion to Spryzon"
        data["sudos"].remove(user_id)
        JONINS.remove(user_id)

    if user_id in CHUNINS:
        message.reply_text("This user is already a Spryzon Disaster.")
        return ""

    if user_id in ACADEMY_USERS:
        rt += "Requested HA to promote this Luinor Disaster to Spryzon"
        data["whitelists"].remove(user_id)
        ACADEMY_USERS.remove(user_id)

    data["supports"].append(user_id)
    CHUNINS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a Spryzon Disaster!"
    )

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in JONINS:
        rt += "This member is a RedLion Disaster, Demoting to Luinor."
        data["sudos"].remove(user_id)
        JONINS.remove(user_id)

    if user_id in CHUNINS:
        rt += "This user is already a Spryzon Disaster, Demoting to Luinor."
        data["supports"].remove(user_id)
        CHUNINS.remove(user_id)

    if user_id in ACADEMY_USERS:
        message.reply_text("This user is already a Luinor Disaster.")
        return ""

    data["whitelists"].append(user_id)
    ACADEMY_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Luinor Disaster!"
    )

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@sudo_plus
@gloggable
def addgenin(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in JONINS:
        rt += "This member is a RedLion Disaster, Demoting to genin."
        data["sudos"].remove(user_id)
        JONINS.remove(user_id)

    if user_id in CHUNINS:
        rt += "This user is already a Spryzon Disaster, Demoting to genin."
        data["supports"].remove(user_id)
        CHUNINS.remove(user_id)

    if user_id in ACADEMY_USERS:
        rt += "This user is already a Luinor Disaster, Demoting to genin."
        data["whitelists"].remove(user_id)
        ACADEMY_USERS.remove(user_id)

    if user_id in GENINS:
        message.reply_text("This user is already a genin.")
        return ""

    data["GENINS"].append(user_id)
    GENINS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a genin Disaster!"
    )

    log_message = (
        f"#genin\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in JONINS:
        message.reply_text("Requested HA to demote this user to Civilian")
        JONINS.remove(user_id)
        data["sudos"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a RedLion Disaster!")
        return ""


@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in CHUNINS:
        message.reply_text("Requested HA to demote this user to Civilian")
        CHUNINS.remove(user_id)
        data["supports"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Spryzon level Disaster!")
        return ""


@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in ACADEMY_USERS:
        message.reply_text("Demoting to normal user")
        ACADEMY_USERS.remove(user_id)
        data["whitelists"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Luinor Disaster!")
        return ""


@sudo_plus
@gloggable
def removegenin(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in GENINS:
        message.reply_text("Demoting to normal user")
        GENINS.remove(user_id)
        data["GENINS"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNgenin\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a genin Disaster!")
        return ""


@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Known Luinor radars 🐺:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering ACADEMY_USERS..</code>", parse_mode=ParseMode.HTML
    )
    bot = context.bot
    for each_user in ACADEMY_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def geninlist(update: Update, context: CallbackContext):
    reply = "<b>Known genin radars 🐯:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering GENINS..</code>", parse_mode=ParseMode.HTML
    )
    bot = context.bot
    for each_user in GENINS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering CHUNINS..</code>", parse_mode=ParseMode.HTML
    )
    reply = "<b>Known Spryzon radars 👹:</b>\n"
    for each_user in CHUNINS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering JONINS..</code>", parse_mode=ParseMode.HTML
    )
    true_sudo = list(set(JONINS) - set(HOKAGE_ID))
    reply = "<b>Known RedLion radars 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering Devs..</code>", parse_mode=ParseMode.HTML
    )
    true_dev = list(set(HOKAGE_ID) - {NARUTO_ID})
    reply = "<b>Hero Association Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


# __help__ = f"""
# *⚠️ Notice:*
# Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
# Group admins/group owners do not need these commands.
#
# *List all special users:*
# ❍ /JONINS*:* Lists all RedLion radars
# ❍ /spryzon*:* Lists all Spryzon radars
# ❍ /GENINS*:* Lists all GENINS radars
# ❍ /ACADEMY_USERS*:* Lists all Luinor radars
# ❍ /heroes*:* Lists all Hero Association members
# ❍ /addredlion*:* Adds a user to RedLion
# ❍ /addspryzon*:* Adds a user to Spryzon
# ❍ /addgenin*:* Adds a user to genin
# ❍ /addluinor*:* Adds a user to Luinor
# ❍ `Add dev doesnt exist, devs should know how to add themselves`
#
# *Ping:*
# ❍ /ping*:* gets ping time of bot to telegram server
# ❍ /pingall*:* gets all listed ping times
#
# *Broadcast: (Bot owner only)*
# *Note:* This supports basic markdown
# ❍ /broadcastall*:* Broadcasts everywhere
# ❍ /broadcastusers*:* Broadcasts too all users
# ❍ /broadcastgroups*:* Broadcasts too all groups
#
# *Groups Info:*
# ❍ /groups*:* List the groups with Name, ID, members count as a txt
# ❍ /leave <ID>*:* Leave the group, ID must have hyphen
# ❍ /stats*:* Shows overall bot stats
# ❍ /getchats*:* Gets a list of group names the user has been seen in. Bot owner only
# ❍ /ginfo username/link/ID*:* Pulls info panel for entire group
#
# *Access control:*
# ❍ /ignore*:* Blacklists a user from using the bot entirely
# ❍ /lockdown <off/on>*:* Toggles bot adding to groups
# ❍ /notice*:* Removes user from blacklist
# ❍ /ignoredlist*:* Lists ignored users

# *Speedtest:*
# ❍ /speedtest*:* Runs a speedtest and gives you 2 options to choose from, text or image output
#
# *Module loading:*
# ❍ /listmodules*:* Lists names of all modules
# ❍ /load modulename*:* Loads the said module to memory without restarting.
# ❍ /unload modulename*:* Loads the said module frommemory without restarting memory without restarting the bot
#
# *Windows self hosted only:*
# ❍ /reboot*:* Restarts the bots service
# ❍ /gitpull*:* Pulls the repo and then restarts the bots service
#
# *Debugging and Shell:*
# ❍ /debug <on/off>*:* Logs commands to updates.txt
# ❍ /logs*:* Run this in support group to get logs in pm
# ❍ /eval*:* Self explanatory
# ❍ /sh*:* Runs shell command
# ❍ /shell*:* Runs shell command
# ❍ /clearlocals*:* As the name goes
# ❍ /dbcleanup*:* Removes deleted accs and groups from db
# ❍ /py*:* Runs python code
#
# *Heroku Settings*
# *Owner only*
# ❍ /usage*:* Check your heroku dyno hours remaining.
# ❍ /see var <var>*:* Get your existing varibles, use it only on your private group!
# ❍ /set var <newvar> <vavariable>*:* Add new variable or update existing value variable.
# ❍ /del var <var>*:* Delete existing variable.
# ❍ /logs Get heroku dyno logs.
#
# `⚠️ Read from top`
# Visit @{SUPPORT_CHAT} for more information.
# """

SUDO_HANDLER = CommandHandler(("addsudo", "addredlion"), addsudo, run_async=True)
SUPPORT_HANDLER = CommandHandler(
    ("addsupport", "addspryzon"), addsupport, run_async=True
)
genin_HANDLER = CommandHandler(("addgenin"), addgenin, run_async=True)
WHITELIST_HANDLER = CommandHandler(
    ("addwhitelist", "addluinor"), addwhitelist, run_async=True
)
UNSUDO_HANDLER = CommandHandler(
    ("removesudo", "removeredlion"), removesudo, run_async=True
)
UNSUPPORT_HANDLER = CommandHandler(
    ("removesupport", "removespryzon"), removesupport, run_async=True
)
UNgenin_HANDLER = CommandHandler(("removegenin"), removegenin, run_async=True)
UNWHITELIST_HANDLER = CommandHandler(
    ("removewhitelist", "removeluinor"), removewhitelist, run_async=True
)

WHITELISTLIST_HANDLER = CommandHandler(
    ["whitelistlist", "ACADEMY_USERS"], whitelistlist, run_async=True
)
geninLIST_HANDLER = CommandHandler(["GENINS"], geninlist, run_async=True)
SUPPORTLIST_HANDLER = CommandHandler(
    ["supportlist", "spryzon"], supportlist, run_async=True
)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "JONINS"], sudolist, run_async=True)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes"], devlist, run_async=True)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(genin_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNgenin_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(geninLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [
    SUDO_HANDLER,
    SUPPORT_HANDLER,
    genin_HANDLER,
    WHITELIST_HANDLER,
    UNSUDO_HANDLER,
    UNSUPPORT_HANDLER,
    UNgenin_HANDLER,
    UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER,
    geninLIST_HANDLER,
    SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER,
]
