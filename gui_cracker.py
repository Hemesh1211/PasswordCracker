import customtkinter as ctk
import hashlib
import os
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OP_PASSWORD_CRACKER // HUD")
        self.geometry("650x650")

        self.label = ctk.CTkLabel(self, text="PASS_CRACKER v2.2 // HUD", font=("Courier", 22, "bold"), text_color="#06b6d4")
        self.label.pack(pady=20)

        self.hash_entry = ctk.CTkEntry(self, placeholder_text="SHA-256 Hash", width=550)
        self.hash_entry.pack(pady=10)
        # Correct SHA-256 hash for 'admin123' -> 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
        self.hash_entry.insert(0, "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9")

        self.crack_button = ctk.CTkButton(self, text="INITIALIZE ATTACK", fg_color="#06b6d4", text_color="black", font=("Courier", 14, "bold"), command=self.start_crack)
        self.crack_button.pack(pady=20)

        self.log = ctk.CTkTextbox(self, width=550, height=300, fg_color="#0b1322", font=("Consolas", 12))
        self.log.pack(pady=10)
        self.log.insert("0.0", "[*] SYSTEM READY. LOADING WORDLIST...\n")

    def start_crack(self):
        target = self.hash_entry.get().strip().lower()
        self.log.delete("0.0", "end")
        threading.Thread(target=self.run_logic, args=(target,), daemon=True).start()

    def run_logic(self, target):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        wordlist_path = os.path.join(base_dir, "wordlist.txt")
        
        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                for line in f:
                    w = line.strip()
                    if not w: continue
                    
                    hashed = hashlib.sha256(w.encode()).hexdigest()
                    self.log.insert("end", f"[*] TRYING: {w}\n  -> {hashed[:12]}...\n")
                    self.log.see("end")
                    
                    if hashed == target:
                        self.log.insert("end", f"\n[!] MATCH FOUND!\n[+] PASSWORD: {w}\n")
                        return
            self.log.insert("end", "\n[!] FAILED: PASSWORD NOT IN WORDLIST.\n")
        except Exception as e:
            self.log.insert("end", f"\n[!] ERROR: {e}\n")

if __name__ == "__main__":
    app = CrackerApp()
    app.mainloop()
