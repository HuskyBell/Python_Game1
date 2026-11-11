import random
print("  ▄▄▄▄   ▓█████   ██████ ▄▄▄█████▓    ▒█████    █████▒    ██▓     █    ██  ▄████▄   ██ ▄█▀")
print(" ▓█████▄ ▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒   ▒██▒  ██▒▓██   ▒    ▓██▒     ██  ▓██▒▒██▀ ▀█   ██▄█▒ ")
print("▒ ██▒ ▄██▒███   ░ ▓██▄   ▒ ▓██░ ▒░   ▒██░  ██▒▒████ ░    ▒██░    ▓██  ▒██░▒▓█    ▄ ▓███▄░ ")
print("░ ▓█  ▀█▓ ████▒▒██████▒▒  ▒██▒ ░    ░ ████▓▒░░▒█░       ░██████▒▒▒█████▓ ▒ ▓███▀ ░▒██▒ █▄")
print("░▒▓███▀▒░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░      ░ ▒░▒░▒░  ▒ ░       ░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░▒ ▒▒ ▓▒")
print("▒░▒   ░  ░ ░  ░░ ░▒  ░ ░    ░         ░ ▒ ▒░  ░         ░ ░ ▒  ░░░▒░ ░ ░   ░  ▒   ░ ░▒ ▒░")
print(" ░    ░    ░   ░  ░  ░    ░         ░ ░ ░ ▒   ░ ░         ░ ░    ░░░ ░ ░ ░        ░ ░░ ░ ")
print(" ░         ░  ░      ░                  ░ ░                 ░  ░   ░     ░ ░      ░  ░   ")
print(" ░                                                                  ░               ")
print("6 chambers one water cartrige")
print("begin")
dead = False
turn = True
E_turn = True
count = 0
luck = random.randint(1,6)
P_lives = 3
E_lives = 3
inv = []
items = ['chamber_spinner','water_cartridge','double_shot','chamber_checker']
while dead == False:
    while turn == True:  
        choice = input("fire on yourself, fire on them, check inventory, use item:")        
        if choice == "fire on yourself":
            if luck == 1:
                P_lives = P_lives - 1
                print("haha you got wet, you lose a life! you now have", P_lives, "lives left")
                luck = random.randint(1, 6-count)

            else:
                print("you were lucky this time!")
                luck = luck-1

        if choice == "fire on them":
            if luck == 1:
                print("aww, now I'm all wet")
                E_lives = E_lives - 1
                print(f"they now have {E_lives} lives!")
                turn = False
                luck = random.randint(1, 6-count)
            else:
                print("haha, wrong one")
                turn = False
                luck = luck-1
        if choice == "check inventory":
            print("you have", inv)
        if choice == "use item":
            choice = input(f"what item would you like to use {inv}")

            if choice == "chamber_spinner":
             luck = random.randint(1, 6-count)
             print("you spin the chamber")
             inv.remove("chamber_spinner")
            if choice == 'water_cartridge':
                print("another cartridge has been added")
                count = count + 1
                inv.remove("water_cartridge")
            if choice == "double_shot":
                if luck == 1:
                    E_lives = E_lives-2
                    print("you shot twice... TWO hit!")
                    print("they now have", E_lives, "lives")
                    luck = luck-2
                    inv.remove("double_shot")
                    turn = False
                elif luck == 2:
                    print("you shot twice... ONE hit!")
                    E_lives = E_lives-1
                    print("they now have", E_lives, "lives")
                    luck  = luck-2
                    inv.remove("double_shot")
                    turn = False
                else:
                    print("you shot twice... NONE hit")
                    turn = False
                    luck= luck-1
                    inv.remove("double_shot")
            if choice == "chamber_checker":
                inv.remove("chamber_checker")
                print("there are", luck-1, "blanks left until it fires")
        if turn == False:
            print("they fire at you")
            if luck == 1:
                P_lives = P_lives - 1
                luck = random.randint(1,6-count)
                print("you now have", P_lives, "lives")
                turn = True
                E_turn = False
            else:
                print("aw man, lucky")
                turn = True
                luck = luck - 1
                E_turn = False
        if E_turn == False:
            item = random.choice(items)
            inv.append(item)
            print ("you got a", item)
            E_turn = True
        if luck <= 0:
            luck = random.randint(1,6-count)
        if E_lives <= 0:
            print("You win !!!")
            turn = False
            dead = True
        if P_lives <= 0:
            print("you lose")
            dead = True
            turn = False
    

            
