#-*-coding: utf8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UploadFileForm
from django.core.files.uploadedfile import UploadedFile
#import csv
import os, sys, subprocess
from io import TextIOWrapper, BytesIO
from shutil import copyfile

def converte():#função para converter aquivos de texto linux para windows
    if os.path.exists("/home/ubuntu/workspace/rds/static/rds/Sintegra.txt"):#verificar caminhos no deploy
        subprocess.call('unix2dos /home/ubuntu/workspace/rds/static/rds/Sintegra.txt', shell = True)#verificar caminhos no deploy

#função para retornar os números das notas retirados no registro 50 #validada
def reg54():
    notas = ''
    with open('log.txt') as log:
        for linha in log:
            notas += linha[45:51]
            notas += '\n'
    return notas

#função para retornar os produtos do registro 75
def produto():
    produtos = ''
    with open('sem51.txt') as arquivo:
        for linha in arquivo:
            if linha[0:2] == '75':
                produtos += linha[18:32]
                produtos += '\n'
    return produtos

#função para retirar os registros 60D do arquivo
def reg60d(): 
    controle = 0
    with open('sem51.txt') as sintegra:#abre arquivo para leitura
        for linha in sintegra:
            if linha[0:2] == '75':
                controle = 0
                for nota in sintegra:
                    if nota[0:2] != ''
                    #if nota == linha[43:49]:
                        controle = 1
                if controle == 0:
                    with open('sem51.txt', 'a') as novo2:#abre arquivo para escrita no seu final, apendice
                        novo2.write(linha)
            else:
                with open('sem51.txt', 'a') as novo2:
                    novo2.write(linha)    

#função para retirar os registros 51 do arquivo
def reg51(): 
    controle = 0
    with open('new_sintegra.txt') as sintegra:#abre arquivo para leitura
        for linha in sintegra:
            if linha[0:2] == '51':
                controle = 0
                for nota in reg54().split():
                    if nota == linha[43:49]:
                        controle = 1
                if controle == 0:
                    with open('sem51.txt', 'a') as novo2:#abre arquivo para escrita no seu final, apendice
                        novo2.write(linha)
            else:
                with open('sem51.txt', 'a') as novo2:
                    novo2.write(linha)

def reg74(): #função para retirar os registros 54 referentes ao 50, funciona em conjunto com a função reg54()
    controle = 0
    with open('novo_sintegra.txt') as sintegra:#abre arquivo para leitura
        for linha in sintegra:
            if linha[0:2] == '54':
                controle = 0
                for nota in reg54().split():
                    if nota == linha[21:27]:
                        controle = 1
                if controle == 0:
                    with open('new_sintegra.txt', 'a') as novo2:#abre arquivo para escrita no seu final, apendice
                        novo2.write(linha)
            else:
                with open('new_sintegra.txt', 'a') as novo2:
                    novo2.write(linha)

def home(request):
        
    context = {}
    if request.method == 'POST':
        if request.FILES.get('arquivo'):
            f = request.FILES['arquivo']
            context['check'] = len(f.readlines())
            
            if os.path.exists("/home/ubuntu/workspace/rds/static/rds/Sintegra.txt"):#verifico se ja existe um sintegra e apago
                os.remove('/home/ubuntu/workspace/rds/static/rds/Sintegra.txt')
            if os.path.exists("/home/ubuntu/workspace/new_sintegra.txt"):
                os.remove('new_sintegra.txt')
            if os.path.exists("/home/ubuntu/workspace/log.txt"): #verifico se ja exite um log e apago
                os.remove('log.txt')
            if os.path.exists("/home/ubuntu/workspace/novo_sintegra.txt"):
                os.remove('novo_sintegra.txt')
            if os.path.exists("/home/ubuntu/workspace/sem51.txt"):
                os.remove('sem51.txt')
                
            for linha in f: #o for tira os registro 50 do sintegra criando um novo arquivo que posteriormente passara pela função reg74()
                if linha.decode('ascii')[0:2] == '50' and linha.decode('ascii')[40:43] == '011' and linha.decode('ascii')[55] == 'P':
                    with open('log.txt', 'a') as log:
                        log.write(linha.decode('ascii'))
                else:
                    with open('novo_sintegra.txt', 'a') as novo:
                        novo.write(linha.decode('ascii'))
            context['controle'] = 1
            try:#Verifica se o arquivo é um sintegra atraves do arquivo de log
                with open('log.txt') as log:
                    context['D1'] = len(log.readlines())
            except:
                context['controle'] = 2
                pass
            try:
                reg74()
                reg51()
            except:
                pass
            context['form'] = UploadFileForm()
        if context['controle'] == 1:
            copyfile('/home/ubuntu/workspace/sem51.txt', '/home/ubuntu/workspace/rds/static/rds/Sintegra.txt')#copio o novo sintegra para a pasta static para que o usuario possa fazer download
            converte()#depois de copiado o arquivo é convertido para windows conforme descrição na função
        return render(request, 'rds/home.html', context)
    else:
        context['controle'] = 0
        context['form'] = UploadFileForm()
        return render(request, 'rds/home.html', context)