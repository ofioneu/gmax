from flask import Flask, render_template,redirect, url_for, send_from_directory, flash, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
import psutil
import os
import sys
import json
import subprocess
import datetime
from datetime import datetime, date, timedelta
import time
from flask import send_file
import socket
import win32serviceutil
import threading
import os.path
import shutil
import win32ui
from flask import Flask
import logging
from logging.config import fileConfig
import json

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '@11tahe89!'
socketio = SocketIO(app)

hostname = socket.gethostname()
service='JBMAXIMUS'
machine=hostname
fileConfig('logging.cfg')
log = logging.getLogger('werkzeug')
log.disabled = True


with open("config.json") as conf:
        config = json.load(conf)


block = False
resetBlock = False
stopBlock = False
initTime = 0.0

servicoStatus={'rodando': 4, 'parado': 1, 'iniciando': 2, 'parando': 3}

@app.route('/')
def home():
    
    return render_template('home.html', maximus_url=config['maximus_url'])

@app.route('/stop')
def stop():
    try: 
        global block
        print("Block", block)
        if(block == False and status(service)==servicoStatus['rodando']):
            managerService('stop')
        else:
            flash("Já foi solicitado a interrupção do sistema. Aguarde!", "info")   
                 
    except Exception as e:
        flash("Favor startar o maximus, pois o mesmo está parado!", "error")
        app.logger.error('Gerenciamento de servico jboss: '+str(e))
    return redirect (url_for('home'))


@app.route('/start')
def start():    
    try:
        global block
        if(status(service)==servicoStatus['parado']):
            block = True
            managerService('start')
        else:
            flash("Sistema Maximus já está com o processo iniciado!", "info")

    except Exception as e:
        flash("O Sistema Maximus encontra-se desligado! Para iniciar o sistema clique em START!","error")
        app.logger.error('Gerenciamento de servico jboss: '+str(e))
    finally:
               
        return redirect (url_for('home'))
    


@app.route('/reset', methods=['GET', 'POST'])
def reset():    
    try:
        global block
        global resetBlock
        print("resetBlock0: ", resetBlock)
        
        if(status(service)==servicoStatus['rodando']):
            print("Entrei no if do reset")
            block = True
            managerService('reset')
            print("Finalizado managerService!")
            
        else:
            print("entrei no else do reset")
            flash("Já foi solicitado o reset do sistema. Aguarde!", "info")       
        
    except Exception as e:
        flash("Favor startar o maximus, pois o mesmo está parado!", "error") 
        app.logger.error('Processo de gerenciamento de logs, servicos e ou data-hora!: '+str(e))
        startJboss(service)

    finally:

        return redirect (url_for('home'))


@app.route('/download', methods=['GET', 'POST'])
def downloadFile ():
    data_download=[]
    arq_download=''
    arq_download= open(r'config_download.txt','r')
    for linha_downlaod in arq_download:
        data_download.append(linha_downlaod)
    arq_download.close()
    lista={'endereco_download':data_download[0]}
    enderecodownload=lista['endereco_download']
    path = enderecodownload
    return send_file(path, as_attachment=True)
    flash("Sucesso Download")
    return redirect (url_for('home'))



@socketio.on('message')
def machine_recursos(message):
    while True:
        try:
            cpu_percent=psutil.cpu_percent(interval=1)
            ram_percent=psutil.virtual_memory()[2]
            process_name = "java.exe"
            for process in psutil.process_iter():
                try:
                    if process.name() == process_name:
                        process_int= process.pid
                        p = psutil.Process(process_int)
                        ram_process=int(process.memory_info()[2])
                        ram_process_mb=round((ram_process/1023)*2,2)
                        cpu_process=p.cpu_percent(interval=1)
                except(psutil.AccessDenied):
                    pass
                except(psutil.NoSuchProcess):
                    pass
            dados_maquina={
                "cpu_total":cpu_percent,
                "ram_total":ram_percent,
                "cpu_process":cpu_process,
                "ram_process":ram_process_mb
            }
            json_dados_maquina=json.dumps(dados_maquina)        
            emit('message', json_dados_maquina)
            
        except Exception as e:
            pass
            #app.logger.warning('Processo java nao iniciado para obter valores de recurso do hardware: '+str(e))
        time.sleep(10)




