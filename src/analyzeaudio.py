from os import path, getcwd, mkdir
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import mediainfo
from textblob import TextBlob

import wave
from json import loads, dump
from vosk import Model, KaldiRecognizer

VOCABULARY_NAME = "vocabulary.txt"
FOLDER_NAME = "audio-chunks"

# add path path.dirname(getcwd())
model_path = path.join(getcwd(), "vosk-model-small-en-us-0.15")
model = Model(model_path)


def delete_new_line_char(element):
    return element.replace('\n', '')

def get_vocabulary(path):
    file = open(path, 'r')
    lines = file.readlines()
    result = map(delete_new_line_char, lines)

    return list(result)

def mp3_to_wav(file_path, base_path):
    # convert mp3 file to wav                                                       
    sound_mp3 = AudioSegment.from_mp3(file_path)

    sound_mp3 = sound_mp3.set_channels(1) # mono
    sound_mp3 = sound_mp3.set_frame_rate(16000) # 16000Hz
    
    # create new .wav file path
    file_wav_format_path = path.join(base_path, 'transcript.wav')
    
    # export the mp3 to .wav inside the project
    sound_mp3.export(file_wav_format_path, format="wav")

    return file_wav_format_path

def generate_wav_chunks(file_path, base_path):
    
    audio_chunks_path = path.join(base_path, FOLDER_NAME)
    # open the audio file using pydub 
    sound = AudioSegment.from_wav(file_path)

    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-16,
        keep_silence=500,
    )

    
    # create a directory to store the audio chunks
    if not path.exists(audio_chunks_path):
        mkdir(audio_chunks_path)

    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `FOLDER_NAME` directory.
        print("saving chunk{0}.wav".format(i))
        chunk_filename = path.join(audio_chunks_path, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

    return len(chunks)

def analyze_chunk(file_path):
    wf = wave.open(file_path, "rb")
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
            part_result = loads(rec.Result())
            results.append(part_result)
    part_result = loads(rec.FinalResult())
    results.append(part_result)
    wf.close()  # close audiofile 

    return {
        "results": results,
        "duration": mediainfo(file_path)['duration']
    }

def transform_timestamp(timestamp):
    result = ""
    hours = timestamp / 3600
    
    # get hours
    if  hours < 1:
        result += "00:"
    else:
        int_hours = int(hours)
        if int_hours < 10:
            result += "0" + str(int_hours) + ":"
        else:
            result += str(int_hours) + ":"
    
    # get minutes
    minutes = (hours - int(hours)) * 60
    if minutes < 1:
        result += "00:"
    else:
        int_minutes = int(minutes)
        if int_minutes < 10:
            result += "0" + str(int_minutes) + ":"
        else:
            result += str(int_minutes) + ":"

    # get seconds
    seconds = (minutes - int(minutes)) * 60
    int_seconds = int(seconds)
    if int_seconds < 10:
        result += "0" + str(int_seconds) + ":"
    else:
        result += str(int_seconds) + ":"
    
    return result

def add_chunk_results(results, whole_text, result_dict, overall_timestamp, vocabulary):
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        
        whole_text += ' ' + sentence['text']
        for obj in sentence['result']:
            word = obj["word"]
            timestamp = obj["start"]
            if word in vocabulary:
                if word in result_dict:
                    result_dict[word]["freq"] += 1
                    human_readable_timestamp = transform_timestamp(overall_timestamp + timestamp)
                    result_dict[word]["timestamps"].append(human_readable_timestamp)
                else:
                    human_readable_timestamp = transform_timestamp(overall_timestamp + timestamp)
                    result_dict[word] = {
                        "freq": 1,
                        "timestamps": [human_readable_timestamp]
                    }
    return {
        "text": whole_text,
        "dict": result_dict
    }

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

def save_to_json(dictionary, base_path):
    json_path = path.join(base_path, 'results.json')
    with open(json_path, "w") as outfile:
        dump(dictionary, outfile, indent = 4)

def analyze_audio(file_path, base_path):
    vocabulary = []

    # read user vocabulary
    # path.dirname(getcwd())
    vocabulary_path = path.join(getcwd(), VOCABULARY_NAME)
    vocabulary = get_vocabulary(vocabulary_path)

    # conver mp3 file to wav
    wav_file_path = mp3_to_wav(file_path, base_path)

    # split the wav file in chunks
    number_of_chunks = generate_wav_chunks(wav_file_path, base_path)

    whole_text = ""
    result_dict = {}
    overall_timestamp = 0
    #loop chunks
    for i in range(number_of_chunks):

        # get chunk text and timestamps
        chunk_path = path.join(base_path, FOLDER_NAME, f"chunk{i + 1}.wav")
        audio_results = analyze_chunk(chunk_path)

        # add text and timestamps to current reuslts
        results = add_chunk_results(audio_results["results"], whole_text, result_dict, overall_timestamp, vocabulary)

        # update variables with new results
        whole_text = results["text"]
        result_dict = results["dict"]
        chunk_duration = audio_results["duration"].split('.')[0]
        overall_timestamp += float(chunk_duration)

    # get sentiment from text
    sentiment_value = get_sentiment(whole_text)

    # translate sentiment to positive, negative or neutral
    sentiment = ""
    if sentiment_value >= 0.2:
        sentiment = "POSITIVE"
    elif sentiment_value <= -0.2:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    results_dict =  {
        "sentiment": sentiment,
        "text": whole_text,
        "freq": result_dict
    }

    # save results to json file
    save_to_json(results_dict, base_path)

    return results_dict
