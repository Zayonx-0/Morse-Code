from scipy.io import wavfile
#from pydub import AudioSegment
#sound = AudioSegment.from_mp3("./morse.mp3")
#sound.export("./morse.wav", format="wav")
samplerate, data = wavfile.read('./morse.wav')
import math

realdata = []


for i in data:
    realdata += [i]
    print(i)

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
                print(SupposedFinalSilence)
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

BeepTime = determineBeepTime(realdata)


# Si c'est inferieur à 500 pendant au moins 10 fois, c'est un silence.

def Analyzer(BeepTime, realdata):
    index = 0
    row = 0
    current = 0

    while index < len(realdata):
        realdata[index]