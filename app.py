import flask_socketio
from flask import Flask, render_template,redirect, url_for, send_from_directory, flash
from flask_socketio import SocketIO
from flask_socketio import send, emit
import psutil
import os
import sys
import json
import subprocess
from datetime import datetime
import datetime
import time
from flask import send_file
import socket
import win32serviceutil
import threading


app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '@11tahe89!'
socketio = SocketIO(app)

hostname = socket.gethostname()
service='JBMAXIMUS'
machine=hostname
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stop')
def stop():   
    try:
        #subprocess.Popen(endereco_stop)
        win32serviceutil.StopService(service, machine)
        flash("Sucesso Stop")
    except:
        flash("Falha Stop")
        print('A execucao do .bat falhou, check o endereco do arquivo .bat')
    return redirect (url_for('home'))
@app.route('/start')
def start(): 
    try:
        win32serviceutil.StartService(service, machine)
        flash("Sucesso Start")    
    except:
        flash("FALHA Start") 
        print('A execucao do .bat falhou, check o endereco do arquivo .bat')
    return redirect (url_for('home'))
@app.route('/reset')
def reset():   
    try:
        #subprocess.Popen(endereco_reset)
        win32serviceutil.RestartService(service, machine)
        flash("Sucesso Reset")    
    except:
        flash("falha Reset") 
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
            time.sleep(2)
tsocket=threading.Thread(target=machine_recursos)
tsocket.start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port= 5005)