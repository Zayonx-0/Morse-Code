from scipy import signal
from scipy.io import wavfile


sample_rate, samples = wavfile.read('test3.wav') # FICHIER .WAV A METTRE ICI !
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

def most_frequent(List):
    counter = 0
    num = List[0]  
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
  
    return num

def most_frequent2nd(List):
    firstone = float(most_frequent(List))
    counter = 0
    num = List[0]  
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter) and i != firstone:
            counter = curr_frequency
            num = i
  
    return num


SortedFrequencies = []
SortedSpectrogram = []
SortedTimes = []

for t in range(len(times)):
    max = [0]
    for f in range(len(frequencies)):
        if max[0] <= spectrogram[f][t]:
            max = []
            max.append(spectrogram[f][t])
            max.append(times[t])
            max.append(frequencies[f])
    SortedSpectrogram.append(max[0])
    SortedTimes.append(max[1])
    SortedFrequencies.append(max[2])

average = sum(SortedSpectrogram) / len(SortedSpectrogram)
plusutilisee = most_frequent(SortedFrequencies)
plusutilisee2 = most_frequent2nd(SortedFrequencies)

def LoudestFrequency(): # Fonction servant à définir quelle est la fréquence à écouter, car la plus utilisée peut être celle qui définit les silences. 
    firstloudest = 0
    secondloudest = 0
    for i in range(len(SortedSpectrogram)):
        if SortedFrequencies[i] == plusutilisee:
            firstloudest += SortedSpectrogram[i]
        elif SortedFrequencies[i] == plusutilisee2:
            secondloudest += SortedSpectrogram[i]
    return firstloudest,secondloudest

LoudestFrequencyResult = LoudestFrequency()


def DetermineBeepTime(list): # Cette fonction permet de déterminer le temps d'un Beep dans le fichier audio actuel, le temps donc d'un . dans un code morse.
    if LoudestFrequencyResult[0] > LoudestFrequencyResult[1]:
        ToUse = plusutilisee
    else:
        ToUse = plusutilisee2
    index = 0
    while SortedFrequencies[index] != ToUse:
        index += 1
    while SortedFrequencies[index] == ToUse:
        index += 1
    FirstTime = float(SortedTimes[index])
    while SortedFrequencies[index] != ToUse:
        index += 1
    SecondTime = float(SortedTimes[index])
    FirstOne = SecondTime - FirstTime
    SecondOne = 1
    for e in range(len(list)):
        if list[e][1] < SecondOne:
            SecondOne = list[e][1]
    if SecondOne > 1 or SecondOne < 0.01:
        return FirstOne
    else:
        return SecondOne



def Translate(most_frequent2,average,most_frequent):
    index = 0
    translated = []
    last = 0
    timeSaved = []
    while SortedFrequencies[index] != most_frequent:
        index += 1
    
    while index < len(SortedFrequencies):
        if SortedFrequencies[index] != most_frequent and SortedFrequencies[index] != most_frequent2 and index + 1< len(SortedFrequencies):
            index += 1
        if SortedFrequencies[index] == most_frequent or SortedSpectrogram[index] > average:
            timeSaved = SortedTimes[index]
            while (SortedFrequencies[index] == most_frequent or SortedSpectrogram[index] > average) and index + 1< len(SortedFrequencies):
                index += 1
            translated.append(['Noise',float(SortedTimes[index]) - timeSaved])
        else:
            timeSaved = SortedTimes[index]
            while (SortedFrequencies[index] == most_frequent2 or SortedSpectrogram[index] < average) and index + 1< len(SortedFrequencies):
                index += 1
            translated.append(['Silence',float(SortedTimes[index]) - timeSaved])
        if index == len(SortedFrequencies) - 1:
            return translated


if LoudestFrequencyResult[0] > LoudestFrequencyResult[1]:
    firstdone = Translate(plusutilisee2,average,plusutilisee)
else:
    firstdone = Translate(plusutilisee,average,plusutilisee2)

def finalTranslate(BeepTime, TimeList):
    finaltranslated = []
    for i in range(len(TimeList)):
        if TimeList[i][0] == 'Noise':
            if TimeList[i][1] > BeepTime - 0.05:
                if TimeList[i][1] > BeepTime * 2 and TimeList[i][1] < BeepTime * 5:
                    finaltranslated.append('-')
                    print('-',end='')
                else:
                    finaltranslated.append('.')
                    print('.',end='')
        else:
            if TimeList[i][1] < BeepTime * 2:
                print('',end='')
            elif TimeList[i][1] > BeepTime * 5:
                finaltranslated.append('_')
                print('_', end='')
            else:
                finaltranslated.append(' ')
                print(' ',end='')
    return finaltranslated



BeepTime = DetermineBeepTime(firstdone)
print(BeepTime)
toNormalize = finalTranslate(BeepTime,firstdone)

morse = {'.-': 'A',   '-...': 'B',   '-.-.': 'C',
      '-..': 'D',      '.': 'E',   '..-.': 'F',
       '-.': 'G',   '....': 'H',     '..': 'I',  
     '.---': 'J',    '-.-': 'K',   '.-..': 'L',
       '--': 'M',     '-.': 'N',    '---': 'O', 
     '.--.': 'P',   '--.-': 'Q',    '.-.': 'R',
      '...': 'S',      '-': 'T',    '..-': 'U', 
     '...-': 'V',    '.--': 'W',   '-..-': 'X',
     '-.--': 'Y',   '--..': 'Z',  '-----': '0', 
    '.----': '1',  '..---': '2',  '...--': '3',
    '....-': '4',  '.....': '5',  '-....': '6', 
    '--...': '7',  '---..': '8',  '----.': '9',
    '.-.-.-':'.',  '--..--':',',  '..--..':'?',
    '.---.':"'",   '-.-.--':'!',   '-.--.':'(',
    '-.--.-':')',   '.--.-.':'@', '...-..-':'$'}

def normalizer(list):
    index = 0
    translated = ''
    totranslate = ''
    while index < len(list):
        if list[index] == ' ':
            translated += morse[totranslate]
            totranslate = ''
            index += 1
        elif list[index] == '_':
            translated += morse[totranslate]
            translated += ' '
            totranslate = ''
            index += 1
        else:
            totranslate += list[index]
            index += 1
    if len(totranslate) > 0:
        translated+= morse[totranslate]

    return translated
        
print(normalizer(toNormalize))