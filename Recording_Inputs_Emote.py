from pynput import keyboard, mouse
import pynput
import multiprocessing
import traceback
import time
import re
# The event listener will be running in this block
def replacement():
    def converter(hex_s):
        return int("0x"+hex_s,16)

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
    a = float(0.001)/50

    str_text = ""

    try:
        for i,x in zip(instruction_list,range(len(instruction_list))):
            if i[0].__eq__("a"):
                matches = pattern_key_pressed.findall(i)
                if matches[0][1:len(matches[0])-3].__eq__(r"\x"):
                    #str_text += chr(converter(matches[0][3:len(matches[0])-1])+96)
                    time.sleep(a)
                else:
                    try:
                        str_text += (str(matches[0]))
                    except Exception:
                        str_text += (str(matches[0])[1:-1])
                        
                        #time.sleep(a)
            if i[0].__eq__("K"):
                
                matches = pattern_kkey_released.findall(i)
                if Key[matches[0][4:len(matches[0])]] == Key.backspace and x != 0:
                    str_text = str_text[0:x]
                #keyboard.release(Key[matches[0][4:len(matches[0])]])
                
            if i[0].__eq__("'"):
                matches = pattern_key_released2.findall(i)
                if str(matches[0][0:len(matches[0])-2]).__eq__(r"\x"):
                    str_text += chr(converter(matches[0][2:len(matches[0])-1])+96)
                else:
                    str_text += str(matches[0])
    except:
        print()
        #traceback.print_exc() # don't care about index out of range expection because it's only because of last line, remember that it is empty
    
    link_examples = [
    "https://media.discordapp.net/attachments/818214043743158302/830226182280577065/vurmaab.png",
    "https://cdn.discordapp.com/attachments/796554830936145932/830203065255854121/pepog.png",
    "https://cdn.discordapp.com/attachments/796554830936145932/830203066962673664/poggies.png",
    "https://cdn.discordapp.com/attachments/796554830936145932/830203068024094740/wesmart.png",
    "https://cdn.discordapp.com/attachments/796554830936145932/830203207841218560/gablick.gif",
    "https://media.discordapp.net/attachments/818214043743158302/830222286798848070/love.png",
    "https://cdn.discordapp.com/attachments/818214043743158302/830224397935706152/sipFelix.png",
    "https://cdn.discordapp.com/attachments/818214043743158302/830223774715609118/crying.png",
    "https://media.discordapp.net/attachments/829155749040750596/830236204280184872/hiSlpy.png",
    "https://media.discordapp.net/attachments/818214043743158302/830236648570224650/o7Slpy.png",
    "https://cdn.discordapp.com/attachments/823215544916246559/830306292828602398/kekw.png",
    "https://cdn.discordapp.com/attachments/125619281638457345/830727874633269268/pepothink.png"]

    def find_emote_equality(finding,data):
        count = 0
        try:
            for i in range(len(str(data))):
                if str(finding[i]) == str(data[i]) and i<3:
                    count = count + 1
                elif str(finding[i]) != str(data[i]) and i<3:
                    count = count - 1
                if str(finding[i]) == str(data[i]) and i>2 and count>=3:
                    count = count + 1
                elif str(finding[i]) != str(data[i]) and i>2 and count>=3:
                    count = count - 1
        except:
            print()
        if len(finding)>len(data): return False
        elif count>=len(data)/4 and count<= len(data): return True#if at least 25% of data given correctly we will return the link
        else: return False

    discord_emote_regex = r".*\:([^:\W]+)\:?.*"
    pattern = re.compile(discord_emote_regex)

    discord_url_emote_regex = r".+\/(.+)\..+"
    pattern_url = re.compile(discord_url_emote_regex)

    send_this = ""
    matches = pattern.findall(str_text)
    for a in range(len(link_examples)):
        url_matches = pattern_url.findall(str(link_examples[a]))
        try:
            if find_emote_equality(matches[0],url_matches[0]):
                send_this = link_examples[a]
        except:
            traceback.print_exc()
   
    with keyboard.pressed(Key.ctrl):
        keyboard.press('a')
        keyboard.release('a')
    keyboard.press(Key.delete)
    keyboard.release(Key.delete)
    keyboard.type(send_this)
    output_txt = open("output.txt","w")
    output_txt.write("")
    output_txt.close()


def keyboard_listener():
    from pynput import keyboard

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop listener
            #print('{0} released'.format(key))
            return False 
        if key == keyboard.Key.alt_l:
            replacement()

    
        else:
            #print('{0} released'.format(key))
            f = open('output.txt', 'a')
            f.write(str(key)+' released\n')
            f.close()
    

    # Collect events until released
    with keyboard.Listener(on_press=None,on_release=on_release) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=None,on_release=on_release)
    listener.start()

if __name__ == '__main__':
    keyboard_process = multiprocessing.Process(target=keyboard_listener)
    keyboard_process.start()
    keyboard_process.join()
    f = open('output.txt', 'w')
    f.write("")
    f.close()
