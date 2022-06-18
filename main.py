import kivy
import socket
from time import *
from kivy.app import App
from textwrap import wrap
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty
from kivymd.icon_definitions import md_icons
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition




text_new_chat = "New Chat"
text_chats = "Chats"
text_settings = "Settings"
text_language = "Language"
text_account = "Account name"
text_langlogo = "Change language"
text_langmenu="Language"
text_acclogo = "Change account name"
text_save_nik = "Save"
text_server_label = "----Server----"
text_my_ip_btn = "My ip"
text_start_server_btn = "Start"
text_client_label = "----Client----"
text_connect_server_btn = "Connect"
text_wait_usr = "Wait user"
text_person_chat = "You"
text_ru = "RU"
text_en = "EN"

en_text_new_chat = "New Chat"
en_text_chats = "Chats"
en_text_settings = "Settings"
en_text_language = "Language"
en_text_account = "Account name"
en_text_langlogo = "Change language"
en_text_acclogo = "Change account name"
en_text_langmenu="Language"
en_text_save_nik="Save"
en_text_server_label = "----Server----"
en_text_my_ip_btn = "My ip"
en_text_start_server_btn = "Start"
en_text_client_label = "----Client----"
en_text_connect_server_btn = "Connect"
en_text_wait_usr = "Wait user"
en_text_person_chat="You"

ru_text_new_chat = "Новый чат"
ru_text_chats = "Чаты"
ru_text_settings = "Настройки"
ru_text_language = "Язык"
ru_text_account = "Имя аккаунта"
ru_text_langlogo = "Изменить язык"
ru_text_acclogo = "Изменить имя профиля"
ru_text_save_nik = "Сохранить"
ru_text_langmenu="Язык"
ru_text_server_label = "----Сервер----"
ru_text_my_ip_btn = "Мой ip"
ru_text_start_server_btn = "Запустить"
ru_text_client_label = "----Клиент----"
ru_text_connect_server_btn = "Подключиться"
ru_text_wait_usr = "Ожидание пользователя"
ru_text_person_chat = "Вы"

namevar = " "
clientname = ""

connectstsatus = 0
serverstsatus = 0

hist_name_dist = ["","","","",""]
hist_ip_dist = ["","","","",""]
hist_lang = ["New Chat","Chats","Settings","Language","Account name","Change language","Language","Change account name","Save","----Server----","My ip","Start","----Client----","Connect","Wait user","You","RU","EN"]
hist_name_dist_r = hist_name_dist[::-1]
hist_ip_dist_r = hist_ip_dist[::-1]

nl = 0
check = 0

