import os
import speech_recognition as sr
import ffmpeg

import openai
import re

command2mp3 = "ffmpeg -i /YourFolder/FileName.mp4 /YourFolder/FileName.mp3"
command2wav = "ffmpeg -i /YourFolder/FileName.mp3 /YourFolder/FileName.wav"

os.system(command2mp3)
os.system(command2wav)

# Set the chunk size and the audio file path
chunk_size = 1024
audio_file = "/YourFolder/FileName.wav"

full_text = ""

# Initialize the recognizer
r = sr.Recognizer()

# Open the audio file
with sr.AudioFile(audio_file) as source:
    # Iterate over the audio chunks
    while True:
        # Read the chunk from the audio file
        chunk = source.stream.read(chunk_size)
        
        # Exit the loop if there is no more data to read
        if len(chunk) == 0:
            break
        
        # Feed the chunk to the recognizer
        r.adjust_for_ambient_noise(source)
        r.operation_timeout = 1000
        r.pause_threshold = 5.0
        audio = r.record(source, duration=120)

        # Print the recognized text
        full_text += r.recognize_google(audio)
        
# Set up OpenAI API key and model
openai.api_key = "YourKey"
model_engine = "text-davinci-002"

# Define function to punctuate a text string
def punctuate_text(text):
    # Split the text into chunks of 2048 characters or less
    text_chunks = re.findall(r".{1,2048}(?:\s|$)", text)

    # Initialize the punctuated text string
    punctuated_text = ""

    # Punctuate each chunk of text and append it to the punctuated text string
    for chunk in text_chunks:
        prompt = f"Punctuate and break it into readable paragraphs the following text:\n{chunk}"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        punctuated_chunk = response.choices[0].text.strip()
        punctuated_text += punctuated_chunk

    # Return the punctuated text string
    return punctuated_text

# usage
punctuated_article = punctuate_text(full_text)
print(punctuated_article)
