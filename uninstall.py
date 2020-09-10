import PySimpleGUI as sg
import json
import os



class GmaxInstall:
    def __init__(self):
        sg.theme('Reddit')   # Tema da tela
        #layout
        layout = [
            [sg.Text('Log:', font=(0,15))],
            [sg.Output(text_color='black', size=(80,20))],
            [sg.Button(button_text='Uninstall', key='uninstall'), sg.Button('Cancel')]
            ]

        #cria a tela
        self.window = sg.Window('Uninstall Gmax', icon='pineapple_emoji.ico').layout(layout)
    #função que inicia a tela  e a mantem rodando   
    def start(self):
        while True:
            #transfere os valores da tela  para a variavel value 
            self.Button, self.value=self.window.Read()
            #Para o programa
            if self.Button in (None, 'Cancel'):   # if user closes window or clicks cancel
                break
            
            if(self.Button == 'uninstall'):
                try:
                    print('Removendo serviço GMAX...')
                    os.chdir('nssm/win64' )# navega até a pasta do instalador do serviço
                    os.system('nssm remove GMAX')
                    sg.Popup("successfully Uninstall!")
                    print('Gmax removido com sucesso!')
                    self.window.close()
                except Exception(e):
                    print(e)
                    sg.Popup("An error occurred!")
                    self.window.close()
                
                

        self.window.close()



try:
    app=GmaxInstall()
    app.start()
except:
    sg.Popup("An error occurred!")