#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:53:36 2021

@authors: Matteo
"""

"""Il faut installer ffmpeg au préalable sur la machine
et installer scipy : pip install scipy
et pyaudio : pip install PyAudio"""



import os 
from scipy.io import wavfile
import math
import pyaudio
import numpy as np
from scipy.io.wavfile import write

Dic={'A':'.-',
    'B':'-...',
    'C':'-.-.',
    'D':'-..',
    'E':'.',
    'F':'..-.',
    'G':'--.',
    'H':'....',
    'I':'..',
    'J':'.---',
    'K':'-.-',
    'L':'.-..',
    'M':'--',
    'N':'-.',
    'O':'---',
    'P':'.--.',
    'Q':'--.-',
    'R':'.-.',
    'S':'...',
    'T':'-',
    'U':'..-',
    'V':'...-',
    'W':'.--',
    'X':'-..-',
    'Y':'-.--',
    'Z':'--..',
    '1':'.----',
    '2':'..---',
    '3':'...--',
    '4':'....-',
    '5':'.....',
    '6':'-....',
    '7':'--...',
    '8':'---..',
    '9':'----.',
    '0':'-----'}
nomfichier=input('Entrez le nom du fichier : ')
nomsortie=input("Entrez le nom de sortie : ")

def conversionEnWav(nomFichier,nomDeSortie,affichertermine=True):
    try:
        commande="ffmpeg -ac 1 -i "+nomFichier+" "+nomDeSortie
        print(commande)
        os.system(commande)
        if affichertermine:
            print('conversion terminee')
    except Exception:
        print("Une erreur est survenue")
        print(Exception)
    
conversionEnWav(nomfichier,nomsortie)

samplerate, data = wavfile.read(nomsortie)


realdata = []


for i in data:
    realdata += [i]

def determineBeepTime(realdata):
    SupposedSilence = 0
    SupposedFinalSilence = math.inf

    index = 0
    while abs(realdata[index]) < 500: # Skip 1er silence
        index += 1

    finaldata = FinalSilenceTime(realdata)
    while index < finaldata:
        if abs(realdata[index]) > 500:
            if SupposedFinalSilence > SupposedSilence and SupposedSilence > 10:
                SupposedFinalSilence = SupposedSilence
            SupposedSilence = 0
            index += 1
            continue
        if abs(realdata[index]) <= 500:
            SupposedSilence += 1
            index += 1
    return SupposedFinalSilence

def FinalSilenceTime(realdata):
    Analyze = realdata[::-1]
    for i in range(len(Analyze)):
        if abs(Analyze[i]) > 500:
            return len(realdata) - i


def CheckLastTen(index, realdata):
    current = abs(realdata[index])
    if current < 500:
        for i in range(0,10):
            if realdata[index-i] < 500:
                continue
            else:
                return False # Means that last 10 are NOT the same
    else:
        for i in range(0,10):
            if realdata[index-i] > 500:
                continue
            else:
                return False

    return True # last 10 ARE the same ! It means that there are nothing worng here. (Like bit of err)

BeepTime = determineBeepTime(realdata)# 676 dans cet exemple. 

# But : reconnaitre un ., un - et reconnaitre 5 . d'espace, qui signale une autre lettre.
# Creer un Array de type : ['.','-','.','-',''/.....]
# Maybe time everything ? Like there is sound for 500 sample rate ?
# /..... = Espacement de deux lettres. 

def test(realdata,samplerate,index):
    #print('y')
    var = 0
    try:
        var = realdata[index+(samplerate/1000)]
    except Exception:
        #print(Exception)
        return False
    counter = 0
    for i in range(index, index+samplerate/1000):
        if abs(realdata[i]) < 800:
            counter += 1
    if counter > (samplerate / 1000) / 2:
        return True
    else:
        return False
    
def Analyzer(BeepTime, realdata):
    index = 10
    Array = [0]
    ArrayIndex = 0
    last = ['']
    while index < len(realdata):
        # 500 Is the treshold, over 500 and we have a noise; under and we have silence
        if test(realdata, samplerate, index): #Maybe try to do something according to the samplerate
            if last[ArrayIndex] == 'Silence':
                Array[ArrayIndex] = Array[ArrayIndex] + 1
            else:
                ArrayIndex +=1
                last.append('Silence')
                Array.append(1)
        else:
            if last[ArrayIndex] == 'Noise':
                Array[ArrayIndex] = Array[ArrayIndex] + 1
            else:
                ArrayIndex +=1
                last.append('Noise')
                Array.append(1)
        index += 1
    return Array, last

result = Analyzer(BeepTime, realdata)
NoiseTimes = result[0]
NoiseNature = result[1]

def translator(NoiseTimes, NoiseNature):
    translated = []
    for i in range(len(NoiseNature)):
        if NoiseNature[i] == 'Silence':
            if NoiseTimes[i] > BeepTime - 50 and NoiseTimes[i] < BeepTime + 50:
                translated.append('')
            elif NoiseTimes[i] > BeepTime * 5:
                translated.append(' ')
        else:
            if NoiseTimes[i] > BeepTime - 50 and NoiseTimes[i] < BeepTime + 50:
                translated.append('.')
            elif NoiseTimes[i] > BeepTime * 2:
                translated.append('-')
    return translated

def create(text,output):
    sample_rate = 11025
    frequency = 10000
    data=np.array([])
    petit_temps=sample_rate//10

    for i in text:
        if i.upper() in Dic: #si il est dans le dictionnaire
            for j in Dic[i.upper()]:#chaque valeur de morse
                if j=='.':
                    print('.',end='')
                    #ajouter un point
                    for i in range(petit_temps):
                        data=np.append(data,frequency*math.sin(i))

                elif j=='-':
                    print('-',end='')
                    #ajouter un tiret
                    for i in range(3*petit_temps):
                        data=np.append(data,frequency*math.sin(i))
                for i in range(petit_temps):
                        data=np.append(data,0)
            print(' ',end='')
            for i in range(2*petit_temps):#2en plus du précédent soit 3 au total
                        data=np.append(data,0)
        elif i == " ":
            print('| ',end='')
            #ajouter grand temps
            for i in range(4*petit_temps):#4 en plus des précédents soit 7 au total 
                        data=np.append(data,0)
        
    
    data=np.asarray(data, dtype=np.int16)
    #for dtype=int16 ==> min : -32768 / max : 32767
    write(output, sample_rate, data.astype(np.int16))
create('test','salut2.wav')

toprint = ''

done = translator(NoiseTimes, NoiseNature)

for i in range(len(done)):
    toprint += done[i]

print(toprint)