import json
import threading
import readline
from colorama import Fore
import time

def start_worker(key, min_value, max_value, should_stop_event):
    worker_thread = threading.Thread(target=worker_thread, args=(key, min_value, max_value, should_stop_event))
    worker_thread.start()
    return worker_thread

def worker_thread(key, min_value, max_value, should_stop):
    encontrar_bitcoins(key, min_value, max_value, should_stop.is_set)

def main():
    should_stop_event = threading.Event()

    print(Fore.LIGHTSALMON_EX + "╔════════════════════════════════════════════════════════╗")
    print(Fore.RESET + Fore.CYAN + "   ____ _____ ____   _____ ___ _   _ ____  _____ ____   ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.CYAN + "  | __ )_   _/ ___| |  ___|_ _| \\ | |  _ \\| ____|  _ \\  ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.CYAN + "  |  _ \\ | || |     | |_   | ||  \\| | | | |  _| | |_) | ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.CYAN + "  | |_) || || |___  |  _|  | || |\\  | |_| | |___|  _ <  ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.CYAN + "  |____/ |_| \\____| |_|   |___|_| \\_|____/|_____|_| \\_\\ ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.CYAN + "                                                        ")
    print(Fore.RESET + Fore.LIGHTSALMON_EX + "║\n" +
          Fore.RESET + Fore.LIGHTSALMON_EX + "╚══════════════════════" + Fore.GREEN + "Investidor Internacional - v0.4" + Fore.RESET + Fore.LIGHTSALMON_EX + "═══╝" + Fore.RESET)

    answer = input(f'Escolha uma carteira puzzle( {Fore.CYAN}1{Fore.RESET} - {Fore.CYAN}160{Fore.RESET}): ')
    if int(answer) < 1 or int(answer) > 160:
        print(Fore.RED + 'Erro: voce precisa escolher um numero entre 1 e 160' + Fore.RESET)
        exit(1)

    with open('ranges.json', 'r') as file:
        ranges = json.load(file)

    min_value = int(ranges[int(answer) - 1]['min'], 16)
    max_value = int(ranges[int(answer) - 1]['max'], 16)
    print(f'Carteira escolhida: {Fore.CYAN}{answer}{Fore.RESET}, Min: {Fore.YELLOW}{min_value}{Fore.RESET}, Max: {Fore.YELLOW}{max_value}{Fore.RESET}')
    print(f'Numero possivel de chaves: {Fore.YELLOW}{max_value - min_value:,}{Fore.RESET}')
    key = min_value

    option = input(f'Escolha uma opcao ({Fore.CYAN}1{Fore.RESET} - Comecar do inicio, {Fore.CYAN}2{Fore.RESET} - Escolher uma porcentagem, {Fore.CYAN}3{Fore.RESET} - Escolher minimo): ')

    if option == '2':
        percentage = float(input('Escolha um numero entre 0 e 1: '))
        if percentage < 0 or percentage > 1:
            print(Fore.RED + 'Erro: voce precisa escolher um numero entre 0 e 1' + Fore.RESET)
            exit(1)

        range_value = max_value - min_value
        key = min_value + int(range_value * percentage)
        print(f'Comecando em: {Fore.YELLOW}0x{key:064x}{Fore.RESET}')
    elif option == '3':
        min_value = int(input('Entre o minimo: '), 16)
        key = min_value
    else:
        key = min_value

    worker = start_worker(key, min_value, max_value, should_stop_event)

    try:
        worker.join()
    except KeyboardInterrupt:
        should_stop_event.set()
        worker.join()

if __name__ == "__main__":
    main()