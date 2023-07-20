from keys import *
import telebot
API_KEY = TELEGRAM_KEY_PRIMARY
bot = telebot.TeleBot(API_KEY, parse_mode=None)

from utils import *
def delete_command(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

from chatbot import ai_response

from news import FetchNews
fetch_news = FetchNews()

@bot.edited_message_handler(commands=['news'])
@bot.message_handler(commands=['news'])
def help(msg):
    chat_id = msg.chat.id
    msg_id = msg.id
    crud.check_chat_entry(chat_id)
    message = fetch_news.news()
    prev_msg_id = bot.send_message(chat_id, message).message_id
    type = 'apis'
    prev_msg_id_fnc = crud.data[str(chat_id)]['last_message_id'][type]
    if prev_msg_id_fnc != None:
        try:
            bot.delete_message(chat_id, prev_msg_id_fnc)
            crud.data[str(chat_id)]['last_message_id'][type] = None
        except:
            pass
    delete_command(chat_id, msg_id)
    crud.data[str(chat_id)]['last_message_id'][type] = prev_msg_id
    crud.save()

from api import ReputationSystem
crud = ReputationSystem(bot)

@bot.message_handler(commands=['create'])
def create(msg):
    chat_id = msg.chat.id
    text = msg.text[8:]
    message = crud.Create(text)
    bot.send_message(chat_id, message)

@bot.message_handler(commands=['read'])
def read(msg):
    chat_id = msg.chat.id
    text = msg.text[6:]
    message = crud.Read(text)
    bot.send_message(chat_id, message)

@bot.message_handler(commands=['update'])
def update(msg):
    chat_id = msg.chat.id
    text = msg.text
    lst = text[8:].split("<>")
    a = lst[0]
    b = lst[1]
    message = crud.Update(a, b)
    bot.send_message(chat_id, message)

@bot.message_handler(commands=['delete'])
def delete(msg):
    chat_id = msg.chat.id
    text = msg.text[8:]
    message = crud.Delete(text)
    bot.send_message(chat_id, message)

''' here start the bot '''

@bot.edited_message_handler(commands=['startbot'])
@bot.message_handler(commands=['startbot'])
def send_help_message(msg):

    if msg.from_user.id in crud.data['special_members']:
        chat_id = msg.chat.id
        msg_id = msg.id

        if chat_id in crud.data['available_chats']:
            prev_msg_id = bot.send_message(chat_id, "already working for this group").message_id
        else:
            crud.data['available_chats'].append(chat_id)
            crud.check_chat_entry(chat_id)
            prev_msg_id = bot.send_message(chat_id, "started working for this group").message_id

        delete_command(chat_id, msg_id)

        prev_msg_id_fnc = crud.data[chat_id]['last_message_id']['super']
        if prev_msg_id_fnc != None:
            try:
                bot.delete_message(chat_id, prev_msg_id_fnc)
                crud.data[chat_id]['last_message_id']['super'] = None
            except:
                pass
        crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
    crud.save()



@bot.edited_message_handler(commands=['help'])
@bot.message_handler(commands=['help'])
def help(msg):
    chat_id = msg.chat.id
    msg_id = msg.id
    crud.check_chat_entry(chat_id)
    message = "<COMMANDS>\n\n(FOR ALL MEMBERS) \n/me : to see your information. \n/levels : to see level. \n/toplvl : to see users with top levels. \n/toprep : to see users with top reps.\n\n(FOR ADMINS)\n/addlvl level_name level_points : to add a new level.\n/rmvlvl level_name : to remove a level.\n\n(REPLIED MESSAGES)\n/status : to see user information.\n/setrank nick_name : to set a custom nickname.\n/unsetrank : to remove custom nickname.\nw or W or 😼 : to increase rep.\nl or L or 💀 : to decrease rep."
    prev_msg_id = bot.send_message(chat_id, message).message_id
    type = 'super'
    prev_msg_id_fnc = crud.data[chat_id]['last_message_id'][type]
    if prev_msg_id_fnc != None:
        try:
            bot.delete_message(chat_id, prev_msg_id_fnc)
            crud.data[chat_id]['last_message_id'][type] = None
        except:
            pass
    delete_command(chat_id, msg_id)
    crud.data[chat_id]['last_message_id'][type] = prev_msg_id
    crud.save()



# FUNCTION FOR TEXT COMMANDS IN A GROUP CHAT OR A CHANNEL
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def commands(msg):

    try:

        chat_id = msg.chat.id
        msg_id = msg.id
        text = msg.text
        from_member = bot.get_chat_member(chat_id, msg.from_user.id)

        if len(msg.text) < 50 and from_member.user.is_bot == False:

            if text == SUPER_USER_COMMAND:
                if msg.from_user.id not in crud.data['special_members']:
                    crud.data['special_members'].append(msg.from_user.id)
                    crud.save()
                    bot.send_message(chat_id, "you are a superuser now")
                    delete_command(chat_id, msg_id)
                else:
                    bot.send_message(chat_id, "you are a superuser already")
                    delete_command(chat_id, msg_id)

            if len(msg.text) < 50 and chat_id in crud.data['available_chats']:

                # INITIALIZING VARIABLES
                from_hyper_name = getHyperLink(from_member.user.id, from_member.user.first_name)
                text_len = len(text)
                # chat_member_count = bot.get_chat_member_count(chat_id)
                crud.check_chat_entry(chat_id)
                crud.check_entry(from_member.user.id, chat_id)

                # SUPERUSER
                superuser = False
                if from_member.user.id in crud.data['special_members']:
                    superuser = True

                # deleting previous message of bot
                def del_msg(type):
                    prev_msg_id_fnc = crud.data[chat_id]['last_message_id'][type]
                    if prev_msg_id_fnc != None:
                        try:
                            bot.delete_message(chat_id, prev_msg_id_fnc)
                            crud.data[chat_id]['last_message_id'][type] = None
                        except:
                            pass
                    crud.save()

                # INCREASING LEVEL OF A USER
                s = str(text)
                pt = len(s.split())
                crud.change_lvl(from_member.user.id, pt, chat_id)


                # CHECKING THE TEXT LENGHT
                if text_len < 40:
                    lst = text.split()
                    lst_len = len(lst)

                    # STARING UP
                    start = True
                    # start = crud.data['']
                    if start:

                        # COMMANDS ACSESABLE TO ALL MEMBERS
                        if text == '/levels':
                            message = crud.show_levels(chat_id)
                            prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                            del_msg('levels')
                            delete_command(chat_id, msg_id)
                            crud.data[chat_id]['last_message_id']['levels'] = prev_msg_id
                            return

                        elif text == "/me":

                            from_hyper_name = getHyperLink(from_member.user.id, from_member.user.first_name)
                            lst = crud.show_level(from_member.user.id, chat_id)
                            rank = crud.getRankTitle(from_member.user.id, chat_id)
                            message = f"{bold(from_hyper_name)} [ {bold(rank)} ]\n{bold('Reputation:')} {bold(a(chat_id, crud.read_rep(from_member.user.id, chat_id)))}\n{bold('Level:')} {bold(a(chat_id, lst[2]))} [{a(chat_id, crud.read_lvl(from_member.user.id, chat_id))}/{a(chat_id, lst[1])}]"
                            prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                            delete_command(chat_id, msg_id)
                            del_msg("me")
                            crud.data[chat_id]['last_message_id']['me'] = prev_msg_id
                            return

                        if lst[0] == "/toplvl":
                            if lst_len==2:
                                c = int(lst[1])
                            else:
                                c = 10
                            message = "<b>TOP-LEVELS</b>: 😼\n"
                            for obj in crud.toplvl(chat_id, c):
                                user = bot.get_chat_member(chat_id=chat_id, user_id=obj['id']).user
                                username = getHyperLink(user.id, user.first_name)
                                message = message + f"{a(chat_id, obj['curr_lvl'])} {bold(obj['lvl_name'])} {bold(username)} [{a(chat_id, obj['lvl'])}/{a(chat_id, obj['nxt_lvl_pt'])}]\n"
                            prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                            delete_command(chat_id, msg_id)
                            del_msg('toplvl')
                            crud.data[chat_id]['last_message_id']['toplvl'] = prev_msg_id
                            return

                        elif lst[0] == "/toprep":
                            if lst_len==2:
                                c = int(lst[1])
                            else:
                                c = 10
                            message = "<b>TOP-REPS</b>: 😼\n"
                            for obj in crud.toprep(chat_id, c):
                                user = bot.get_chat_member(chat_id=chat_id, user_id=obj['id']).user
                                username = getHyperLink(user.id, user.first_name)
                                message = message + f"{a(chat_id, obj['rep'])} {bold(obj['title'])} {bold(username)}\n"
                            prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                            delete_command(chat_id, msg_id)
                            del_msg('toprep')
                            crud.data[chat_id]['last_message_id']['toprep'] = prev_msg_id
                            return

                        # NON-REPLY COMMMANDS FOR ADMINS
                        if (crud.data[chat_id]['members'][from_member.user.id]) and (from_member.status == "administrator" or from_member.status == "creator" or superuser):
                            lst = text.split()

                            if len(text.split()) > 0:

                                if lst[0] == '/addlvl':
                                    try:
                                        lvl_pt = int(lst.pop())
                                    except:
                                        message = f" {from_hyper_name}  enter valid points with new level"
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        delete_command(chat_id, msg_id)
                                        del_msg('addlvl')
                                        crud.data[chat_id]['last_message_id']['addlvl'] = prev_msg_id
                                        return
                                    lst.pop(0)
                                    new_lvl = remove_unsupported_letter(' '.join(lst))
                                    if new_lvl not in crud.data[chat_id]['levels'].keys():
                                        lvl_name = str(new_lvl)
                                        crud.add_level(lvl_name, lvl_pt, chat_id)
                                        message = f"{from_hyper_name} has added a new Level {bold(lvl_name)} [{a(chat_id, lvl_pt)}]"
                                    else:
                                        message = f" {from_hyper_name} level already exist"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg("addlvl")
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['addlvl'] = prev_msg_id
                                    crud.save()
                                    return

                                if lst[0] == '/rmvlvl':
                                    lst.pop(0)
                                    new_lvl = ' '.join(lst)
                                    if new_lvl in crud.data[chat_id]['levels'].keys():
                                        lvl_name = new_lvl
                                        crud.del_level(lvl_name, chat_id)
                                        message = f"You have deleted level {bold(lvl_name)}"
                                    else:
                                        message = f" {from_hyper_name}  level does not exit"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg("rmvlvl")
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['rmvlvl'] = prev_msg_id
                                    crud.save()
                                    return

                        # COMMANDS FOR REPLIED MESSAGES
                        if msg.reply_to_message != None:
                            to_member = bot.get_chat_member(chat_id, msg.reply_to_message.from_user.id)

                            # print(to_member.user.id)
                            if to_member.user.id==PRIMARY_BOT_ID:
                                # bot.reply_to(msg, "lol")
                                bot.reply_to(msg, ai_response(text))

                            crud.check_entry(to_member.user.id, chat_id)

                            # SUPERUSER COMMANDS
                            if superuser:
                                if lst[0] == '/superrank':
                                    lst.pop(0)
                                    new_rank = remove_unsupported_letter(' '.join(lst))
                                    if True:
                                        username = getHyperLink(to_member.user.id, to_member.user.first_name)
                                        crud.data[chat_id]['members'][to_member.user.id]['special_commands']['rank'] = new_rank
                                        message = f"A superuser has set rank [{bold(new_rank)}] for {bold(username)}"
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('super')
                                        delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
                                    return

                                elif lst[0] == '/superranknull':
                                    username = getHyperLink(to_member.user.id, to_member.user.first_name)
                                    crud.data[chat_id]['members'][to_member.user.id]['special_commands']['rank'] = None
                                    message = f"A superuser has unset rank for {bold(username)}"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg('super')
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
                                    return

                                elif lst[0] == '/superrep':
                                    username = getHyperLink(to_member.user.id, to_member.user.first_name)
                                    crud.change_rep(to_member.user.id, lst[1], chat_id)
                                    message = f"A superuser has changed rep by [{a(chat_id, lst[1])}] for {bold(username)}"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg('super')
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
                                    crud.save()
                                    return

                                elif lst[0] == '/superlvl':
                                    username = getHyperLink(to_member.user.id, to_member.user.first_name)
                                    crud.change_lvl(to_member.user.id, lst[1], chat_id)
                                    message = f"A superuser has changed level by [{a(chat_id, lst[1])}] for {bold(username)}"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg('super')
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
                                    crud.save()
                                    return

                                elif text == '/changerights':
                                    username = getHyperLink(to_member.user.id, to_member.user.first_name)
                                    status = crud.data[chat_id]['members'][to_member.user.id]['special_commands']['admin']
                                    crud.data[chat_id]['members'][to_member.user.id]['special_commands']['admin'] = not status
                                    message = f"A superuser has changed rights for {bold(username)}"
                                    prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                    del_msg('super')
                                    delete_command(chat_id, msg_id)
                                    crud.data[chat_id]['last_message_id']['super'] = prev_msg_id
                                    crud.save()
                                    return



                            # CHECK USER ID ARE NOT EQUAL AND NO BOTS
                            if to_member.user.id != from_member.user.id and to_member.user.is_bot==False:

                                # Setting up the USERNAMES
                                from_hyper_name = getHyperLink(from_member.user.id, from_member.user.first_name)
                                to_hyper_name = getHyperLink(to_member.user.id, to_member.user.first_name)

                                from_username = from_hyper_name
                                to_username = to_hyper_name

                                # COMMANDS FOR ALL MENERB IN REPLY MESSAGES


                                # COMMANDS ACSESABLE TO ALL ADMINISTROTORS
                                if (crud.data[chat_id]['members'][from_member.user.id]['special_commands']['admin']) and (from_member.status == "administrator" or from_member.status == "creator" or superuser):

                                    if text == "W" or text == "😼" or text == "w":
                                        crud.change_rep(to_member.user.id, 1, chat_id)
                                        message = f'{bold(from_username)} increased reputation of {bold(to_username)}'
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('w')
                                        # delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['w'] = prev_msg_id
                                        crud.save()
                                        return

                                    elif text == "L" or text == "💀" or text == "l":
                                        crud.change_rep(to_member.user.id, -1, chat_id)
                                        message = f'{bold(from_username)} decreased reputation of {bold(to_username)}'
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('l')
                                        # delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['l'] = prev_msg_id
                                        crud.save()
                                        return

                                    if lst[0] == '/setrank':
                                        from_username = gethtmlLink(from_member.user.id, from_member.user.first_name)
                                        to_username = gethtmlLink(to_member.user.id, to_member.user.first_name)
                                        if crud.data[chat_id]['members'][to_member.user.id]['special_commands']['rank'] == None:
                                            lst.pop(0)
                                            new_rank = remove_unsupported_letter(' '.join(lst))
                                            if True:
                                                crud.setrank(to_member.user.id, chat_id, new_rank)
                                                message = f"{bold(from_username)} has set custom rank [ {bold(new_rank)} ] for {bold(to_username)}"
                                            else:
                                                message = f" {from_username}  custom ranks should contain only alphabets and spaces"
                                        else:
                                            message = f"a superuser had set rank for {to_hyper_name}"

                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('set')
                                        delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['set'] = prev_msg_id
                                        crud.save()
                                        return

                                    if lst[0] == '/unsetrank':
                                        crud.setrank(to_member.user.id, chat_id, None)
                                        message = f"{from_hyper_name} has unset rank for {to_hyper_name}"
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('set')
                                        delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['set'] = prev_msg_id
                                        crud.save()
                                        return

                                    elif lst_len == 2:
                                        pass

                                    if text == "/status":
                                        lst = crud.show_level(to_member.user.id, chat_id)
                                        rank_ = crud.getRankTitle(to_member.user.id, chat_id)
                                        message = f"{bold(to_hyper_name)} [ {bold(rank_)} ]\n{bold('Reputation:')} {bold(a(chat_id, crud.read_rep(to_member.user.id, chat_id)))}\n{bold('Level:')} {bold(a(chat_id, lst[2]))} [{a(chat_id, crud.read_lvl(to_member.user.id, chat_id))}/{a(chat_id, lst[1])}]"
                                        prev_msg_id = bot.send_message(chat_id, message, parse_mode='HTML', disable_web_page_preview=True).message_id
                                        del_msg('status')
                                        delete_command(chat_id, msg_id)
                                        crud.data[chat_id]['last_message_id']['status'] = prev_msg_id
                                        crud.save()
                                        return
    except:
        pass




bot.infinity_polling()