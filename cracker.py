import hashlib
import time
import multiprocessing
from colorama import Fore, init

init(autoreset=True)

def hash_word(word):
    return hashlib.sha256(word.strip().encode()).hexdigest()

def crack_chunk(chunk, target_hash, result_queue):
    for word in chunk:
        if hash_word(word) == target_hash:
            result_queue.put(word.strip())
            return
    result_queue.put(None)

def main():
    target = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
    wordlist_file = 'wordlist.txt'
    
    try:
        with open(wordlist_file, 'r', encoding='utf-8') as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist not found.")
        return

    num_cores = multiprocessing.cpu_count()
    print(f"{Fore.CYAN}[*] Utilizing {num_cores} CPU cores for parallel cracking...")
    
    chunk_size = max(1, len(words) // num_cores)
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    
    result_queue = multiprocessing.Queue()
    processes = []
    start_time = time.time()
    
    for chunk in chunks:
        p = multiprocessing.Process(target=crack_chunk, args=(chunk, target, result_queue))
        processes.append(p)
        p.start()
        
    found_password = None
    for _ in range(len(processes)):
        res = result_queue.get()
        if res:
            found_password = res
            break
            
    for p in processes:
        p.terminate()
        
    duration = time.time() - start_time
    
    if found_password:
        print(f"\n{Fore.GREEN}[+] SUCCESS: Password found: {found_password}")
        print(f"{Fore.GREEN}[+] Time taken: {duration:.4f} seconds")
    else:
        print(f"\n{Fore.RED}[!] Password not found in wordlist.")

if __name__ == '__main__':
    main()
