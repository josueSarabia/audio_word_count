## About The Project
an API that receives an MP3 file and transcribes it, runs it through a natural language processor to identify sentiment and provide a word count. The system should look for words configured by a user and create an output of the number of times this word was used, and the time stamp the word was used on the recording


## Getting Started

the app needs ffmpeg. it can be found here: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
you also need to download nltk tools for textblob
* npm
  ```sh
  nltk.download() or python3 -m textblob.download_corpora
  ```
## Usage

the API docs can be found here: [https://audio-to-text-inktel.herokuapp.com/docs](https://audio-to-text-inktel.herokuapp.com/docs)

# upload vocabulary

### Request

`POST https://audio-to-text-inktel.herokuapp.com/upload-vocabulary`
 
 receives a .txt file. every line must be only one word.
 
 # upload audio

### Request

`POST https://audio-to-text-inktel.herokuapp.com/upload-audio`
 
 receives a mp3 file.
 
 ### Response
    {
        "sentiment": "NEUTRAL",
        "text": "",
        "freq": {
            "word1": {
                "freq": 6,
                "timestamps": [
                    "00:00:03:",
                ]
            },
            "word2": {
                "freq": 1,
                "timestamps": [
                    "00:00:07:"
               ]
            },
        },
        "UUID": "06dbed83-8bd2-4b1b-a009-7a9d06cedf0d"
    }

# get result by id
 
### Request

`GET https://audio-to-text-inktel.herokuapp.com/result/06dbed83-8bd2-4b1b-a009-7a9d06cedf0d`
 
### Response
    {
        "sentiment": "NEUTRAL",
        "text": "",
        "freq": {
            "word1": {
                "freq": 6,
                "timestamps": [
                    "00:00:03:",
                ]
            },
            "word2": {
                "freq": 1,
                "timestamps": [
                    "00:00:07:"
               ]
            },
        },
        "UUID": "06dbed83-8bd2-4b1b-a009-7a9d06cedf0d"
    }
