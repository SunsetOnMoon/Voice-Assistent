import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import sys
#import multiproccesing
from datetime import datetime
import requests
import json
import time
import threading
import playsound

#-----------------------------
#Константы
GMT = 3 # часовой пояс
path_to_alarm = 'C:/Work/Studying/Python/Voice Assistent/alarm_erjan.mp3'
#--------------------------

def init_speaker(): # инициализируем "голос"
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

def get_weather_now(): #Дописать влажность, облачность
	url = "https://api.ambeedata.com/weather/latest/by-lat-lng"
	querystring = {"lat":"53.9018","lng":"27.5565"}
	headers = {
    	'x-api-key': "48d499acb58211be2ed40a6be345aac36cf27dce79dcd4559a5afe9e1e80c5d2",
    	'Content-type': "application/json"
    }
	response = requests.request("GET", url, headers=headers, params=querystring)

	weather_dict = json.loads(response.text)

	celsius = (weather_dict['data']['temperature'] - 32) * 5 / 9
	return round(celsius)

def get_weather_forecast(hour): # Получаем прогноз погоды на завтра. Добавить влажность, облачность, скорость ветра
	url = "https://api.ambeedata.com/weather/forecast/by-lat-lng"
	querystring = {"lat":"53.9018","lng":"27.5565"}
	headers = {
	    'x-api-key': "48d499acb58211be2ed40a6be345aac36cf27dce79dcd4559a5afe9e1e80c5d2API_KEY",
	    'Content-type': "application/json"
	    }
	response = requests.request("GET", url, headers=headers, params=querystring)
	forecast_dict = json.loads(response.text)

	timestamp = get_timestamp(hour, 0)
	#print(int(timestamp))
	for forecast in forecast_dict['data']['forecast']:
		if forecast['time'] == timestamp:
			celsius = (forecast['temperature'] - 32) * 5 / 9
			return round(celsius)

def alarm(hour, minutes): #будильник
	time.sleep(get_timestamp(hour, minutes) - int(time.time()))
	alarm_sound = threading.Thread(target = playsound.playsound, args = [path_to_alarm])
	alarm_sound.start()

def get_timestamp(hour, minutes): #получаем Unix Timestamp по начему часовому диапазону
	timestamp = int(time.time())

	timestamp //= 60 * 60 * 24
	timestamp += 1
	timestamp *= 60 * 60 * 24
	timestamp += (hour - GMT) * 60 * 60 + minutes * 60
	return timestamp

def command(engine): # Распознаём речь
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
		#engine.say('Я вас не поняла')
		task = command(engine)
			
	return task
			


def do_task(task): # Список выполняемых задач
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
	elif 'включи музыку' in task: # попробовать мультипроццесность
		engine.say('Слушайте...')
		engine.runAndWait()
		os.startfile(r'C:/Music/Big Baby Tape, kizaru - BANDANA I/bandana.aimppl')
	elif 'который час' in task:
		current_datetime = datetime.now()
		engine.say('Сейчас ' + str(current_datetime.hour) + ' ' + str(current_datetime.minute))
		engine.runAndWait()
	elif 'погода на улице' in task:
		celsius = get_weather_now()
		engine.say('Сейчас на улице ' + str(celsius) + ' градусов Цельсия.')
		engine.runAndWait()
		#Дописать 
		#
		#
	elif 'погода завтра утром' in task:
		celsius = get_weather_forecast(8)
		engine.say('Завтра утром на улице будет ' + str(celsius) + ' градусов Цельсия.')
		engine.runAndWait()
	elif 'погода завтра днём' in task:
		celsius = get_weather_forecast(12)
		engine.say('Завтра днём на улице будет ' + str(celsius) + ' градусов Цельсия.')
		engine.runAndWait()
	elif 'погода завтра вечером' in task:
		celsius = get_weather_forecast(18)
		engine.say('Завтра вечером на улице будет ' + str(celsius) + ' градусов Цельсия.')
		engine.runAndWait()
	elif 'спасибо' in task:
		engine.say('Всегда рада помочь, зайка')
		engine.runAndWait()
	elif 'поставь будильник' in task:
		parsed_str = task.split()
		for string in parsed_str:
			if ':' in string:
				time_for_voice = string
				parsed_time = string.split(':')
				break
		hour = int(parsed_time[0])
		minutes = int(parsed_time[1])
		alarm_thread = threading.Thread(target=alarm, args=[hour, minutes])
		alarm_thread.start()
		engine.say('Я поставила будильник на ' + time_for_voice)
		engine.runAndWait()


engine = init_speaker()
engine.say('Привет пупсик!')
engine.runAndWait()

while 1:
	do_task(command(engine))


