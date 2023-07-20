from pymongo import MongoClient
import json
from keys import *

class ReputationSystem(object):

    def __init__(self, bot):
        self.uri = "mongodb+srv://username:varunkapass@cluster0.lattlsd.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri)
        self.crud_mongo = self.client["CRUD"]
        self.test = self.crud_mongo['test']
        self.database_server = self.client['Chat-Level-Bot-Telegram-Mei']
        self.database = self.database_server['DataBase']
        self.data = self.database.find_one()
        self.counter = 0
        self.bot = bot

    def Create(self, post):
        post = json.loads(post)
        self.test.insert_one(post)
        return self.Read(post)
    
    def Read(self, query):
        if type(query) == str:
            query = json.loads(query)
        return str(self.test.find_one(query))
    
    def Update(self, query, post):
        query = json.loads(query)
        post = json.loads(post)
        self.test.update_one(query, { "$set": post })
        return self.Read(query)
    
    def Delete(self, query):
        query = json.loads(query)
        self.test.delete_one(query)
        return self.Read(query)
    
    def check_entry(self, user_id, chat_id):
        if str(user_id) not in self.data[str(chat_id)]['members'].keys():
            self.data[str(chat_id)]['members'][str(user_id)] = {'lvl':0, 'rep':0, 'custom_rank':{'name':None, 'points':None}, 'special_commands':{'rank':None, 'admin':True}}
            self.save()

    def check_chat_entry(self, chat_id):
        if str(chat_id) not in self.data.keys():
            self.data[str(chat_id)] = { 'last_message_id':{'me':None, 'toplvl':None, 'toprep': None, 'w':None, 'l':None, 'super':None, 'addlvl':None, 'set':None, 'status':None, 'levels':None, 'rmvlvl':None, 'apis':None}, 'levels' : {}, 'members' : {} }
            self.save()

    def read_rep(self, user_id, chat_id):
        return self.data[str(chat_id)]['members'][str(user_id)]['rep']
    
    def read_lvl(self, user_id, chat_id):
        return self.data[str(chat_id)]['members'][str(user_id)]['lvl']
    
    def change_rep(self, user_id, rep, chat_id):
        rep = int(rep)
        self.data[str(chat_id)]['members'][str(user_id)]['rep'] += rep
        self.save()
        return self.data[str(chat_id)]['members'][str(user_id)]['rep']
    
    def change_lvl(self, user_id, lvl, chat_id):
        lvl = int(lvl)
        self.data[str(chat_id)]['members'][str(user_id)]['lvl'] += lvl
        self.save()
        return self.data[str(chat_id)]['members'][str(user_id)]['lvl']
    
    def add_level(self, lvl_name, lvl_pt, chat_id):
        self.data[str(chat_id)]['levels'][lvl_name] = lvl_pt

    def del_level(self, lvl_name, chat_id):
        try:
            del self.data[str(chat_id)]['levels'][lvl_name]
        except:
            pass

    def show_levels(self, chat_id):
        lst = sorted(self.data[str(chat_id)]['levels'].items(), key=lambda x:x[1])
        msg = "<b>LEVELS:</b> 😼\n"
        i = len(lst) - 1
        while i >= 0:
            msg = msg + f"<a href='tg://user?id={str(chat_id)}'>{i+1}</a> <b>{lst[i][0]}</b> [<a href='tg://user?id={str(chat_id)}'>{lst[i][1]}</a>]\n"
            i -= 1
        return msg
    
    def show_level(self, user_id, chat_id):
        lst = sorted(self.data[str(chat_id)]['levels'].items(), key=lambda x:x[1])
        level_name = ""
        level_pt = 0
        c = 0
        i = 0
        length = len(lst)
        for lvl, pt in lst:
            if self.data[str(chat_id)]['members'][str(user_id)]['lvl'] >= pt:
                c = i + 1
                level_name = lvl
                if i < length-1:
                    level_pt = lst[i+1][1]
                else:
                    level_pt = "max"
            i += 1
        return level_name, level_pt, c
    
    def toplvl(self, chat_id, top_c):
        lst = sorted(self.data[str(chat_id)]['members'].items(), key=lambda x:x[1]['lvl'], reverse=True)
        length = len(lst)
        top_lvl_lst = []
        top = 1
        i = 0
        while i >= 0 and i < length and top <= top_c:
            user_id=lst[i][0]
            user_first_name = self.bot.get_chat_member(chat_id=chat_id, user_id=user_id).user.first_name
            if user_first_name == "":
                self.save()
                continue
            user_lvl = lst[i][1]['lvl']
            lvl_name, nxt_lvl_pt, curr_lvl =  self.show_level(user_id, chat_id)
            lvl_name = self.getRankTitle(str(user_id), str(chat_id))
            dic = {"id":str(user_id), "lvl":user_lvl, "lvl_name":lvl_name, "nxt_lvl_pt":nxt_lvl_pt, "curr_lvl":curr_lvl}
            top_lvl_lst.append(dic)
            i += 1
            top += 1
        return top_lvl_lst
    
    def toprep(self, chat_id, top_c):
        lst = sorted(self.data[str(chat_id)]['members'].items(), key=lambda x:x[1]['rep'], reverse=True)
        length = len(lst)
        top_rep_lst = []
        top = 1
        i = 0
        while i >= 0 and i < length and top <= top_c:
            user_id=lst[i][0]
            user_first_name = self.bot.get_chat_member(chat_id=chat_id, user_id=user_id).user.first_name
            if user_first_name == "":
                self.save()
                continue
            user_rep = lst[i][1]['rep']
            title = self.getRankTitle(str(user_id), str(chat_id))
            dic = {"id":str(user_id), "rep":user_rep, "title":title}
            top_rep_lst.append(dic)
            i += 1
            top += 1
        return top_rep_lst
    
    def getRankTitle(self, user_id, chat_id):
        rank = ""
        user = self.data[str(chat_id)]['members'][str(user_id)]
        if user['special_commands']['rank'] != None:
            rank = user['special_commands']['rank']
        elif user['custom_rank']['name'] != None:
            rank = user['custom_rank']['name']
        else:
            rank = self.show_level(str(user_id), str(chat_id))[0]
        return rank
    
    def setrank(self, user_id, chat_id, rank):
        self.data[str(chat_id)]['members'][str(user_id)]['custom_rank']['name'] = rank

    def special_status(self, user_id, chat_id):
        return self.data[str(chat_id)]['members'][str(user_id)]['special_commands']
    
    def save(self):
        myquery = { "query": "querykey" }
        newvalues = self.data
        self.database.replace_one(myquery, newvalues)