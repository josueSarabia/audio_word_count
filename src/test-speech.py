import speech_recognition as sr
from os import path, getcwd, mkdir
from pydub import AudioSegment
from pydub.silence import split_on_silence
from textblob import TextBlob

BASE_PATH = getcwd()
VOCABULARY = []

def mp3_to_text(file_path):
    # convert mp3 file to wav                                                       
    sound_mp3 = AudioSegment.from_mp3(file_path)

    sound_mp3 = sound_mp3.set_channels(1) # mono
    sound_mp3 = sound_mp3.set_frame_rate(16000) # 16000Hz
    
    # create new .wav file path
    file_wav_format_path = path.join(BASE_PATH, 'transcript.wav')
    
    # export the mp3 to .wav inside the project
    sound_mp3.export(file_wav_format_path, format="wav")

    # open the audio file using pydub 
    sound = AudioSegment.from_wav(file_wav_format_path)

    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-16,
        keep_silence=500,
    )

    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not path.isdir(folder_name):
        mkdir(folder_name)
    whole_text = ""

    # create a speech recognition object
    r = sr.Recognizer()

    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        print("saving chunk{0}.wav".format(i))
        chunk_filename = path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        print("Processing chunk "+str(i))
        """ # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", e)
            except sr.RequestError as e:
                print("Could not request results. check your internet connection")
            else:
                whole_text += text + ' ' """
    # return the text for all chunks detected
    return whole_text

def delete_new_line_char(element):
    return element.replace('\n', '')

def get_vocabulary(path):
    file = open(path, 'r')
    lines = file.readlines()
    result = map(delete_new_line_char, lines)

    return list(result)

def get_sentiment(text):
    blob = TextBlob(text)
    print('blob.sentiment: ', blob.sentiment)
    sentiment = blob.sentiment.polarity
    return sentiment

def get_word_count(text):
    result = {}
    blob = TextBlob(text)
    for word in VOCABULARY:
        print(word)
        result[word] = blob.words.count(word)
    
    return result


def main():
    
    file_path = input('Type the mp3 file path: ')
    """ vocabulary_path = input('Type the vocabulary file path: ') """

    # read mp3 file path
    text = mp3_to_text(file_path)
    print('text: ', text)

    """ # read user vocabulary
    global VOCABULARY 
    VOCABULARY = get_vocabulary(vocabulary_path)
    print(VOCABULARY)

    # get sentiment. s > 0.2 positive, s < -0.2 negative, -0.2 > s < 0.2 neutral
    sentiment = get_sentiment(text)
    print('sentiment', sentiment)

    # get word count
    word_count = get_word_count(text)
    print('word_count: ', word_count) """

main()
