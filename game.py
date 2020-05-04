import random
import pyttsx3
import assistant_main as am
import random
from random import shuffle


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

# print(voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#then, let's make a set of moves the PC can choose from:
def game():
    speak("Lets play")
    moves = ["rock", "paper", "scissors"]

    c_count=0
    p_count=0

    #Now let's get coding our game:

    # I would like to have this loop forever, so let's make a "switch" for the game

    keep_playing = "true"

    while keep_playing == "true":
        cmove = random.choice(moves)
        print("Scores Player score : ",p_count," Computer score : ",c_count)
        pmove = int(input("What is your move: \n1.rock,\n2.paper\n3.scissors? "))

        pmove = moves[pmove-1]
        
        print ("The computer chose",cmove)
        if cmove == pmove:
            print ("Tie")
            speak("Tie")
        elif pmove == "rock":
            if cmove == "scissors":
                print ("Player wins")
                speak("Player wins")
                p_count=p_count+1
            elif cmove == "paper":
                print ("Computer wins")
                speak("Computer wins")
                c_count=c_count+1
        elif pmove == "scissors":
            if cmove == "rock":
                print ("Computer wins")
                speak("Computer wins")
                c_count=c_count+1
            elif cmove == "paper":
                print ("Player wins")
                speak("Player wins")
                p_count=p_count+1
        elif pmove == "paper":
            if cmove == "scissors":
                print ("Computer wins")
                speak("Computer wins")
                c_count=c_count+1
            elif cmove == "rock":
                print ("Player wins")
                speak("Player wins")
                p_count=p_count+1
        if p_count==5:
            print("Scores Player score : ",p_count," Computer score : ",c_count)
            print("Player Won ^_^")
            speak("hip hip hurray")
            speak("Player won")
            keep_playing = "false"
        elif c_count==5:
            print("Scores Player score : ",p_count," Computer score : ",c_count)
            print("Computer won -_-")
            speak("Ohh no")
            speak("Computer won")
            keep_playing = "false"

def game1():
    speak("Welcome to the words jumbling game")
    answer = ["python","youtube","google"]

    words =[]

    for i in answer:
        word = list(i)
        shuffle(word)
        words.append(word)

    chances = 5

    num = random.randint(0,len(words)-1)

    while chances>0:
        print("No of chances left : ",chances)
        speak("No of chances left")
        speak(chances)
        for i in words[num]:
            print(i,end="")
        print()
        user_input = input("Guess the word : ")
        if user_input == answer[num]:
            print("Hurray, it's correct ^_^")
            speak("Hurray, it's correct")
            chances=-1
        chances = chances-1
        if(chances==0):
            print("chances over -_-")
            speak("chances over")
        elif chances>0:
            print("Please try again")
            speak("Please try again")