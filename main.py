from google import genai
import os
import sys
import pyaudio
import wave
import tkinter
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

'''with open("transcription.txt", "w") as file:
    file.write("")'''

IsRecordingText = ""

def updateLabelRecording():
  IsRecording_label.config(text= "Recording...")

def updateLabel_DoneRecording():
  IsRecording_label.config(text= "Finished Recording!")

def getTkInputRecord():
  input_text = entry_widget_record.get()
  print(f"User entered: {input_text}")
  RECORD_SECONDS=input_text 
  return RECORD_SECONDS

def getTkInputEdit():
  input_text = edit_entry.get()
  print(f"User entered: {input_text}")
  return input_text

def select_file():
    # Create a Tk root window
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Optional: ensure the dialog box appears on top of other windows
    root.call('wm', 'attributes', '.', '-topmost', True) 
    
    # Open the file selection dialog
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select a file",
        filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg"))
    )
    
    # Destroy the root window after the dialog is closed
    root.destroy()
    
    # Return the selected filename
    return filename

client= genai.Client()
UserInput = ""


def ask():
  print("What do you want to do now? 1)record audio 2)Transcribe 3)ask about/maniputlate transcription 4)end")
  UserInput=input()
  if UserInput =="1":
    Terminal_record()
  elif UserInput =="2":
   Terminal_transcribe()
  elif UserInput =="3":
   Terminal_edit()
  elif UserInput =="4":
    ""

def Terminal_record():
    # Audio parameters
    FORMAT = pyaudio.paInt16  # 16-bit resolution
    CHANNELS = 1             # Mono audio
    RATE = 44100             # Sample rate (samples per second)
    CHUNK = 1024             # Number of frames per buffer
    print("how many seconds do you want to record?")
    UserInput=int(input())
    RECORD_SECONDS = UserInput       # Duration of recording
    WAVE_OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []

    for i in range(0, int(RATE / int(CHUNK) * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    ask()


def tkRecord():
  # Audio parameters
    FORMAT = pyaudio.paInt16  # 16-bit resolution
    CHANNELS = 1             # Mono audio
    RATE = 44100             # Sample rate (samples per second)
    CHUNK = 1024             # Number of frames per buffer

    RECORD_SECONDS = getTkInputRecord()      # Duration of recording
    WAVE_OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()
    updateLabelRecording()
    # Start recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RATE / int(CHUNK) * int(RECORD_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)

    updateLabel_DoneRecording()

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()





def Terminal_transcribe():
  myfile = client.files.upload(file=select_file())
  #updated transcription code
  response = client.models.generate_content(
     model="gemini-2.5-flash", contents=["Transcribe this audio clip", myfile]
  )

  #Below for creating Transcription
  # Upload the audio file
  print(response.text)
  transcriptionText = response.text
  #add transcription to a text file for refrence
  with open("transcription.txt", "w") as file:
    file.write(transcriptionText)
  ask()

def tkTranscribe():
  myfile = client.files.upload(file=select_file())
  #updated transcription code
  response = client.models.generate_content(
     model="gemini-2.5-flash", contents=["Transcribe this audio clip", myfile]
  )

  #Below for creating Transcription
  # Upload the audio file
  print(response.text)
  transcriptionText = response.text
  #add transcription to a text file for refrence
  with open("transcription.txt", "w") as file:
    file.write(transcriptionText)
    Transcription_label.config(text=transcriptionText)

def Terminal_edit():
  #Below for modifying transcription
  loop = True
  while loop:
   print("What would you like to do to the transcription? \"end\" to stop.")
   UserInput = input()
   if UserInput == "end":
     loop = False
   else:
    with open("transcription.txt", "r") as f:
      transcriptionFile = f.read()
    if transcriptionFile != "":
      # Create a model instance for modification
      geminiInput=str(
        f"Follow these instructions to the transcription{UserInput}"
        f"the Transcription is:{transcriptionFile}"
      )
      response = client.models.generate_content(
      model="gemini-2.5-flash", contents=geminiInput
      )
      print(response.text)
    else:
      print("please transcribe an audio file first")
      loop= False
  ask()


def tkedit():
  #Below for modifying transcription
  UserInput = getTkInputEdit()
  with open("transcription.txt", "r") as f:
    transcriptionFile = f.read()
  if transcriptionFile != "":
    # Create a model instance for modification
    geminiInput=str(
      f"Follow these instructions to the transcription{UserInput}"
      f"the Transcription is:{transcriptionFile}"
    )
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=geminiInput
    )
    editedTranscription_label.config(text=response.text)
  else:
    editedTranscription_label.config(text="please transcribe an audio file first")
#ask()



root = tk.Tk()
root.title("NADCA")

SecondsRequired_label=tk.Label(root,text="Please put how many seconds you want to record as a number below!",width=70)
SecondsRequired_label.pack(pady=10)

entry_widget_record=tk.Entry(
  root,width=70
)
entry_widget_record.pack(pady=10)

Record_button= tk.Button(
  root,text="Click to record!",command=tkRecord, width=50,font=("bold"))
Record_button.pack(pady=10)

IsRecording_label=tk.Label(root, width=70, text="")
IsRecording_label.pack(pady=10)

Transcribe_button= tk.Button(
  root,text="Click to transcribe an audio file!",command=tkTranscribe,width=50,font=("bold"))
Transcribe_button.pack(pady=10)

Transcription_label= tk.Label(root,text="",width=70)
Transcription_label.pack(pady=10)

edit_button=tk.Button(
  root,text="Edit a made trascription!",command=tkedit,width=50,font=("bold"))
edit_button.pack(pady=10)
 
edit_entry=tk.Entry(
  root, width=70
)
edit_entry.pack(pady=10)

editedTranscription_label=tk.Label(root,text="",width=100)
editedTranscription_label.pack(pady=10)

root.mainloop()