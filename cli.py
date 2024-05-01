import speech_recognition as sr
recognizer = sr.Recognizer()

import json

import requests

import os 

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

###############################################
##########    CREATE AUDIO FUNCTIONS    #######
###############################################

def record_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def recognize_speech(audio):
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")

###############################################
##########    CREATE GAME FUNCTIONS    ########
###############################################

def create_game(size,handicap,komi):
    r= requests.get('http://127.0.0.1:5000/create_game', params={'size': size, 'handicap':handicap, 'komi':komi})

    return r.json()["game_manager_uuid"]

def is_blindfolded_player_black(game_manager_uuid):
    r= requests.get('http://127.0.0.1:5000/is_blindfolded_player_black/')
    return True

def request_move_from_server(game_manager_uuid):
    r= requests.get('http://127.0.0.1:5000/request_ply_from_engine/')
    return "D4" 

def is_game_over(game_manager_uuid):
    r= requests.get('http://127.0.0.1:5000/is_game_over/')
    return False

def play_move(game_manager_uuid, move):
    r= requests.get(url='http://127.0.0.1:5000/play_move',params={'game_manager_uuid': game_manager_uuid,"move":move}) 



def is_move(game_manager_uuid, candidate_speech):
    r= requests.get(url='http://127.0.0.1:5000/is_move', params={'game_manager_uuid': game_manager_uuid, 'candidate_speech':candidate_speech})
    return r.json()["result"]

'''
def is_playable_move(game_manager_uuid, move):
    r= requests.get('http://127.0.0.1:5000/is_playable_move/')
    return True  
'''

def submit_pass(game_manager_uuid):
    pass

def resign_game(game_manager_uuid):
    pass

def request_undo(game_manager_uuid):
    r= requests.get('http://127.0.0.1:5000/request_undo',params={"game_manager_uuid":game_manager_uuid})



##############################################################
##########    CREATE GAME AND INITIALIZE VARIABLES    ########
##############################################################

#game_id=None
size=int(config['GOBAN']['size'])
handicap=int(config['HANDICAP']['number_of_stones'])
komi=float(config['RULES']['komi'])
game_manager_uuid=create_game(size,handicap,komi)

r = sr.Recognizer()
mic = sr.Microphone()
sr.Microphone.list_microphone_names()

blindfolded_player_is_black=is_blindfolded_player_black(game_manager_uuid)
label_dict={True:"black", False:"white"}
#os.system("say 'Blindfolded player plays with the "+label_dict[blindfolded_player_is_black]+" stones !'") 
#os.system("say 'Game started !'")

if not blindfolded_player_is_black:
    move=request_move_from_server(game_manager_uuid)
    #os.system("say 'White plays "+move+" !'")

##########################################
##########    RUN PLAYING LOOP    ########
##########################################

while(is_game_over(game_manager_uuid)==False):

    result=""
    print(result)

    # while the speech is not a playable move
    while(is_move(game_manager_uuid,result)==False):
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            result=r.recognize_google(audio)
            print(result)
        except sr.UnknownValueError:
            # speech was unintelligible
            result=""

    # when the speech is a playable move
    if result in ["pass","Pass"]:
        submit_pass(game_manager_uuid)
    elif result in ["resign","Resign"]:
        resign_game(game_manager_uuid)
    elif result in ["undo","Undo"]:
        request_undo(game_manager_uuid)
    else:
        play_move(game_manager_uuid,result)
    

    if is_game_over(game_manager_uuid):
        break
    else:
        move_from_AI=request_move_from_server(game_manager_uuid)
        #os.system("say '"+label_dict[blindfolded_player_is_black==False]+" plays "+move_from_AI+" !'")



#os.system("say 'Thanks for the game !'")