def managerService(btn):
    flagService=False
    global block
    global resetBlock
    global stopBlock
    initTime =  time.time()
    if(btn=='reset' and resetBlock == False):
        flash("Iniciando reset...", "info")
        resetBlock = True     
        while(flagService==False):    
            if (status(service)==servicoStatus['rodando'] and stopBlock == False):
                stopBlock = True
                print("serviço está rodando e vou parar o mesmo")
                win32serviceutil.StopService(service, machine)
                print("Serviço parado!")

            elif(status(service)==servicoStatus['iniciando']):
                flash("Já foi solicitado a inicialização do sistema. Aguarde!", "info")

            elif(status(service)==servicoStatus['parando']):
                flash("Já foi solicitado a reinicialização do sistema. Aguarde!", "info")

            elif(status(service)==servicoStatus['parado']):
                print("O serviço está parado e vou copiar o log e estartar o mesmo")
                data_e_hora_atuais = datetime.now()
                data_e_hora_em_texto = data_e_hora_atuais.strftime('%Y-%m-%d %H-%M-%S')
                app.logger.info('JBOSS Parado!')
                app.logger.info('Renomeando log -- !' + data_e_hora_em_texto)
                os.rename(config['input_backup_log'], config['output_backup_log']+data_e_hora_em_texto)
                app.logger.info('log renomeado e copiado!')
                app.logger.info('Iniciando Start do JBOSS...')
                print("Iniciando o serviço")
                startJboss()
                print("Serviço iniciadoS")
                flash("A reinicialização foi efetuada com sucesso!", "sucess")
            else:
                flash("O Sistema Maximus encontra-se desligado! Para iniciar o sistema clique em START!", "error")
                
            endTime = time.time()
            delta = endTime - initTime
            print("resetBlock1: ", resetBlock)
            print("delta: ", delta)
            delta = endTime - initTime
            if(delta >= 60):
                resetBlock = True
                block = False
                flagService = True

            print("Block: ", block)
        
        stopBlock = False
                                   
                         
    if(btn == 'stop' and block == False):
        while(flagService==False):
            if (status(service)==servicoStatus['rodando']):
                win32serviceutil.StopService(service, machine)
                data_e_hora_atuais = datetime.now()
                data_e_hora_em_texto = data_e_hora_atuais.strftime('%Y-%m-%d %H-%M-%S')
                app.logger.info('JBOSS Parado!')
                app.logger.info('Renomeando log -- !' + data_e_hora_em_texto)
                os.rename(config['input_backup_log'], config['output_backup_log']+data_e_hora_em_texto)
                app.logger.info('log renomeado e copiado!')
                time.sleep(15)
                flash("STOP - A interrupção do sistema foi efetuada com sucesso!", "sucess")
                flagService=True

            elif(status(service)==servicoStatus['iniciando']):
                flash("Já foi solicitado a inicialização do sistema. Aguarde!", "info")

            elif(status(service)==servicoStatus['parando']):
                flash("Já foi solicitado a interrupção do sistema. Aguarde!", "info")

            elif(status(service)==servicoStatus['parado']):
                flash("O Sistema Maximus encontra-se desligado! Para iniciar o sistema clique em START!", "error")

            else:
                flash("O Sistema Maximus encontra-se desligado! Para iniciar o sistema clique em START!", "error")

    if(btn=='start'):
        flash("Iniciando o Maximus...", "sucess")

        while(flagService==False):

            if (status(service)==servicoStatus['rodando']):
                flash("Sistema Maximus já está com o processo iniciado!", "info")


            elif(status(service)==servicoStatus['iniciando']):
                flash("Já foi solicitado a inicialização do sistema. Aguarde o final do processo!", "info")


            elif(status(service)==servicoStatus['parando']):
                flash("Já foi solicitado a interrupção do sistema. Aguarde o final do processo!", "info")


            elif(status(service)==servicoStatus['parado']):
                initTime =  time.time()
                startJboss()
                flash("A inicialização foi efetuada com sucesso!", "sucess")
            endTime = time.time()
            delta = endTime - initTime
            print("delta: ", delta)
            if(delta >= 60):
                block = False
                flagService = True
                resetBlock = False

            
            else:
                flash("O Sistema Maximus encontra-se desligado! Para iniciar o sistema clique em START!", "error")


    time.sleep(3)

def startJboss():
    app.logger.info('Iniciando o servico jboss!')
    win32serviceutil.StartService(service, machine)
    app.logger.info('jboss iniciado!!')

def status(service):
    statusService = win32serviceutil.QueryServiceStatus(service)
    return statusService[1]

tsocket=threading.Thread(target=machine_recursos)
tsocket.start()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port= 5005, debug=True)