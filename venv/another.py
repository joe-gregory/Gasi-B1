from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import random
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import iot_api_client as iot
from iot_api_client.rest import ApiException
from pprint import pprint
from iot_api_client.configuration import Configuration
from kivy.app import App
from kivy.clock import Clock

root = Builder.load_string('''
<Demo>:
    canvas.before:
        Color:
            rgba: .7, .7, .7, 1
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'vertical'
    Label:
        text: "GASI\\n\\nversion Beta 1.0"
        font_size:20
        halign: 'center'
        color: 1,1,.4,1
        underline: True
        font_name: 'Roboto-Bold'
    Label:
        text:'NIVEL DE GAS:'
        color: 0,0,0,1
        background_color: 1,1,1,1
        font_size: 16
    Label:
        id: tanklevel
        text: '0'
        font_size: 100
        font_name: 'digital-7'
        color: 1,0,0,1
        canvas.before:
            Color:
                rgb: 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
    Label:
        text:'gracias por probar gasi!\\ncontacto:joe@gummilabs.com'
        halign: 'center'
        color: 0,0,0,1

''')

class Demo(BoxLayout):
    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.update_tank_level, 1)

    def update_tank_level(self, dt):
        print('entered update f')
        level = self.connect()
        #self.ids.tanklevel.text = str(level)
        mm = "%.2f" % level
        self.ids.tanklevel.text = mm + "%"
        print(level)

    def connect(self):
        print('entered connect f')
        oauth_client = BackendApplicationClient(client_id='ZJvxUUkxJ5KmiQ09Qf9vEHBnvqHEJCUI')
        token_url = "https://login.arduino.cc/oauth/token"
        oauth = OAuth2Session(client=oauth_client)
        token = oauth.fetch_token(
            token_url=token_url,
            client_id='ZJvxUUkxJ5KmiQ09Qf9vEHBnvqHEJCUI',
            client_secret='avPkazBMIGSnTTuqxaALpsS78R9Z56-zXJQ74kwmj0JrJSpBqjJDUqkkVUId0x93',
            audience="https://api2.arduino.cc/iot",
        )
        access_token = token.get("access_token")
        # print(access_token)
        client_config = Configuration(host="http://api2.arduino.cc/iot")
        client_config.access_token = access_token
        client = iot.ApiClient(client_config)
        properties_api = iot.PropertiesV2Api(client)
        thing_id = 'b427251c-f214-470c-ba3c-28d6c6311c9b'
        try:
            api_response = properties_api.properties_v2_list(thing_id)
            # pprint(api_response)
            print('exiting connect')
            #return str(api_response[0].last_value*0.169-81.6)+"%"
            return api_response[0].last_value*0.169-81.6
        except ApiException as e:
            print("Exception when calling PropertiesV2Api->propertiesV2List: %s\n" % e)

class MainApp(App):
    def build(self):
        return Demo()

if __name__ == '__main__':
    MainApp().run()