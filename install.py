import PySimpleGUI as sg
import json
import os



class GmaxInstall:
    def __init__(self):
        sg.theme('BluePurple')   # Tema da tela
        #layout
        layout = [
            [sg.Text('Log para backup:', size=(10,0)), sg.InputText(key='input', size=(80, 0))],
            [sg.Text('Destino do backup:', size=(10,0)), sg.InputText(key='output', size=(80, 0))],
            [sg.Text('Url maximus:', size=(0,0)), sg.InputText(key='url_max')],
            [sg.Text('Log:', font=(0,15))],
            [sg.Output(text_color='black', size=(80,20))],
            [sg.Button(button_text='Instalar'), sg.Button('Cancel')]
            ]
        #cria a tela
        self.window = sg.Window('Instalador Gmax').layout(layout)
    #função que inicia a tela  e a mantem rodando   
    def start(self):
        while True:
            #transfere os valores da tela  para a variavel value 
            self.Button, self.value=self.window.Read()
            print('Criando o serviço GMAX...')
            print('Aguardando receber as entradas de configurações...')
            path_ = self.value['input']
            output_ = self.value['output']
            url_maximus = self.value['url_max']

            print('Entradas capturadas!')
            
            #carrega o arquivo confg.json
            with open('config.json', 'r') as conf:
                data=json.load(conf)
                
            #edita o arquivo config.json
            with open("config.json", 'w') as upConf:
                data['maximus_url'] = url_maximus
                data["input_backup_log"] = path_
                data["output_backup_log"] = output_
                json.dump(data, upConf)
                print(data)
            
            #Cria o serviço
            try:
                print("Instalando o serviço Gmax")
                pathBat=os.getcwd()#Obtem endereço do diretório raiz   
                os.chdir('nssm/win64' )# navega até a pasta do instalador do serviço
                os.system('nssm install GMAX '+pathBat+'\Gmax.bat' )#executa o comando de instalar o serviço
            except Exception as e:
                print(e)
                sg.Popup("An error occurred!")

            print('Serviço GMAX criado com sucesso!')
            print('*** Talvez seja necessário configurar a opção de logon do serviço ***')

            
            #Para o programa
            if self.Button in (None, 'Cancel'):   # if user closes window or clicks cancel
                break
        self.window.close()



try:
    app=GmaxInstall()
    app.start()
except:
    sg.Popup("An error occurred!")
