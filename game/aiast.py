import random
import time
import os
import sys

def choice(*args, prompt: str = "Select an option:", max_visible: int = 10):
    """
    All-in-one interactive selection bar for Python.
    
    Accepts any number of positional arguments (individual items, lists,
    tuples, or nested iterables) and returns the chosen item.
    """
    import os
    import sys

    # 1. Flatten all positional arguments and nested lists/tuples/sets
    options = []
    stack = list(reversed(args))
    while stack:
        item = stack.pop()
        if isinstance(item, (list, tuple, set)):
            stack.extend(reversed(list(item)))
        else:
            options.append(item)

    if not options:
        raise ValueError("choice() requires at least one option to select from.")

    if len(options) == 1:
        return options[0]

    # 2. Non-interactive fallback (pipes, scripts, non-TTY environments)
    if not sys.stdin.isatty():
        if prompt:
            print(prompt)
        for idx, item in enumerate(options, 1):
            print(f"  [{idx}] {item}")
        while True:
            try:
                raw = input(f"Enter choice (1-{len(options)}): ").strip()
                val = int(raw) - 1
                if 0 <= val < len(options):
                    return options[val]
                print(f"Please enter a number between 1 and {len(options)}.")
            except (ValueError, EOFError):
                print(f"Invalid input. Please enter a number between 1 and {len(options)}.")

    # 3. Cross-platform single key-press reader
    def _read_key():
        if os.name == 'nt':
            import msvcrt
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                return {b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT'}.get(ch2, '')
            elif ch in (b'\r', b'\n'):
                return 'ENTER'
            elif ch == b'\x03':
                raise KeyboardInterrupt
            elif ch in (b'k', b'K'):
                return 'UP'
            elif ch in (b'j', b'J'):
                return 'DOWN'
            elif ch in (b'q', b'Q'):
                return 'QUIT'
            try:
                return ch.decode('utf-8', errors='ignore')
            except Exception:
                return ''
        else:
            import select
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    r, _, _ = select.select([sys.stdin], [], [], 0.05)
                    if r:
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            r, _, _ = select.select([sys.stdin], [], [], 0.05)
                            if r:
                                ch3 = sys.stdin.read(1)
                                return {'A': 'UP', 'B': 'DOWN', 'C': 'RIGHT', 'D': 'LEFT'}.get(ch3, '')
                        elif ch2 == 'O':
                            r, _, _ = select.select([sys.stdin], [], [], 0.05)
                            if r:
                                ch3 = sys.stdin.read(1)
                                return {'A': 'UP', 'B': 'DOWN'}.get(ch3, '')
                    return 'ESC'
                elif ch in ('\r', '\n'):
                    return 'ENTER'
                elif ch == '\x03':
                    raise KeyboardInterrupt
                elif ch in ('k', 'K'):
                    return 'UP'
                elif ch in ('j', 'J'):
                    return 'DOWN'
                elif ch in ('q', 'Q'):
                    return 'QUIT'
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # 4. ANSI Styling & Interactive Navigation Loop
    CURSOR_HIDE = "\033[?25l"
    CURSOR_SHOW = "\033[?25h"
    CLEAR_LINE = "\033[2K"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    REVERSE = "\033[7m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    GREEN = "\033[32m"

    selected_idx = 0
    top_idx = 0
    total = len(options)
    rendered_line_count = 0

    sys.stdout.write(CURSOR_HIDE)
    sys.stdout.flush()

    try:
        while True:
            visible_count = min(max_visible, total)
            if selected_idx < top_idx:
                top_idx = selected_idx
            elif selected_idx >= top_idx + visible_count:
                top_idx = selected_idx - visible_count + 1

            lines = []
            if prompt:
                lines.append(f"{BOLD}{prompt}{RESET}")

            # Top scroll indicator
            if top_idx > 0:
                lines.append(f"{DIM}  ▲ ({top_idx} more above){RESET}")
            elif total > visible_count:
                lines.append(f"{DIM}  ▲{RESET}")

            # Render visible options
            for i in range(top_idx, top_idx + visible_count):
                item_str = str(options[i])
                if i == selected_idx:
                    lines.append(f"{CYAN}{BOLD}❯{RESET} {REVERSE} {item_str} {RESET}")
                else:
                    lines.append(f"    {item_str}")

            # Bottom scroll indicator
            remaining_below = total - (top_idx + visible_count)
            if remaining_below > 0:
                lines.append(f"{DIM}  ▼ ({remaining_below} more below){RESET}")
            elif total > visible_count:
                lines.append(f"{DIM}  ▼{RESET}")

            lines.append(f"{DIM}Use ↑/↓ (or j/k) to move, Enter to select, 'q' to cancel{RESET}")

            if rendered_line_count > 0:
                sys.stdout.write(f"\033[{rendered_line_count}A")

            output_buffer = "\r" + "\n".join(f"{CLEAR_LINE}{line}" for line in lines) + "\n"
            sys.stdout.write(output_buffer)
            sys.stdout.flush()

            rendered_line_count = len(lines)

            key = _read_key()
            if key == 'UP':
                selected_idx = (selected_idx - 1) % total
            elif key == 'DOWN':
                selected_idx = (selected_idx + 1) % total
            elif key == 'ENTER':
                break
            elif key in ('QUIT', 'ESC'):
                raise KeyboardInterrupt("Selection cancelled by user.")

        # Clean up menu lines and display confirmation
        sys.stdout.write(f"\033[{rendered_line_count}A")
        for _ in range(rendered_line_count):
            sys.stdout.write(f"{CLEAR_LINE}\n")
        sys.stdout.write(f"\033[{rendered_line_count}A")

        if prompt:
            sys.stdout.write(f"{BOLD}{prompt}{RESET} {GREEN}✔ {options[selected_idx]}{RESET}\n")
        else:
            sys.stdout.write(f"{GREEN}✔ Selected: {BOLD}{options[selected_idx]}{RESET}\n")
        sys.stdout.flush()

        return options[selected_idx]

    finally:
        sys.stdout.write(CURSOR_SHOW)
        sys.stdout.flush()

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
        choice = choice("fire on yourself", "fire on them", "check inventory", "use item")        
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
            choice = choice(inv)

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
    

            
