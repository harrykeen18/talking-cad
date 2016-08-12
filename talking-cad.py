import speech_recognition as sr
import warnings
from os import path
import simplejson as json
import re

warnings.filterwarnings("ignore")

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something like 'extrude a rectangle 15mm'")
    audio = r.listen(source)

# write audio to a WAV file
with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "microphone-results.wav")

# use the audio file as the audio source
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
  audio = r.record(source) # read the entire audio file

# recognize speech using Sphinx
# try:
#   print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#   print("Sphinx could not understand audio")
# except sr.RequestError as e:
#   print("Sphinx error; {0}".format(e))

# recognize speech using Google Speech Recognition
try:
  # for testing purposes, we're just using the default API key
  # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
  # instead of `r.recognize_google(audio)`
  print("You said " + r.recognize_google(audio))
except sr.UnknownValueError:
  print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
  print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Write .json file

input_string = r.recognize_google(audio)
json_output = {'features': {}}
feature = {}
feat_ind = 0

if 'extrude' in input_string:
  print('found extrude')
  feat_ind += 1
  # json_output['features']['extrudes'] = 'extrude' + str(feat_ind)
  feature['name'] = 'extrude' + str(feat_ind)
  feature['type'] = 'extrude'

if bool(re.search(r'\d', input_string)):
  numbers = re.findall(r'\d+', input_string)
  print(int(numbers[feat_ind - 1]))
  feature['distance'] = int(numbers[feat_ind - 1])

json_output['features']['feature' + str(feat_ind)] = feature

print(json.dumps(json_output, indent=4 * ' '))










