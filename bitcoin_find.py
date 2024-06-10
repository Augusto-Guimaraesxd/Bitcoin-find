import secrets
from ecdsa import SECP256k1, SigningKey
import hashlib
from binascii import hexlify, unhexlify
import os
from colorama import Fore
import json

with open('wallets.json', 'r') as file:
    wallets = json.load(file)

wallets_set = set(wallets)

def encontrar_bitcoins(key, min_value, max_value, should_stop):
    start_time = time.time()
    chaves_buscadas = 0
    ultima_chave = ''

    print('Buscando Bitcoins...')

    while not should_stop():
        key += 1
        pkey = format(key, '064x')
        ultima_chave = pkey
        chaves_buscadas += 1

        if time.time() - start_time >= 10:
            tempo_decorrido = time.time() - start_time
            chaves_por_segundo = chaves_buscadas / tempo_decorrido

            os.system('cls' if os.name == 'nt' else 'clear')
            print('Resumo:')
            print(f'Velocidade: {chaves_por_segundo:.2f} chaves por segundo')
            print(f'Chaves buscadas: {chaves_buscadas:,}')
            print(f'Ultimos caracteres da ultima chave buscada: {ultima_chave[-5:]}')

            start_time = time.time()
            chaves_buscadas = 0

        public_key = generate_public(pkey)
        if public_key in wallets_set:
            tempo_total = time.time() - start_time
            print(f'Velocidade: {chaves_buscadas / tempo_total:.2f} chaves por segundo')
            print(f'Tempo: {tempo_total:.2f} segundos')
            print(f'Private key: {Fore.GREEN}{pkey}{Fore.RESET}')
            print(f'WIF: {Fore.GREEN}{generate_wif(pkey)}{Fore.RESET}')

            with open('keys.txt', 'a') as file:
                file.write(f'Private key: {pkey}, WIF: {generate_wif(pkey)}\n')
                print('Chave escrita no arquivo com sucesso.')

            print('ACHEI!!!! 🎉🎉🎉🎉🎉')
            exit(0)

def generate_public(private_key):
    private_key_bytes = unhexlify(private_key)
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key = verifying_key.to_string("compressed")
    return hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).hexdigest()

def generate_wif(private_key):
    private_key_bytes = unhexlify(private_key)
    signing_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    private_wif = signing_key.to_pem()
    return private_wif.decode()

if __name__ == "__main__":
    import sys
    import json

    worker_data = json.loads(sys.argv[1])
    encontrar_bitcoins(worker_data["key"], worker_data["min"], worker_data["max"], lambda: worker_data["shouldStop"])