import flask_socketio
from flask import Flask, render_template,redirect, url_for, send_from_directory, flash
from flask_socketio import SocketIO
from flask_socketio import send, emit
import psutil
import os
import sys
import json
import subprocess
import datetime
from datetime import datetime, date
import time
from flask import send_file
import socket
import win32serviceutil
import threading
import os.path
import shutil
import win32ui




app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '@11tahe89!'
socketio = SocketIO(app)

hostname = socket.gethostname()
service_joboss='JBMAXIMUS'
service_modulo_bd = 'MODULO BD'
service_modulo_controle = 'MODULO CONTROLE'
service_modulo_digicon = 'MODULO DIGICON'
machine=hostname




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stop')
def stop():   
    try:
        #subprocess.Popen(endereco_stop)
        print("Parando o Jboss")
        win32serviceutil.StopService(service_joboss, machine)    
        time.sleep(3)
        print('Parando o Modulo BD')
        win32serviceutil.StopService(service_modulo_bd, machine)    
        time.sleep(3)
        print('Parando o Modulo Controle')
        win32serviceutil.StopService(service_modulo_controle, machine)   
        time.sleep(3)
        print('Parando o Modulo Digicon')
        win32serviceutil.StopService(service_modulo_digicon, machine)    
        time.sleep(3)
        flash("Sucesso Stop")
    except:
        flash("Falha Stop")
        print('A execucao do .bat falhou, check o endereco do arquivo .bat')
    return redirect (url_for('home'))
@app.route('/start')
def start():

    def service_running_jboss(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_jboss = service_running_jboss(service_joboss, machine)

    def service_running_BD(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_BD =service_running_BD(service_modulo_bd, machine)
    def service_running_controle(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_controle =service_running_controle(service_modulo_controle, machine)
    def service_running_digicon(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_digicon =service_running_digicon(service_modulo_digicon, machine)
    
    try:
        if not running_BD:
            print('Iniciando modulo BD')
            win32serviceutil.StartService(service_modulo_bd, machine)
            time.sleep(1.5)
        else:
            print('Falha ao iniciar modulo BD!!')
        if not running_controle:
            print('Iniciando modulo Controle')
            win32serviceutil.StartService(service_modulo_controle, machine)
            time.sleep(1.5)
        else:
            print("Falha ao iniciar modulo controle")
        if not running_digicon:
            print('Iniciando modulo Digicon')
            win32serviceutil.StartService(service_modulo_digicon, machine)
            time.sleep(1.5)
        else:
            print("Falha ao iniciar modulo Digicon")
            
        if not running_jboss:               
            print('Iniciando o Jboss!!!!')
            win32serviceutil.StartService(service_joboss, machine)  
            print('Jboss iniciado!!!!')            
             
        else:
            print('Falha ao iniciar Jboss')
        flash("Sucesso Start")    
    except:
        flash("FALHA Start") 
        
    return redirect (url_for('home'))
@app.route('/reset')
def reset():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d-%m-%Y %H-%M-%S')

    print("Parando o Jboss")
    win32serviceutil.StopService(service_joboss, machine)    
    time.sleep(3)
    print('Parando o Modulo BD')
    win32serviceutil.StopService(service_modulo_bd, machine)    
    time.sleep(3)
    print('Parando o Modulo Controle')
    win32serviceutil.StopService(service_modulo_controle, machine)    
    time.sleep(3)
    print('Parando o Modulo Digicon')
    win32serviceutil.StopService(service_modulo_digicon, machine)    
    time.sleep(3)
  

    def service_running_jboss(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_jboss = service_running_jboss(service_joboss, machine)

    def service_running_BD(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_BD =service_running_BD(service_modulo_bd, machine)
    def service_running_controle(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_controle =service_running_controle(service_modulo_controle, machine)
    def service_running_digicon(process_name, hostname):
        return win32serviceutil.QueryServiceStatus(process_name,hostname)[1]==4
    running_digicon =service_running_digicon(service_modulo_digicon, machine)
    
    try:
    
        if not running_BD:
            print('Iniciando modulo BD')
            win32serviceutil.StartService(service_modulo_bd, machine)
            time.sleep(1.5)
        else:
            print('Falha ao iniciar modulo BD!!')
        if not running_controle:
            print('Iniciando modulo Controle')
            win32serviceutil.StartService(service_modulo_controle, machine)
            time.sleep(1.5)
        else:
            print("Falha ao iniciar modulo controle")
        if not running_digicon:
            print('Iniciando modulo Digicon')
            win32serviceutil.StartService(service_modulo_digicon, machine)
            time.sleep(1.5)
        else:
            print("Falha ao iniciar modulo Digicon")
            
        if not running_jboss:               
            print('Jboss rodando!!!!')
            print('Renomeando log -- !!!!', data_e_hora_em_texto)
            os.rename('C:/ambiente_dev_windows/jboss-CTC-limpo/standalone/log', 'C:/ambiente_dev_windows/jboss-CTC-limpo/backup_ log/log-'+ data_e_hora_em_texto)
            print('Renomeado log!!!!')
            print('Iniciando o Jboss!!!!')
            win32serviceutil.StartService(service_joboss, machine)  
            print('Jboss iniciado!!!!')            
             
        else:
            print('Falha ao iniciar Jboss')
                
                            
        flash("Sucesso reset!") 
    except:
        flash("Falha Reset") 
        print('A execucao do serviço falhou!')

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
    print('Endereco download: ', enderecodownload)
    path = enderecodownload
    return send_file(path, as_attachment=True)
    flash("Sucesso Download")
    return redirect (url_for('home'))



@socketio.on('message')
def machine_recursos(message):
    print(message)
    while True:
        try:
            cpu_percent=psutil.cpu_percent(interval=1)
            ram_percent=psutil.virtual_memory()[2]
            process_name = "java.exe"
            mega_bytes=0
            for process in psutil.process_iter():
                if process.name() == process_name:
                    
                    process_int= process.pid
                    p = psutil.Process(process_int)
                    #mem=round(proc.memory_percent(),2)
                    ram_process=int(process.memory_info()[2])
                    ram_process_mb=round((ram_process/1023)*2,2)
                    cpu_process=p.cpu_percent(interval=1)
            dados_maquina={
                "cpu_total":cpu_percent,
                "ram_total":ram_percent,
                "cpu_process":cpu_process,
                "ram_process":ram_process_mb
            }
            json_dados_maquina=json.dumps(dados_maquina)        
            emit('message', json_dados_maquina)
        except:
            cpu_percent=psutil.cpu_percent(interval=1)
            ram_percent=psutil.virtual_memory()[2]
            process_name = "java.exe"
            mega_bytes=0
            for process in psutil.process_iter():
                if process.name() == process_name:
                    
                    process_int= process.pid
                    p = psutil.Process(process_int)
                    #mem=round(proc.memory_percent(),2)
                    ram_process=int(process.memory_info()[2])
                    ram_process_mb=int(ram_process/1024)
                    cpu_process=p.cpu_percent(interval=1)
            dados_maquina={
                "cpu_total":cpu_percent,
                "ram_total":ram_percent,
                "cpu_process":cpu_process,
                "ram_process":ram_process_mb
            }
            json_dados_maquina=json.dumps(dados_maquina)        
            emit('message', json_dados_maquina)
            time.sleep(10)
tsocket=threading.Thread(target=machine_recursos)
tsocket.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port= 5005)