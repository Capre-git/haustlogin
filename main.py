from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.graphics import InstructionGroup
from random import random as r

import socket


import tologin


class LogFailed(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RootWidget(FloatLayout):
    pass

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.fontname = 'MPARUDJingxiheiGb4-DB.otf'
        self.fontcolor =[1,1,1,1]
        self.contentbgcolor = [1, 1, 1, 0.1]
        self.cols = 2
        self.add_widget(Label(text=u'账号',
                              size_hint=(.5,.1),
                              font_name=self.fontname,
                              ))
        self.username = TextInput(multiline=False,
                                  text="161413130xxx",
                                  background_color=self.contentbgcolor,
                                  foreground_color=self.fontcolor,
                                  )
        self.add_widget(self.username)
        self.add_widget(Label(text=u'密码',
                              size_hint=(.5, .1),
                              font_name=self.fontname
                              ))
        self.password = TextInput(password=True,
                                  multiline=False,
                                  background_color=self.contentbgcolor,
                                  foreground_color=self.fontcolor
                                  )
        self.add_widget(self.password)
        self.size_hint = (0.7, 0.15)
        self.pos_hint = {'x': .15, 'y': .5}
        self.isfirstpress = True
        self.infodisplay = [Label(text=u'信息提示',
                                  size_hint_x=.1,
                                  font_name=self.fontname
                                  ),
                            Label(text=u'按下登陆按钮登陆',
                                  size_hint_x=.5,
                                  font_name=self.fontname
                                  )]
        self.add_widget(self.infodisplay[0])
        self.add_widget(self.infodisplay[1])
        self.filecontent()

    #def

    def filecontent(self, tagtosave = False):
        #path = '/storage/emulated/0/kivy/new/'
        #filename = path + 'filecontent'
        filename = 'filecontent'
        content = 'self.username.text = \'' + \
        self.username.text + '\'' + \
        '\nself.password.text = \''+ \
        self.password.text+'\''
        if tagtosave == True:
            with open(filename, 'w') as t:
                t.write(content)
        else:
            try:
                t = open(filename, 'r')
                exec(t.read())
            except FileNotFoundError:
                t = open(filename, 'w')
                t.write(content)
            finally:
                t.close()

    def on_press(self, instance):
        print('The button <%s> is being pressed' % instance.text)
        #print('username <%s>' % self.username.text)
        #print('password <%s>' % self.password.text)
        tologin.username = self.username.text
        tologin.password = self.password.text
        if tologin.password == '':
            self.infodisplay[1].text = u"输入密码后再点登陆"
            return 0
        elif not tologin.host_ip.startswith('172'):
            self.infodisplay[1].text = u"用寝室wifi才行"


        try:
            if self.isfirstpress:
                tologin.bind()
        except OSError as e:
            if e.args[0] == 10048:
                self.infodisplay[1].text = u'你已经登陆成功，不要再点了'
                self.isfirstpress = True
                return 0

        try:
            tologin.main()
        except tologin.LogFailed:
            self.infodisplay[1].text = u'密码填错了'

        except tologin.LogSuccessful:
            self.filecontent(tagtosave=True)
            self.infodisplay[1].text = u'成了，开始网上冲浪吧'
            self.isfirstpress = True
        except socket.timeout:
            self.infodisplay[1].text =u'不要用移动网络点这个'





class TestApp(App):
    def build(self):
        self.root = root = RootWidget()
        #set background to screen
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(.76, .74, 0.83, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)

        #bgrender = Widget(canvas=)
        lgScreen = LoginScreen()
        lgbtn = Button(text="登 陆",
                       size_hint = (.7,.1),
                       pos_hint = {'center_x': .5, 'center_y': .2},
                       font_name=lgScreen.fontname,
                       background_color=[.28,.35,.5,.3],
                       )
        lgbtn.bind(on_press=lgScreen.on_press)
        #self.root.add_widget(wid)
        self.root.add_widget(lgScreen)
        self.root.add_widget(lgbtn)
        return self.root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__=='__main__':
    TestApp().run()