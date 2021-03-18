from scipy.io import wavfile
#from pydub import AudioSegment
#sound = AudioSegment.from_mp3("./morse.mp3")
#sound.export("./morse.wav", format="wav")
samplerate, data = wavfile.read('./morse.wav')

realdata = []


for i in data:
    realdata += [i]

def determineBeepTime(realdata):
    SupposedSilence = 0
    SupposedFinalSilence = 0
    Row = 0

    index = 0
    while abs(realdata[index]) < 500: # Skip 1er silence
        index += 1
    
    while index < len(realdata):
        if abs(realdata[index]) > 500:
            if SupposedFinalSilence < SupposedSilence:
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
    return Analyze
    for i in range(len(Analyze)):
        if abs(Analyze[i]) > 500:
            return i

print(FinalSilenceTime(realdata))