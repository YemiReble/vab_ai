# VAB AI
- [x] Project
- [x] Python
- [x] Django
- [x] Openai
- [x] Assembly AI

## Introduction
Vab stands for Video, Audio to Blog, this is a program that uses generative artificial intelligence to read a video, audio file, transcribe the audio file and use the audio transcription to generate a blog article. User can then copy this article for proper editing and publishing.

## Instructions
To use this app:
- Install Python3 and pip
- Install Django
- Install Cohere AI
- Install Assembly AI

You should look into the requirements.txt file for more information, or check the [README.md](https://github.com/yemireble/vab_ai/blob/main/README.md)

## How to use
Clone the repo:
```bash/
git clone https://github.com/yemireble/vab_ai.git
```
#### For Linux user
running the app:
```bash
$ ./start_server.sh
```
#### For Windows user
running the app:
```bash
$ python start_server.py
```

## How it works
This is how it works:
- User paste a video link form Youtube
- vab_ai will download the video audio file
- vab_ai will generate tanscription of the audio file
- vab_ai will generate a blog article from the transcription
- User get the blog article
- User can copy the article for editing and publishing

## Author
*Sulaimon Abodunrin*
