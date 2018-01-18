#-*-coding: utf8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from django.core.files.uploadedfile import UploadedFile
import os, sys, subprocess
from io import TextIOWrapper, BytesIO
from shutil import copyfile

def converte():#função para converter aquivos de texto linux para windows
    if os.path.exists("ultimo.txt"):#verificar caminhos no deploy
        subprocess.call("unix2dos ultimo.txt", shell = True)#verificar caminhos no deploy

#função para retornar os números das notas retirados no registro 50 #validada
def reg54():
    notas = ''
    with open('log.txt') as log:
        for linha in log:
            notas += linha[45:51]
            notas += '\n'
    return notas
    
#função para contar os registros    
def conta():
    reg50 = 0
    reg51 = 0
    reg53 = 0
    reg54 = 0
    reg60 = 0
    reg61 = 0
    reg70 = 0
    reg74 = 0
    reg75 = 0
    with open('sem5160d.txt') as sintegra:
        for linha in sintegra:
            if linha[0:2] == '50':
                reg50 += 1
            if linha[0:2] == '51':
                reg51 += 1
            if linha[0:2] == '53':
                reg53 += 1
            if linha[0:2] == '54':
                reg54 += 1
            if linha[0:2] == '60':
                reg60 += 1
            if linha[0:2] == '61':
                reg61 += 1
            if linha[0:2] == '70':
                reg70 += 1
            if linha[0:2] == '74':
                reg74 += 1
            if linha[0:2] == '75':
                reg75 += 1
    while len(str(reg50)) < 8:
        reg50 = str(0) + str(reg50)
        
    while len(str(reg51)) < 8:
        reg51 = str(0) + str(reg51)
        
    while len(str(reg53)) < 8:
        reg53 = str(0) + str(reg53)
        
    while len(str(reg54)) < 8:
        reg54 = str(0) + str(reg54)
        
    while len(str(reg60)) < 8:
        reg60 = str(0) + str(reg60)
        
    while len(str(reg61)) < 8:
        reg61 = str(0) + str(reg61)
        
    while len(str(reg70)) < 8:
        reg70 = str(0) + str(reg70)
        
    while len(str(reg74)) < 8:
        reg74 = str(0) + str(reg74)
    
    while len(str(reg75)) < 8:
        reg75 = str(0) + str(reg75)
        
        
    
    with open('sem5160d.txt') as sintegra:
        for linha in sintegra:
            if linha[0:2] != '90':
                arquivo = open('ultimo.txt', 'a')
                arquivo.write(linha)
                arquivo.close()
            else:
                arquivo = open('ultimo.txt')
                cnpj = linha[0:30]
                arquivo.close()
                
    
    with open('ultimo.txt', 'a') as arquivo:
        linha = str(cnpj)
        linha += '50'+reg50
        linha += '51'+reg51
        linha += '53'+reg53
        linha += '54'+reg54
        linha += '60'+reg60
        linha += '61'+reg61
        linha += '70'+reg70
        linha += '74'+reg74
        linha += '75'+reg75
        linha += '     2'
        linha += '\n'
        arquivo.write(linha)
    
    sintegra = open('ultimo.txt')
    total = len(sintegra.readlines())
    sintegra.close()
    total += 1
    while len(str(total)) < 8:
        total = str(0) + str(total)
    linha = str(cnpj)
    linha += '99'+total
    linha += '                                                                                     2'
    arquivo = open('ultimo.txt', 'a')
    arquivo.write(linha)
    arquivo.close()    

    
    

#função que devolve registro que possa ter referência no registro 75
def teste():
    registros = ''
    arquivo = open('sem51.txt')
    for linha in arquivo:
        if  linha[0:2] == '54' or linha[0:3] == '60D' or linha[0:3] == '60I' or linha[0:3] == '61R' or linha[0:2] == '74':
            registros += linha
            registros += '\n'
    arquivo.close()
    return registros

#função para retirar registros 75 não referenciados no sintegra                
def reg60d2(): 
    f = open('sem51.txt')
    reg = teste()
    for linha in f:
        if linha[0:2] == '75':
            if linha[18:32] in reg:
                fnovo = open('sem5160d.txt', 'a')
                fnovo.write(linha)
                fnovo.close()
            else:
                log = open('log.txt', 'a')
                log.write(linha)
                log.close()
        else:
            fnovo = open('sem5160d.txt', 'a')
            fnovo.write(linha)
            fnovo.close()
    f.close()

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
            if os.path.exists("new_sintegra.txt"):
                os.remove('new_sintegra.txt')
            if os.path.exists("log.txt"): #verifico se ja exite um log e apago
                os.remove('log.txt')
            if os.path.exists("novo_sintegra.txt"):
                os.remove('novo_sintegra.txt')
            if os.path.exists("sem51.txt"):
                os.remove('sem51.txt')
            if os.path.exists("sem5160d.txt"):
                os.remove('sem5160d.txt')
            if os.path.exists("ultimo.txt"):
                os.remove('ultimo.txt')
                
            for linha in f: #o for tira os registro 50 do sintegra criando um novo arquivo que posteriormente passara pela função reg74()
                if linha.decode('ascii')[0:2] == '50' and linha.decode('ascii')[40:44] == '01D1' and linha.decode('ascii')[55] == 'P':
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
                reg60d2()
                conta()
            except:
                pass
            context['form'] = UploadFileForm()
        #if context['controle'] == 1:
        #    converte()#depois de copiado o arquivo é convertido para windows conforme descrição na função
        mostrar = ''
        file = open('ultimo.txt')
        for linha in file.readlines():
            mostrar += linha
            mostrar += '\r\n'
        response = HttpResponse(mostrar,content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="Sintegra.txt"'
        return response
    else:
        context['controle'] = 0
        context['form'] = UploadFileForm()
        return render(request, 'rds/home.html', context)