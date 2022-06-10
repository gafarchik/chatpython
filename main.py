import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import *
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivy.clock import Clock
import socket
from time import *
from textwrap import wrap


Window.clearcolor = (0.98,0.98, 0.98, 1)
kv_text = '''
<MainArea>:
    Widget:
        id: flybox
        size_hint_y: 1/5
        pos_hint: {'x': 0, 'center_y': 1}
        canvas.before:
            Color:
                rgba: .9,.9,.9,1
            Rectangle:
                pos: self.pos
                size: self.size
'''

class MainArea(FloatLayout):
    pass
class MyApp(App):
    def clientsstart(self,instance):
        try:
            self.mainArea.remove_widget(self.startserver_btn)
            self.mainArea.add_widget(self.iptext)
            self.mainArea.add_widget(self.porttext)
            self.mainArea.add_widget(self.conserver_btn)
            self.mainArea.remove_widget(self.getip_btn)
        except:
            pass
    def serverstart(self,instance):
        try:
            self.mainArea.add_widget(self.getip_btn)
            self.mainArea.remove_widget(self.iptext)
            self.mainArea.remove_widget(self.porttext)
            self.mainArea.remove_widget(self.conserver_btn)
            self.mainArea.add_widget(self.startserver_btn)
        except:
            pass
    def get_ip(self,instance):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        self.IP = s.getsockname()[0]
        s.close()
        self.startchat()
    def proz(self,instance):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) 
            self.IP = s.getsockname()[0]
            s.close()
            self.context.text = str(self.IP)+str("     7777")
            self.mainArea.add_widget(self.context)
        except:
            pass
    def startchat(self):
        try:
            self.connectstsatus = 0
            self.serverstsatus = 1
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((str(self.IP), 7777))
            self.server.listen(1)
            self.usr, self.addr = self.server.accept()
            self.openchat()
        except:
            pass
    def openchat(self):
        try:
            self.f1.clear_widgets()
            self.f1.add_widget(Label(text="Start",color="#fafafa",font_size='5sp',pos=(0,0), size_hint=(1.0,1.0), halign="center"))
            self.f1.add_widget(Label(text="Start2",color="#fafafa",font_size='15sp',pos=(0,0), size_hint=(1.0,None), halign="left"))
            self.mainArea.add_widget(self.exitfromchat)
            self.mainArea.add_widget(self.messagetext)
            self.mainArea.add_widget(self.sendmessage)
            self.mainArea.remove_widget(self.server_btn)
            self.mainArea.remove_widget(self.getip_btn)
            self.mainArea.remove_widget(self.context)
            self.mainArea.remove_widget(self.client_btn)
            self.mainArea.remove_widget(self.startserver_btn)
            self.mainArea.remove_widget(self.conserver_btn)
            self.mainArea.remove_widget(self.iptext)
            self.mainArea.remove_widget(self.porttext)
            self.readvar = 1
            Clock.schedule_interval(self.read, 0.5)
        except:
            pass
    def conchat(self,instance):
        self.connectstsatus = 1
        self.serverstsatus = 0
        try:
            IP_address = str(self.iptext.text)
            Port = int(self.porttext.text)
            self.usr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.usr.connect((IP_address, Port))
            self.openchat()
        except:
            pass
    def read(self,datatime):
        try:
            if self.readvar == 1:
                dataFromClient = self.usr.recv(4096,socket.MSG_DONTWAIT)
                if dataFromClient != b'':
                    self.textprint = Label(text="Собеседник: " + dataFromClient.decode(),color="#00000",font_size='15sp',pos=(0,0), size_hint=(1.0,None), halign="left")
                    self.textprint.bind(width=lambda *x:
                    self.textprint.setter('text_size')(self, (self.textprint.width, None)),
                    texture_size=lambda *x: self.textprint.setter('height')(self, self.textprint.texture_size[1]))
                    self.f1.add_widget(self.textprint)
        except:
            pass
    def sendmessagefunc(self,instance):
        try:
            data = str(self.messagetext.text)
            self.usr.send(data.encode())
            self.sendtext = Label(text="Вы: "+data,color="#00000",font_size='15sp',pos=(0,0), size_hint=(1.0,None), halign="left")
            self.sendtext.bind(width=lambda *x:
                self.sendtext.setter('text_size')(self, (self.sendtext.width, None)),
                texture_size=lambda *x: self.sendtext.setter('height')(self, self.sendtext.texture_size[1]))
            self.f1.add_widget(self.sendtext)
            self.messagetext.text = ""
        except:
            pass
    def exitt(self,instance):
        try:
            self.f1.clear_widgets()
            self.mainArea.remove_widget(self.exitfromchat)
            self.mainArea.remove_widget(self.messagetext)
            self.mainArea.remove_widget(self.sendmessage)
            self.mainArea.add_widget(self.server_btn)
            self.mainArea.add_widget(self.getip_btn)
            self.mainArea.add_widget(self.context)
            self.mainArea.add_widget(self.client_btn)
            self.mainArea.add_widget(self.startserver_btn)
            if self.connectstsatus == 1:
                self.usr.close()
                self.readvar = 0
            if self.serverstsatus == 1:
                self.server.close()
                self.readvar = 0
        except:
            pass
    def build(self):
        try:
            Builder.load_string(kv_text)
            self.readvar = 0
            self.f1 = GridLayout(cols=1,spacing=30,size_hint_y=None)
            self.f1.bind(minimum_height=self.f1.setter('height'))
            main = MainArea()
            self.root = ScrollView(size_hint=(.80,.82),pos_hint={'x':0.1,'y':.05})
            self.mainArea = FloatLayout()
            self.logo = Label(text ="Alexandriya",color="#00000",font_size='25sp',pos_hint={'x':0,'center_y':0.95})
            self.server_btn = Button(text='Server',color="#00000",font_size='20sp',background_color=[.80,.80,.80,1],background_normal="",size_hint = (.20,.05),pos_hint={'x':.2,'center_y':0.85},on_press=self.serverstart)
            self.client_btn = Button(text='Client',color="#00000",font_size='20sp',background_color=[.80,.80,.80,1],background_normal="",size_hint = (.20,.05),pos_hint={'x':.6,'center_y':0.85},on_press=self.clientsstart)
            self.startserver_btn = Button(text='New Chat',color="#00000",font_size='20sp',background_color=[.80,.80,.80,1],background_normal="",size_hint = (.50,.10),pos_hint={'x':.25,'center_y':0.5},on_press=self.get_ip)
            self.getip_btn = Button(text='Get ip',color="#00000",font_size='20sp',background_color=[.80,.80,.80,1],background_normal="",size_hint = (.50,.10),pos_hint={'x':.25,'center_y':0.35},on_press=self.proz)
            self.context = Label(text ="",color="#00000",font_size='25sp',pos_hint={'x':.0,'center_y':.60})
            self.conserver_btn = Button(text='Connect',color="#00000",font_size='20sp',background_color=[.80,.80,.80,1],background_normal="",size_hint = (.50,.10),pos_hint={'x':.25,'center_y':0.2},on_press=self.conchat)
            self.iptext = TextInput(text='',size_hint = (.50,.10),pos_hint={'x':.25,'center_y':0.6},halign="center",font_size='15sp')
            self.porttext = TextInput(text='',size_hint = (.50,.10),pos_hint={'x':.25,'center_y':0.4},halign="center",font_size='15sp')
            self.messagetext = TextInput(text='',size_hint = (.85,.05),pos_hint={'x':.05,'center_y':0.05},halign="left",font_size='15sp')
            self.sendmessage = Button(text='>',color="#00000",font_size='20sp',background_color=[.50,.50,.50,1],background_normal="",size_hint = (.05,.05),pos_hint={'x':.9,'center_y':0.05},on_press=self.sendmessagefunc)
            self.exitfromchat = Button(text='<',color="#00000",font_size='20sp',background_color=[.50,.50,.50,1],background_normal="",size_hint = (.05,.05),pos_hint={'x':.05,'center_y':0.95},on_press=self.exitt)
            self.root.add_widget(self.f1)
            self.mainArea.add_widget(main)
            self.mainArea.add_widget(self.root)
            self.mainArea.add_widget(self.logo)
            self.mainArea.add_widget(self.getip_btn)
            self.mainArea.add_widget(self.startserver_btn)
            self.mainArea.add_widget(self.server_btn)
            self.mainArea.add_widget(self.client_btn)
            return self.mainArea
        except:
            pass
MyApp().run()
