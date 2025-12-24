from telebot import TeleBot
from telebot import types
import config
import random
import string
import config
import os


welcome_message = """

🎮 Game Concept:
Every player receives a secret Character Card. However, one player is the Spy. Everyone else sees the same character, but the Spy is left in the dark!

🕵️ Goal of the Spy:
Blend in and avoid being unmasked. Pretend you know the character!

👥 Goal of the Players:
Identify the player who doesn't know the character by asking subtle questions.

🛠 How to play:
1. Create or Join a room.
2. Everyone must press "Ready".
3. Check your card and start the discussion!
"""


bot = TeleBot(config.TOKEN)

games = {}




folder_path = 'foto'



def process_again_step(message):
    chat_id = message.chat.id
    text = message.text
    room = None
    for r_id, game in games.items():
        if chat_id in game["players"]:
            room = game
            rid = r_id
            break
    if not room:
        bot.send_message(chat_id, "Error: Room not found", reply_markup=main_buttons())
        return
    if text == "Yes":
        room["started"] = False
        room["ready"].add(chat_id)
        ready_count = len(room["ready"])
        total_count = len(room["players"])

        bot.send_message(chat_id, f"You are ready for a new game!", reply_markup=room_buttons())

        if ready_count == total_count:
            game_started(room)
        
    else:
        bot.send_message(chat_id, "Okay, returning to the menu.", reply_markup=main_buttons())
        quit_game(message)







def game_started(room):
    room["ready"] = set()
    room["started"] = True

    for pid in room["players"]:
        bot.send_message(pid, "The game has started!")
    karta = room["players"]
    random_kartka = random.choice(karta)
    bot.send_message(random_kartka, "You are the Spy 🕵️")

    all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    random_image = random.choice(all_files)
    full_path = os.path.join(folder_path, random_image)
    for ppp in room["players"]:

        if ppp != random_kartka:

            
            with open(full_path, 'rb') as photo:
                bot.send_photo(ppp, photo)
   





def generate_roomID():
    while True:
        room_id = "".join(random.choices(string.ascii_uppercase + string.digits, k = 4))
        if room_id not in games:
            return room_id
    


def room_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ready")
    markup.add("View Players", "Leave")
    markup.add("Play Again")
    return markup


def main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Create Game")
    markup.add("Join Game")
    return markup

def again_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Yes", "No")
    return markup




def join_game(message):
    chat_id = message.chat.id
    room_id = message.text.upper()

    if room_id in games:
        game = games[room_id]
        if chat_id not in game["players"]:
            game["players"].append(chat_id)
        bot.send_message(chat_id, f'You joined room {room_id}', reply_markup=room_buttons())

    else:
        bot.send_message(chat_id, "Room not found!")
       



def quit_game(message):
    chat_id = message.chat.id
    
    room = None
    rid = None
    for r_id, game in games.items():
        if chat_id in game["players"]:
            room = game
            rid = r_id
            break

    if room:
        room["players"].remove(chat_id)
        bot.send_message(chat_id, f'You left room {rid}', reply_markup=main_buttons())

        if len(room["players"]) == 0:
            del games[rid]
    else:
        bot.send_message(chat_id, "You were not in a room", reply_markup=main_buttons())

   




@bot.message_handler(commands=['info'])
def send_welcome(message):
    
    bot.reply_to(message,welcome_message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Hi my little man")



@bot.message_handler(commands=['menu'])
def menu_message(message):
    
    bot.send_message(message.chat.id,'Select an option:',reply_markup=main_buttons())




@bot.message_handler(content_types='text')
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    user_room = None
    user_room_id = None
    for rid, game in games.items():
        if chat_id in game["players"]:
            user_room = game
            user_room_id = rid
            break
    if not user_room:
        if text == "Create Game":
            room_id = generate_roomID()
            games[room_id] = {
                "creator" : chat_id,
                "players" : [chat_id], 
                "ready" : set(),
                "started" : False
            }
            bot.send_message(message.chat.id, f"Game created! Your Room ID: {room_id}", reply_markup=room_buttons())

        elif text == "Join Game":
            msg =  bot.send_message(chat_id, "Enter Room ID:")
            bot.register_next_step_handler(msg,join_game)

 

    else:
    
        if text == "View Players":
                
            player_list = []
            for pid in user_room["players"]:
                user = bot.get_chat(pid)
                name = user.first_name or user.username or str(pid)
                player_list.append(name)
            bot.send_message(chat_id, "Players in the room:\n" + "\n".join(player_list))

        elif text == "Leave":
            quit_game(message)

        elif text == "Ready":
            user_room["ready"].add(chat_id)
            bot.send_message(chat_id, "You are ready!")
            if set(user_room["players"]) == user_room["ready"] and not user_room["started"]:
                game_started(user_room)

        elif text == "Play Again":
            messg =  bot.send_message(chat_id, "Ready to play again?", reply_markup=again_button())
            bot.register_next_step_handler(messg, process_again_step)
            
            
            
           
                    
                




    

    





bot.infinity_polling()


