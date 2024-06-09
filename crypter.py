import os
import time

try:
    from tqdm import tqdm
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "tqdm"])
    from tqdm import tqdm


class Color:
    violet = "\033[35;1m"
    red = "\u001b[31;1m"
    cyan = "\u001b[36;1m"
    green = "\u001b[32;1m"
    yellow = "\u001b[33;1m"
    fucsia = "\u001b[35;1m"
    gray = "\033[90;1m"
    italic = "\033[3;1m"
    reset = "\u001b[0m"


def cls():
    os.system("cls") if os.name == 'nt' else os.system("clear")


def intro(dynamic):
    cls()
    logo = [
        Color.green,
        "                          __            \n",
        "   ____ _____ _  _ ____  / /_ __  _____ \n",
        "  / ___/ ___/ / / / __ \/ __/ _ \/ ___/ \n",
        " / /__/ /  / /_/ / /_/ / /_/  __/ /     \n",
        " \___/_/   \__, / .___/\__/\___/_/      \n",
        f"          /____/_/ {Color.fucsia}{Color.italic}   by alfanowski {Color.reset} \n"
        f"{Color.red} ------------------------------------- \n{Color.reset}\n"
    ]
    for i in logo:
        for j in i:
            print(j, end='', flush=True)
            time.sleep(0.01) if dynamic and not j.isalpha() else None
            time.sleep(0.08) if dynamic and j.isalpha() else None
    time.sleep(0.4) if dynamic else None


def selezione():
    intro(False)
    print(f"  {Color.gray}({Color.green}X{Color.gray}){Color.yellow} Exit")
    print(f"  {Color.gray}({Color.green}1{Color.gray}){Color.cyan} Encrypt File")
    print(f"  {Color.gray}({Color.green}2{Color.gray}){Color.cyan} Decrypt File \n")
    sel = input(f"{Color.fucsia}   >> {Color.reset}").lower()
    return sel


def process(action):
    while True:
        intro(False)
        print(f"  {Color.gray}({Color.yellow}B{Color.gray}){Color.yellow} Back \n")
        if action == 1:
            print(f"{Color.gray}{Color.italic}  Enter the path of the file to be encrypted")
        elif action == 2:
            print(f"{Color.gray}{Color.italic}  Enter the path to the file to decrypt")
        sel = input(f"{Color.fucsia}   >> {Color.reset}").strip()
        if sel:
            break
    if sel.lower() == 'b':
        return False
    sel = sel.strip("'\"")
    sel = os.path.abspath(sel)
    intro(False)
    if not os.path.exists(sel):
        print(f"{Color.red}  Invalid path")
        input(f"{Color.gray}\n  [Press enter] {Color.reset} ")
        return True
    _, ext = os.path.splitext(sel)
    if (action == 1 and ext == ".wski") or (action == 2 and ext != ".wski"):
        print(f"{Color.red}  Invalid file!")
        input(f"{Color.gray}\n  [Press enter] {Color.reset} ")
        return True
    contr = crypt(sel, action == 1)
    if contr:
        print(f"  {Color.yellow}{sel.strip()}\n{Color.cyan}  {'Encrypted' if action == 1 else 'Decrypted'} successfully!")
    else:
        print(f"{Color.red}  An error occurred!")
    input(f"{Color.gray}\n  [Press enter] {Color.reset} ")


def crypt(nomeFile, type):
    try:
        with open(nomeFile, 'rb') as f:
            data = bytearray(f.read())
        key = 1
        print(Color.green, end='')
        with tqdm(total=len(data), desc='', unit='B', leave=False,
                bar_format='  {percentage:3.0f}% |{bar}|  ',
                ncols=35) as pbar:
            for i in range(len(data)):
                data[i] ^= key
                key = (key + 1) % 256
                pbar.update(1)
        print(Color.reset, end='')
        with open(nomeFile + '.wski', 'wb') if type else open(nomeFile[:-5], 'wb') as f:
                f.write(data)
        return True
    except Exception as e:
        return False


def main():
    intro(True)
    while True:
        sel = selezione()
        if sel == 'x':
            break
        elif sel in ['1','2']:
            while True:
                controllo = process(int(sel))
                if not controllo:
                    break
    cls()


main()
