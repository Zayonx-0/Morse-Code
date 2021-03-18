#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:53:36 2021

@authors: Matteo
"""

"""Il faut au préalable avoir installé ffmpeg sur la machine linux
avec la commande sudo apt install ffmpeg"""

import os 

path='/home/user/Documents/NSI/Projet Morse/'
nomfichier='audio.mp3'
nomsortie="sortie"


def conversionEnWav(path,nomFichier,nomDeSortie,affichertermine=True):
    os.system(f"ffmpeg -i '{path}{nomFichier}' '{nomDeSortie}.wav'")
    if affichertermine:
        print('conversion terminee')
    
conversionEnWav(path,nomfichier,nomsortie)