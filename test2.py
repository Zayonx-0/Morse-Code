from pydub import AudioSegment

codefile_mp3 = "morse.mp3"
codefile_wav = "morsetest2.wav"
mcode = AudioSegment.from_mp3(codefile_mp3)
mcode.export(codefile_wav , format="wav")