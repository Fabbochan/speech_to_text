import speech_recognition as sr
from fpdf import FPDF
import datetime

# provide the path to your audio file
filename = ""
# pdf filename gets created
pdfFilename = filename.split(".")[0]
# current date gets identified
date = datetime.date.today()

r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    # the audio language needs to be adjusted as the second argument
    text = r.recognize_google(audio_data, language="DE-AT")
    # the pdf file gets created
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.multi_cell(w=0, h=10, align="R", txt=str(date))
    pdf.multi_cell(w=0, h=10, txt=f"{pdfFilename}: {text}.")
    pdf.output(f"{pdfFilename}.pdf")


