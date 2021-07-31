import re
import time
import traceback
def converter(hex_s):
    return int("0x"+hex_s,16)


move_regex = r"Move\(x=(\d+), y=(\d+)"
pattern_move = re.compile(move_regex)

click_regex = r"Click\(x=(\d+), y=(\d+), button=Button\.(left|right), pressed=(True|False)\)"
pattern_click = re.compile(click_regex)

special_key_regex = r"special key (.+) pressed"
pattern_special = re.compile(special_key_regex)

key_kreleased_regex = r"(.+) released"
pattern_kkey_released = re.compile(key_kreleased_regex)

key_pressed_regex = r"alphanumeric key (.+) pressed"
pattern_key_pressed = re.compile(key_pressed_regex)

key_released_regex2 = r"\'(.+)\' released"
pattern_key_released2 = re.compile(key_released_regex2)

with open("output.txt","r") as output:
    instruction_list = output.readlines()
    for element in range(len(instruction_list)):
        if (instruction_list[element][len(instruction_list[element])-1:len(instruction_list[element])-3]).encode().__eq__(r"\n"):
           instruction_list[element] = instruction_list[element][0:len(instruction_list[element])-1]

from pynput.keyboard import Key, Controller 

keyboard = Controller()
f = open("Time.txt","r")
a = f.readline()
a = float(0.001)/50
f.close()

str_text = str()

try:
    for i in instruction_list:
        #if i[0].__eq__("a"):
            #matches = pattern_key_pressed.findall(i)
            #if matches[0][1:len(matches[0])-3].__eq__(r"\x"):
                #keyboard.press(chr(converter(matches[0][3:len(matches[0])-1])+96))
                #time.sleep(a)
            #else:
                #try:
                    #keyboard.press(str(matches[0]))
                #except Exception:
                    #keyboard.press(str(matches[0])[1:-1])
                    #time.sleep(a)
        if i[0].__eq__("K"):
            matches = pattern_kkey_released.findall(i)
            #keyboard.release(Key[matches[0][4:len(matches[0])]])
            time.sleep(a)
        elif i[0].__eq__("'"):
            matches = pattern_key_released2.findall(i)
            if str(matches[0][0:len(matches[0])-2]).__eq__(r"\x"):
                str_text += chr(converter(matches[0][2:len(matches[0])-1])+96)
                #keyboard.release(chr(converter(matches[0][2:len(matches[0])-1])+96))
                time.sleep(a)
            else:
                str_text += str(matches[0])
                #keyboard.release(str(matches[0]))
                time.sleep(a)
        else: 
            print("default value")
            time.sleep(a)
except Exception:
    traceback.print_exc() # don't care about index out of range expection because it's only because of last line, remember that it is empty

print(str_text)


#your png file should be same or similar to the emote name
example_words = [":s","vurma",":vur",":vurmaa",":vurmaab:",":sob:",":sob2",":"]
example_links = ["https://media.discordapp.net/attachments/771392061072343043/829977284122509312/vurmaab.png",
"wwww.discord.com//sob.png",]

def find_emote_equality(finding,data):
    count = 0
    try:
        for i in range(len(str(data))):
            if str(finding[i]) == str(data[i]) and i<3:
                count = count + 1
            if str(finding[i]) == str(data[i]) and i>2 and count>=3:
                count = count + 1
    except:
        print()
    if len(finding)>len(data): return False
    elif count>=len(data)/4 and count<= len(data): return True#if at least 25% of data given correctly we will return the link
    else: return False

discord_emote_regex = r".*\:([^:\W]+)\:?.*"
pattern = re.compile(discord_emote_regex)

discord_url_emote_regex = r".+\/(.+)\..+"
pattern_url = re.compile(discord_url_emote_regex)

send_this = str()
matches = pattern.findall(str_text)
for a in range(len(example_links)):
    url_matches = pattern_url.findall(str(example_links[a]))
    try:
        if find_emote_equality(matches[0],url_matches[0]):
            print(matches[0],example_links[a])
            send_this = example_links[a]
    except:
        traceback.print_exc()
time.sleep(2)
print(str_text)
with keyboard.pressed(Key.ctrl):
    keyboard.press('a')
    keyboard.release('a')
keyboard.press(Key.delete)
keyboard.release(Key.delete)
keyboard.type(send_this)
open("output.txt","w").write("")