ui_text = ("""
<Context>:
        Widget:
                id:logo
                size_hint_y: 1/5
                pos_hint: {'x': 0, 'center_y': 1}
                canvas:
                        Color:
                                id: logobgcolor
                                rgb:0,0.56,0.98
         
                        Rectangle:
                                id: logobg
                                pos:self.pos
                                size:self.width,self.height
                FloatLayout:
                        size: logo.size
                        pos: logo.pos
                        Label:
                                id:logotext
                                bold: True
                                text:"Chats"
                                color: 1,1,1
                                pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                                font_size: logo.height/5
                        MDIconButton:
                                opacity: 0
                                disabled:1
                                id: exitchat
                                icon: 'exit-to-app'
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                                user_font_size: "20sp"
                                pos_hint: {'center_x': 2, 'center_y': 2}
                                on_release: root.close_chat()
        MDList:
                id: chatlist
                size_hint_y: 23/35
                pos_hint: {'x': 0, 'y': 0.25}
                TwoLineListItem:
                        id: listitem1
                        secondary_text: root.hist_ip_dist_r[0]
                        text: root.hist_name_dist_r[0]
                TwoLineListItem:
                        id: listitem2
                        secondary_text: root.hist_ip_dist_r[1]
                        text: root.hist_name_dist_r[1]
                TwoLineListItem:
                        id: listitem3
                        secondary_text: root.hist_ip_dist_r[2]
                        text: root.hist_name_dist_r[2]
                TwoLineListItem:
                        id: listitem4
                        secondary_text: root.hist_ip_dist_r[3]
                        text: root.hist_name_dist_r[3]
                TwoLineListItem:
                        id: listitem5
                        secondary_text: root.hist_ip_dist_r[4]
                        text: root.hist_name_dist_r[4]
        MDList:
                id: settingsscreen
                size_hint_y: 23/35
                pos_hint: {'x': 0, 'y': 0.25}
                disabled: 1
                opacity: 0
                TwoLineIconListItem:
                        id: settingslistitem1
                        text: "Account name"
                        secondary_text: "New user"
                        on_release: root.change_account(settingslistitem1)
                        IconLeftWidget:
                                icon:"account"
                TwoLineIconListItem:
                        id: settingslistitem2
                        text: "Language"
                        secondary_text: "EN"
                        on_release: root.change_theme(settingslistitem2)
                        IconLeftWidget:
                                icon:"earth"


        Widget:
                id: menu
                size_hint_y: 1/7
                pos_hint: {'x': 0, 'center_y': 0}
                canvas:
                        Color:
                                id: menubgcolor
                                rgb:0,0.56,0.98
         
                        Rectangle:
                                id: menubg
                                pos:self.pos
                                size:self.width,self.height
                FloatLayout:
                        id:menubtns
                        size: menu.size
                        pos: menu.pos
                        MDFloatingActionButton:
                                id: pluschat
                                icon: 'chat-plus-outline'
                                theme_icon_color: "Custom"
                                text_color: 1,1,1,1
                                user_font_size: "25sp"
                                pos_hint: {'center_x': 0.5, 'center_y': 1}
                                on_release: root.new_chat(pluschat)
                        MDIconButton:
                                id: settingsbtn
                                icon: 'cog-outline'
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                                user_font_size: "25sp"
                                pos_hint: {'center_x': 0.8, 'center_y': 0.8}
                                on_release: root.settings_func(settingsbtn)
                        MDIconButton:
                                id: mainchats
                                icon: 'view-list'
                                theme_text_color: "Custom"
                                text_color: 1,1,1,1
                                user_font_size: "25sp"
                                icon_color: app.theme_cls.primary_color
                                pos_hint: {'center_x': 0.2, 'center_y': 0.8}
                                on_release: root.main_chat_list(mainchats)

        FloatLayout:
                id: changethememenu
                size_hint_y:1/3
                size_hint_x:1/1.1
                pos_hint:{"center_x":2,"center_y":2}
                disabled:1
                opacity:0
                canvas:
                        Color:
                                id: changethememenubg
                                rgba: 1, 1 ,1,1
                        Rectangle:
                                pos:self.pos
                                size:self.width,self.height
                        Color:
                                id: changethememenuborder
                                rgba:0,0.56,0.98,1
                        Line:
                                width: 2
                                rectangle: self.x, self.y, self.width, self.height
                Label:
                        id:thememenutext
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        text:"Change language"
                        color: 0,0,0
                        font_size: changethememenu.height/8
                MDIconButton:
                        id: exitthememenu
                        icon: 'exit-to-app'
                        theme_text_color: "Custom"
                        text_color: 1,0,0,1
                        user_font_size: "20sp"
                        pos_hint: {'center_x': 0.95, 'center_y': 0.93}
                        on_release: root.close_change_menu(changethememenu)
                MDRoundFlatButton:
                        id: lightthemebutton
                        text: 'EN'
                        user_font_size: "20sp"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        on_release: root.change_lang(0)
                MDRoundFlatButton:
                        id: lightthemebutton
                        text: 'RU'
                        user_font_size: "20sp"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                        on_release: root.change_lang(1)
        FloatLayout:
                id: changeaccountmenu
                size_hint_y:1/3
                size_hint_x:1/1.1
                pos_hint:{"center_x":2,"center_y":2}
                disabled:1
                opacity:0
                canvas:
                        Color:
                                id: changeaccount
                                rgba: 1, 1 ,1,1
                        Rectangle:
                                pos:self.pos
                                size:self.width,self.height
                        Color:
                                rgba:0,0.56,0.98,1
                        Line:
                                width: 2
                                rectangle: self.x, self.y, self.width, self.height
                Label:
                        id:accountmenutext
                        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                        text:"Change account name"
                        color: 0,0,0
                        font_size: changeaccountmenu.height/8
                MDIconButton:
                        id: exitthomemenu
                        icon: 'exit-to-app'
                        theme_text_color: "Custom"
                        text_color: 1,0,0,1
                        user_font_size: "20sp"
                        pos_hint: {'center_x': 0.95, 'center_y': 0.93}
                        on_release: root.close_account_menu(changeaccountmenu)
                TextInput:
                        id:inputnik
                        size_hint_x: 1/1.5
                        size_hint_y:1/5
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        valign:"center"
                        font_size:"20sp"
                MDRoundFlatButton:
                        id: savedataname
                        text: 'Save'
                        user_font_size: "20sp"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                        on_release: root.savename(0)
        BoxLayout:
                id: mainchat
                size_hint_y:1/1.12
                size_hint_x:1/1
                pos_hint:{"center_x":2,"center_y":2}
                disabled:1
                opacity: 0 
                ScrollView:
                        size_hint_y:1/1.09
                        size_hint_x:1/1
                        pos_hint:{"center_x":0.5,"center_y":0.53}
                        # here we can set bar color
                        bar_color: [0, 143, 250, 1]
             
                        # here we can set bar width
                        bar_width: 5
             
                        BoxLayout:
                                size: (self.parent.width, self.parent.height-1)
                                id: container
                                orientation: "vertical"
                                size_hint_y: None
                                spacing: 10
                                height: self.minimum_height
        FloatLayout:
                id: chat_text_input
                size_hint_x:1/1
                size_hint_y:1/14
                orientation: 'horizontal'
                pos_hint:{"x":2,"y":2}
                disabled:1
                opacity: 0
                canvas.before:
                        Color:
                                rgb: 0,0.56,0.98
                        Rectangle:
                                pos: self.pos
                                size: self.size
                TextInput:
                        text:""
                        pos_hint:{"x":0.02,"y":0.05}
                        id: chat_input_obj
                        font_size: chat_input_obj.height/1.5
                        size_hint_y:1/1.1
                        size_hint_x: 1/1.15
                MDIconButton:
                        id: send_message
                        icon: "send"
                        user_font_size: chat_text_input.height/1.2
                        theme_text_color: "Custom"
                        text_color:1,1,1
                        pos_hint: {'center_x': 0.95, 'center_y': 0.5}
                        on_release: root.send_msg(1)
        FloatLayout:
                id: start_chat_menu
                size_hint_y:1/1.2
                size_hint_x:1/1
                disabled:1
                opacity:0
                pos_hint: {'center_x':2,'center_y':2}
                Label:
                        id:server_label
                        text:"----Server----"
                        color: 0,0,0
                        font_size: start_chat_menu.height/17
                        pos_hint:{'center_x':0.5,"center_y":0.95}
                Label:
                        id:my_ip
                        text:" "
                        color:0,0,0
                        font_size: start_chat_menu.height/25
                        pos_hint:{'center_x':0.5,"center_y":0.90}
                MDRoundFlatButton:
                        id: my_ip_btn
                        text:"My ip"
                        size_hint_x:1/2
                        pos_hint:{'center_x':0.5,"center_y":0.80}
                        on_release: root.get_ip_func(1)
                MDRoundFlatButton:
                        id: start_server_btn
                        text:"Start"
                        size_hint_x:1/2
                        pos_hint:{'center_x':0.5,"center_y":0.70}
                        on_release: root.start_server(1)
                Label:
                        id:client_label
                        text:"----Client----"
                        color:0,0,0
                        font_size: start_chat_menu.height/17
                        pos_hint:{'center_x':0.5,"center_y":0.55}
                TextInput:
                        id: connect_ip_input
                        size_hint_x:1/1.2
                        size_hint_y:1/10
                        font_size:connect_ip_input.height/1.5
                        pos_hint: {'center_x':0.5,'center_y':0.45}
                MDRoundFlatButton:
                        id: connect_server_btn
                        text:"Connect"
                        size_hint_x:1/2
                        pos_hint:{'center_x':0.5,"center_y":0.30}
                        on_release: root.conn_server(1)
                                   """)
