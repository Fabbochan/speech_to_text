import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from fpdf import FPDF
import datetime

r = sr.Recognizer()

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition of these chunks
    """
    # open the audio file
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more
    # and get chunks
    # if you increase the min_silence_len you will get less audio chunks
    chunks = split_on_silence(sound,
                              min_silence_len=700,
                              silence_thresh=sound.dBFS-14,
                              keep_silence=500)
    # make folder for the audio chunks
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # process each chunk
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in the folder
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened, language="DE-AT")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    return whole_text


def save_to_pdf(path, text):
    """
    Recieves a string and prints it to a pdf. The title of the pdf
    will be extracted from the path variable. It will also add the
    current data.
    """
    date = datetime.date.today()
    pdf_filename = path.split(".")[0]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.multi_cell(w=0, h=10, align="R", txt=str(date))
    pdf.multi_cell(w=0, h=10, txt=f"{pdf_filename}: {text}")
    pdf.output(f"{pdf_filename}.pdf")


if __name__ == "__main__":
    # provide the path to your audio file
    path = ""
    # print("Full text: ", get_large_audio_transcription(path))
    text = get_large_audio_transcription(path=path)
    save_to_pdf(path=path, text=text)



