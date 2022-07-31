import wave
import json
from os import path, getcwd

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

BASE_PATH = getcwd()
model_path = "./vosk-model-small-en-us-0.15"



model = Model(model_path)
wf = wave.open(r"C:\Users\AMD\Desktop\audio_word_count\audio-chunks\chunk1.wav", "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

print(results)
# convert list of JSON dictionaries to list of 'Word' objects
list_of_words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition 
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence['result']:
        print(obj["word"],)
        """ w = {
            "conf": obj["conf"],
            "end": obj["end"],
            "start": obj["start"],
            "word": obj["word"],
        }  # create custom Word object
        list_of_words.append(w)  # and add it to list """

wf.close()  # close audiofile
""" 
# output to the screen
for word in list_of_words:
    print(word) """