class Context(Screen):
    global text_langmenu,text_new_chat, text_chats, text_settings, text_account, text_language, text_langlogo, text_acclogo,text_save_nik,text_server_label,text_my_ip_btn,text_start_server_btn,text_client_label,text_connect_server_btn,text_wait_usr,text_person_chat
    global en_text_langmenu,en_text_new_chat, en_text_chats, en_text_settings, en_text_account, en_text_language, en_text_langlogo,en_text_acclogo,en_text_save_nik,en_text_server_label,en_text_my_ip_btn,en_text_start_server_btn,en_text_client_label,en_text_connect_server_btn,en_text_wait_usr,en_text_person_chat
    global ru_text_langmenu,ru_text_new_chat, ru_text_chats, ru_text_settings, ru_text_account, ru_text_language, ru_text_langlogo, ru_text_acclogo, ru_text_save_nik,ru_text_server_label,ru_text_my_ip_btn,ru_text_start_server_btn,ru_text_client_label,ru_text_connect_server_btn,ru_text_wait_usr,ru_text_person_chat
    Builder.load_string(ui_text)
    hist_name_dist_r = hist_name_dist_r
    hist_ip_dist_r = hist_ip_dist_r
    hist_lang = hist_lang
    def __init__(self,**kwargs):
        super(Context,self).__init__(**kwargs)
        global namevar
        self.store = JsonStore("cache.json")
        if self.store.get("Lang")["Lang"] == 0:
            self.change_lang(0)
        elif self.store.get("Lang")["Lang"] == 1:
            self.change_lang(1)
        namevar = self.store.get("usr_name")["name"]
        self.ids.settingslistitem1.secondary_text = namevar
        hist_name_dist.pop(0)
        hist_name_dist.append(self.store.get("fifth_list_elem")["name"])
        hist_ip_dist.pop(0)
        hist_ip_dist.append(self.store.get("fifth_list_elem")["ip"])
        hist_name_dist.pop(0)
        hist_name_dist.append(self.store.get("fourth_list_elem")["name"])
        hist_ip_dist.pop(0)
        hist_ip_dist.append(self.store.get("fourth_list_elem")["ip"])
        hist_name_dist.pop(0)
        hist_name_dist.append(self.store.get("third_list_elem")["name"])
        hist_ip_dist.pop(0)
        hist_ip_dist.append(self.store.get("third_list_elem")["ip"])
        hist_name_dist.pop(0)
        hist_name_dist.append(self.store.get("second_list_elem")["name"])
        hist_ip_dist.pop(0)
        hist_ip_dist.append(self.store.get("second_list_elem")["ip"])
        hist_name_dist.pop(0)
        hist_name_dist.append(self.store.get("first_list_elem")["name"])
        hist_ip_dist.pop(0)
        hist_ip_dist.append(self.store.get("first_list_elem")["ip"])
        self.main_chat_list(1)
    def new_chat(self,btnchange):
        self.ids.pluschat.icon = "chat-plus"
        self.ids.settingsbtn.icon = "cog-outline"
        self.ids.mainchats.icon = "view-list-outline"
        self.ids.logotext.text=hist_lang[0]
        self.ids.chatlist.disabled = 1
        self.ids.chatlist.opacity = 0
        self.ids.settingsscreen.disabled = 1
        self.ids.settingsscreen.opacity = 0
        self.ids.chatlist.pos_hint = {'center_x':2,'center_y':2}
        self.ids.settingsscreen.pos_hint = {'x': 2, 'y': 2}
        self.ids.start_chat_menu.pos_hint = {'center_x':0.5,'center_y':0.48}
        self.ids.start_chat_menu.disabled = 0
        self.ids.start_chat_menu.opacity = 1
    def settings_func(self,btnchange):
        self.ids.pluschat.icon = "chat-plus-outline"
        self.ids.settingsbtn.icon = "cog"
        self.ids.mainchats.icon = "view-list-outline"
        self.ids.logotext.text=hist_lang[2]
        self.ids.chatlist.disabled = 1
        self.ids.chatlist.opacity = 0
        self.ids.settingsscreen.disabled = 0
        self.ids.settingsscreen.opacity = 1
        self.ids.chatlist.pos_hint = {'center_x':2,'center_y':2}
        self.ids.settingsscreen.pos_hint = {'x': 0, 'y': 0.25}
        self.ids.start_chat_menu.pos_hint = {'center_x':2,'center_y':2}
        self.ids.start_chat_menu.disabled = 1
        self.ids.start_chat_menu.opacity = 0
    def main_chat_list(self,btnchange):
        self.ids.pluschat.icon = "chat-plus-outline"
        self.ids.settingsbtn.icon = "cog-outline"
        self.ids.mainchats.icon = "view-list"
        self.ids.listitem1.text = hist_name_dist[::-1][0]
        self.ids.listitem1.secondary_text = hist_ip_dist[::-1][0]
        self.ids.listitem2.text = hist_name_dist[::-1][1]
        self.ids.listitem2.secondary_text = hist_ip_dist[::-1][1]
        self.ids.listitem3.text = hist_name_dist[::-1][2]
        self.ids.listitem3.secondary_text = hist_ip_dist[::-1][2]
        self.ids.listitem4.text = hist_name_dist[::-1][3]
        self.ids.listitem4.secondary_text = hist_ip_dist[::-1][3]
        self.ids.listitem5.text = hist_name_dist[::-1][4]
        self.ids.listitem5.secondary_text = hist_ip_dist[::-1][4]
        self.ids.logotext.text=hist_lang[1]
        self.ids.chatlist.disabled = 0
        self.ids.chatlist.opacity = 1
        self.ids.settingsscreen.pos_hint = {'center_x':2,'center_y':2}
        self.ids.chatlist.pos_hint = {'x': 0, 'y': 0.25}
        self.ids.settingsscreen.disabled = 1
        self.ids.settingsscreen.opacity = 0
        self.ids.start_chat_menu.pos_hint = {'center_x':2,'center_y':2}
        self.ids.start_chat_menu.disabled = 1
        self.ids.start_chat_menu.opacity = 0
    def change_theme(self,btnchange):
        self.ids.changethememenu.disabled = 0
        self.ids.changethememenu.opacity = 1
        self.ids.settingsscreen.disabled = 1
        self.ids.changethememenu.pos_hint = {"center_x":0.5,"center_y":0.5}
    def close_change_menu(self,btnchange):
        self.ids.changethememenu.disabled = 1
        self.ids.changethememenu.opacity = 0
        self.ids.settingsscreen.disabled = 0
        self.ids.changethememenu.pos_hint = {"center_x":2,"center_y":2}
    def change_lang(self,lang):
        global text_langmenu,text_new_chat, text_chats, text_settings, text_account, text_language, text_langlogo, text_acclogo,text_save_nik,text_server_label,text_my_ip_btn,text_start_server_btn,text_client_label,text_connect_server_btn,text_wait_usr,text_person_chat
        global en_text_langmenu,en_text_new_chat, en_text_chats, en_text_settings, en_text_account, en_text_language, en_text_langlogo,en_text_acclogo,en_text_save_nik,en_text_server_label,en_text_my_ip_btn,en_text_start_server_btn,en_text_client_label,en_text_connect_server_btn,en_text_wait_usr,en_text_person_chat
        global ru_text_langmenu,ru_text_new_chat, ru_text_chats, ru_text_settings, ru_text_account, ru_text_language, ru_text_langlogo, ru_text_acclogo, ru_text_save_nik,ru_text_server_label,ru_text_my_ip_btn,ru_text_start_server_btn,ru_text_client_label,ru_text_connect_server_btn,ru_text_wait_usr,ru_text_person_chat
        if lang == 0:
            hist_lang[0] = en_text_new_chat
            hist_lang[1] = en_text_chats
            hist_lang[2] = en_text_settings
            hist_lang[3] = en_text_language
            hist_lang[4] = en_text_account
            hist_lang[5] = en_text_langlogo
            hist_lang[6] = en_text_langmenu
            hist_lang[7] = en_text_acclogo
            hist_lang[8] = en_text_save_nik
            hist_lang[9] = en_text_server_label
            hist_lang[10] = en_text_my_ip_btn
            hist_lang[11] = en_text_start_server_btn
            hist_lang[12] = en_text_client_label
            hist_lang[13] = en_text_connect_server_btn
            hist_lang[14] = en_text_wait_usr
            hist_lang[15] = en_text_person_chat
            self.ids.connect_server_btn.text = hist_lang[13]
            self.ids.client_label.text = hist_lang[12]
            self.ids.logotext.text = hist_lang[2]
            self.ids.thememenutext.text = hist_lang[5]
            self.ids.settingslistitem2.text = hist_lang[6]
            self.ids.settingslistitem2.secondary_text = hist_lang[17]
            self.ids.settingslistitem1.text = hist_lang[4]
            self.ids.accountmenutext.text = hist_lang[7]
            self.ids.savedataname.text = hist_lang[8]
            self.ids.server_label.text = hist_lang[9]
            self.ids.my_ip_btn.text=hist_lang[10]
            self.ids.start_server_btn.text=hist_lang[11]
            self.ids.changethememenu.disabled = 1
            self.ids.changethememenu.opacity = 0
            self.ids.settingsscreen.disabled = 0
            self.ids.changethememenu.pos_hint = {"center_x":2,"center_y":2}
            self.store.put("Lang",Lang=0)
        if lang == 1:
            hist_lang[0] = ru_text_new_chat
            hist_lang[1] = ru_text_chats
            hist_lang[2] = ru_text_settings
            hist_lang[3] = ru_text_language
            hist_lang[4] = ru_text_account
            hist_lang[5] = ru_text_langlogo
            hist_lang[6] = ru_text_langmenu
            hist_lang[7] = ru_text_acclogo
            hist_lang[8] = ru_text_save_nik
            hist_lang[9] = ru_text_server_label
            hist_lang[10] = ru_text_my_ip_btn
            hist_lang[11] = ru_text_start_server_btn
            hist_lang[12] = ru_text_client_label
            hist_lang[13] = ru_text_connect_server_btn
            hist_lang[14] = ru_text_wait_usr
            hist_lang[15] = ru_text_person_chat
            self.ids.connect_server_btn.text = hist_lang[13]
            self.ids.client_label.text = hist_lang[12]
            self.ids.logotext.text = hist_lang[2]
            self.ids.thememenutext.text = hist_lang[5]
            self.ids.settingslistitem2.text = hist_lang[6]
            self.ids.settingslistitem2.secondary_text = hist_lang[16]
            self.ids.settingslistitem1.text = hist_lang[4]
            self.ids.accountmenutext.text = hist_lang[7]
            self.ids.savedataname.text = hist_lang[8]
            self.ids.server_label.text = hist_lang[9]
            self.ids.my_ip_btn.text=hist_lang[10]
            self.ids.start_server_btn.text=hist_lang[11]
            self.ids.changethememenu.disabled = 1
            self.ids.changethememenu.opacity = 0
            self.ids.settingsscreen.disabled = 0
            self.ids.changethememenu.pos_hint = {"center_x":2,"center_y":2}
            self.store.put("Lang",Lang=1)
    def close_account_menu(self,btnchange):
        self.ids.changeaccountmenu.disabled = 1
        self.ids.changeaccountmenu.opacity = 0
        self.ids.settingsscreen.disabled = 0
        self.ids.changeaccountmenu.pos_hint = {"center_x":2,"center_y":2}
    def change_account(self,btnchange):
        self.ids.changeaccountmenu.disabled = 0
        self.ids.changeaccountmenu.opacity = 1
        self.ids.settingsscreen.disabled = 1
        self.ids.changeaccountmenu.pos_hint = {"center_x":0.5,"center_y":0.5}
    def savename(self,btnchange):
        global namevar
        namevar = self.ids.inputnik.text
        self.ids.settingslistitem1.secondary_text = namevar
        self.ids.changeaccountmenu.disabled = 1
        self.ids.changeaccountmenu.opacity = 0
        self.ids.settingsscreen.disabled = 0
        self.ids.changeaccountmenu.pos_hint = {"center_x":2,"center_y":2}
        self.store.put("usr_name",name=namevar)
    def get_ip_func(self,btnchange):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) 
            self.IP = s.getsockname()[0]
            s.close()
            self.ids.my_ip.text = str(self.IP)
        except:
            pass
    def start_server(self,btnchange):
        global text_wait_usr
        try:
            self.readvar = 0
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) 
            self.IP = s.getsockname()[0]
            s.close()
            self.openchat()
            Clock.schedule_interval(self.wait_client,0.2)
        except Exception as e:
            pass
    def send_msg(self,btnchange):
        try:
            data = self.ids.chat_input_obj.text
            self.usr.send(data.encode())
            if len(data)>=31:
                mymsgpos = 0.5
            else:
                mymsgpos = 0.95
                mymsgpos = mymsgpos-len(data)/100
                mymsgpos = mymsgpos/2
            if mymsgpos < 0.4:
                mymsgpos = 0.4
            self.sendtext = MDLabel(text=text_person_chat+"\n"+data,color="#00000",font_size=self.ids.container.height/1.5,pos_hint = {"x":mymsgpos,"y":0.05}, size_hint=(0.6,None), halign="left",padding_x=5,padding_y=5,md_bg_color=(0,0.56,0.98,1))
            self.sendtext.bind(width=lambda *x:
                self.sendtext.setter('text_size')(self, (self.sendtext.width, None)),
                texture_size=lambda *x: self.sendtext.setter('height')(self, self.sendtext.texture_size[1]))
            self.ids.container.add_widget(self.sendtext)
            self.ids.chat_input_obj.text = ""
        except Exception as e:
            pass
    def wait_client(self,btnchange):
        global namevar
        global clientname
        global connectstsatus
        global serverstsatus
        global check
        if check == 0:
            try:
                connectstsatus = 0
                serverstsatus = 1
                self.ids.chat_text_input.disabled = 1
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind((str(self.IP), 7777))
                self.server.listen(1)
                self.server.settimeout(0.1)
                self.usr, self.addr = self.server.accept()
                dataFromClient = self.usr.recv(4096)
                if dataFromClient != b'':
                    self.ids.logotext.text = dataFromClient.decode()
                    clientname = dataFromClient.decode()
                data = namevar
                self.usr.send(data.encode())
                hist_name_dist.pop(0)
                hist_name_dist.append(str(clientname))
                hist_ip_dist.pop(0)
                hist_ip_dist.append(str(self.addr[0]))
                self.store.put("fifth_list_elem",name=self.store.get("fourth_list_elem")["name"],ip=self.store.get("fourth_list_elem")["ip"])
                self.store.put("fourth_list_elem",name=self.store.get("third_list_elem")["name"],ip=self.store.get("third_list_elem")["ip"])
                self.store.put("third_list_elem",name=self.store.get("second_list_elem")["name"],ip=self.store.get("second_list_elem")["ip"])
                self.store.put("second_list_elem",name=self.store.get("first_list_elem")["name"],ip=self.store.get("first_list_elem")["ip"])
                self.store.put("first_list_elem",name=str(clientname),ip=str(self.addr[0]))
                check = 1
                self.ids.chat_text_input.disabled = 0
            except Exception as e:
                Clock.schedule_interval(self.wait_client,1)
        else:
            Clock.unschedule(self.wait_client)
    def conn_server(self,btnchange):
        global namevar
        global clientname
        global connectstsatus
        global serverstsatus
        try:
            self.readvar = 0
            connectstsatus = 1
            serverstsatus = 0
            IP_address = str(self.ids.connect_ip_input.text)
            Port = int("7777")
            self.usr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.usr.connect((IP_address, Port))
            data = namevar
            self.usr.send(data.encode())
            dataFromClient = self.usr.recv(4096)
            if dataFromClient != b'':
                self.ids.logotext.text = dataFromClient.decode()
                clientname = dataFromClient.decode()
            hist_name_dist.pop(0)
            hist_name_dist.append(str(clientname))
            hist_ip_dist.pop(0)
            hist_ip_dist.append(str(IP_address))
            self.store.put("fifth_list_elem",name=self.store.get("fourth_list_elem")["name"],ip=self.store.get("fourth_list_elem")["ip"])
            self.store.put("fourth_list_elem",name=self.store.get("third_list_elem")["name"],ip=self.store.get("third_list_elem")["ip"])
            self.store.put("third_list_elem",name=self.store.get("second_list_elem")["name"],ip=self.store.get("second_list_elem")["ip"])
            self.store.put("second_list_elem",name=self.store.get("first_list_elem")["name"],ip=self.store.get("first_list_elem")["ip"])
            self.store.put("first_list_elem",name=str(clientname),ip=str(IP_address))
            self.openchat()
        except Exception as e:
            pass
    def read(self,dt):
        global clientname
        try:
            if self.readvar == 1:
                dataFromClient = self.usr.recv(4096,socket.MSG_DONTWAIT)
                mymsgsize = 0.0
                data = dataFromClient.decode()
                if len(data)>=31:
                    mymsgsize = 0.5
                elif len(clientname)>len(data):
                    if len(clientname)>=31:
                        mymsgsize = 0.5
                    else:
                        mymsgsize = 0.1
                        mymsgsize = mymsgsize+len(clientname)/100
                        mymsgsize = mymsgsize*2
                else:
                    mymsgsize = 0.1
                    mymsgsize = mymsgsize+len(data)/100
                    mymsgsize = mymsgsize*2
                if mymsgsize > 0.6:
                    mymsgsize = 0.6
                if dataFromClient != b'':
                    self.textprint = MDLabel(text=clientname+"\n" + dataFromClient.decode(),color="#00000",font_size=self.ids.container.height/1.5,pos=(0,0), size_hint=(mymsgsize,None), halign="left",padding_x=5,padding_y=5,md_bg_color=(0.80,0.80,0.80,1))
                    self.textprint.bind(width=lambda *x:
                        self.textprint.setter('text_size')(self, (self.textprint.width, None)),
                        texture_size=lambda *x: self.textprint.setter('height')(self, self.textprint.texture_size[1]))
                    self.ids.container.add_widget(self.textprint)
        except Exception as e:
            pass
    def close_chat(self):
        global connectstsatus
        try:
            self.ids.container.clear_widgets()
            self.ids.pluschat.icon = "chat-plus"
            self.ids.settingsbtn.icon = "cog-outline"
            self.ids.mainchats.icon = "view-list-outline"
            self.ids.logotext.text=text_new_chat
            self.ids.chatlist.disabled = 1
            self.ids.chatlist.opacity = 0
            self.ids.settingsscreen.disabled = 1
            self.ids.settingsscreen.opacity = 0
            self.ids.chatlist.pos_hint = {'center_x':2,'center_y':2}
            self.ids.settingsscreen.pos_hint = {'x': 2, 'y': 2}
            self.ids.start_chat_menu.pos_hint = {'center_x':0.5,'center_y':0.48}
            self.ids.start_chat_menu.disabled = 0
            self.ids.start_chat_menu.opacity = 1
            self.ids.chat_text_input.opacity = 0
            self.ids.chat_text_input.disabled = 1
            self.ids.chat_text_input.pos_hint = {"x":2,"y":2}
            self.ids.mainchat.disabled = 1
            self.ids.mainchat.opacity = 0
            self.ids.mainchat.pos_hint = {"center_x":2,"center_y":2}
            self.ids.menu.disabled = 0
            self.ids.menu.opacity = 1
            self.ids.menu.pos_hint = {'x': 0, 'center_y': 0}
            self.ids.exitchat.opacity = 0
            self.ids.exitchat.disabled = 1
            self.ids.exitchat.pos_hint = {'center_x': 2, 'center_y': 2}
            if connectstsatus == 1:
                self.usr.close()
                self.readvar = 0
            if serverstsatus == 1:
                self.server.close()
                self.readvar = 0
        except:
            pass
    def openchat(self):
        self.ids.exitchat.opacity = 1
        self.ids.exitchat.disabled = 0
        self.ids.exitchat.pos_hint = {'center_x': 0.05, 'center_y': 0.25}
        self.ids.menu.disabled = 1
        self.ids.menu.opacity = 0
        self.ids.menu.pos_hint = {'center_x':2,'center_y':2} 
        self.ids.mainchat.disabled = 0
        self.ids.mainchat.opacity = 1
        self.ids.mainchat.pos_hint = {"center_x":0.5,"center_y":0.45}
        self.ids.chatlist.disabled = 1
        self.ids.chatlist.opacity = 0
        self.ids.chatlist.pos_hint = {'center_x':2,'center_y':2}
        self.ids.start_chat_menu.pos_hint = {'center_x':2,'center_y':2}
        self.ids.start_chat_menu.disabled = 1
        self.ids.start_chat_menu.opacity = 0
        self.ids.settingsscreen.pos_hint = {'center_x':2,'center_y':2}
        self.ids.chat_text_input.opacity = 1
        self.ids.chat_text_input.disabled = 0
        self.ids.chat_text_input.pos_hint = {"x":0,"y":0}
        self.ids.settingsscreen.disabled = 1
        self.ids.settingsscreen.opacity = 0
        self.readvar = 1
        Clock.schedule_interval(self.read, 0.5)

class ChatApp(MDApp):
  
    # method which will render our application
    def build(self):
        main = Context()
        return main
  

ChatApp().run()
