import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import sys
#import multiproccesing
from datetime import datetime

def init_speaker():
	engine = pyttsx3.init()

	rate = engine.getProperty('rate')
	print(rate)
	engine.setProperty('rate', 210)

	volume = engine.getProperty('volume')
	print(volume)
	engine.setProperty('volume', 5.0)

	voices = engine.getProperty('voice')
	engine.setProperty('voice', voices[0])
	return engine

def command(engine):
	r = sr.Recognizer()

	with sr.Microphone() as source:
		print('Говорите...')
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)

	try:
		task = r.recognize_google(audio, language = 'ru-RU').lower()
		print('Вы сказали: ' + task)
	except sr.UnknownValueError:
		engine.say('Я вас не поняла')
		task = command(engine)
			
	return task
			


def do_task(task):
	if 'открыть сайт' in task:
		engine.say('Уже открываю')
		engine.runAndWait()
		url = 'https://habr.com/ru/all/'
		webbrowser.open(url)
	elif 'хочу посмотреть фильм' in task:
		engine.say('Надеюсь. Вы найдёте что-то по вкусу')
		engine.runAndWait()
		url = 'https://kinogo.biz/'
		webbrowser.open(url)
	elif 'заканчиваем' in task:
		engine.say('Без проблем. До свидания!')
		engine.runAndWait()
		sys.exit()
	elif 'включи музыку' in task:
		engine.say('Слушайте...')
		engine.runAndWait()
		os.startfile(r'C:/Music/Big Baby Tape, kizaru - BANDANA I/bandana.aimppl')
	elif 'который час' in task:
		current_datetime = datetime.now()
		engine.say('Сейчас ' + str(current_datetime.hour) + ' ' + str(current_datetime.minute))
		engine.runAndWait()

engine = init_speaker()
engine.say('Привет мой дорогой друг!')
engine.runAndWait()

while 1:
	do_task(command(engine))


