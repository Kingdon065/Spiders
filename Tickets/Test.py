from colorama import init, Fore, Back, Style
init(autoreset=True)
print(Fore.RED + 'some blue text')
print(Back.CYAN + 'cyan background')
print(Style.DIM + 'in dim text')
print('auto set to normal now')