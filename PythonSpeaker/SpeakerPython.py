#-----------------------------------
#-----------------------------------
#History:
#23.12.2020 - Created by Akeeper
#-----------------------------------
#-----------------------------------
#-----------------------------------
import wave;
import requests;
import contextlib;
import xml.etree.ElementTree as ET

from dict2xml import dict2xml as xmlify
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat;
from azure.cognitiveservices.speech.audio import AudioOutputConfig;

#Считываение текста с файла
filename = input("Enter the filename (text.txt): ");
file = open(filename, "r");
text = file.read();
textLen = len(text);
file.close();
print("Your text: " + text)


key = "2289141bea2d44bf8e1fcb140acc8fa9" 
auth_url = "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
lang_url = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
auth_headers = { "ocp-apim-subscription-key": key, "content-length": "0", "content-type": "application/x-www-form-urlencoded" }

#Получение токена
auth_response = requests.post(auth_url, headers=auth_headers)

if (auth_response.status_code == 200):
    print("Program connected to services, token received and stored");
else:
    print("Program cant connect to services...");

token = auth_response.text
f = open("token.txt", "w").write(token)
lang_headers= { "authorization": "bearer " + token }

#Получение дикторов
lang_response = requests.get(lang_url, headers=lang_headers)
json_langs = lang_response.json()

#Выбор диктора
speakerNumStr = input("Enter the number of speaker (0-206), : ");
speakerNumInt = int(speakerNumStr);
selectedSpeaker = json_langs[speakerNumInt];
print("You selected: \n" 
      + "Short Name: " + selectedSpeaker["ShortName"] + "\n" 
      + "Locale: " + selectedSpeaker["Locale"])

#Составление и сохранение файла настроек произношения текста
Speak = ET.Element("speak")
Speak.set("version", "1.0")
Speak.set("xmlns", "https://www.w3.org/2001/10/synthesis")
Speak.set("xml:lang", selectedSpeaker["Locale"])
Voice = ET.SubElement(Speak,"voice")
Voice.set("name", selectedSpeaker["ShortName"])
Prosody = ET.SubElement(Voice,"prosody")
Prosody.set("rate", "0.9")
Prosody.text = text

SpeakTree = ET.ElementTree(Speak);
SpeakTree.write("ssml.xml")

ssml_string = open("ssml.xml", "r").read()

#Настройка разговорника
speech_config = SpeechConfig(subscription=key, region="westeurope");
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff16Khz16BitMonoPcm"])
speech_sync = SpeechSynthesizer(speech_config=speech_config);

#Сохранение результата в файл
result = speech_sync.speak_ssml_async(ssml_string).get();
stream = AudioDataStream(result);
stream.save_to_wav_file("audio_output.wav");

#Подсчёт длительности
with contextlib.closing(wave.open("audio_output.wav",'r')) as f:
    frames = f.getnframes();
    rate = f.getframerate();
    duration = frames / float(rate);
    print("Output duration in sec: " + str(duration));
    print("Average character duration in sec: " + str(duration/textLen));