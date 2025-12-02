# ========== IMPORTS ==========
import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time
from pynput import keyboard
# pynput = bibliothèque pour détecter les touches du clavier
from pynput.keyboard import Key
# Key = pour utiliser les touches spéciales (Echap, F1, etc.)


# ========== VARIABLES GLOBALES ==========
bot_actif = False
en_pause = False


# ========== FONCTION DE GESTION DES TOUCHES ==========

def gerer_touches(key):
    """
    Fonction appelée automatiquement quand tu appuies sur une touche
    "key" = la touche que tu as appuyée
    """
    
    global en_pause, bot_actif
    
    try:
        # "try" = essaye de faire ça (peut causer une erreur)
        
        # Vérifier si c'est la touche P
        if key.char == 'p' or key.char == 'P':
            # key.char = le caractère de la touche
            # On vérifie 'p' et 'P' pour minuscule ET majuscule
            
            basculer_pause()
            # On appelle la fonction pause (la même que le bouton)
    
    except:
        # "except" = si y'a une erreur, fais ça à la place
        # Pourquoi une erreur ? Parce que les touches spéciales (Echap, F1...)
        # n'ont pas de ".char", donc ça plante
        
        # Vérifier si c'est la touche Echap
        if key == Key.esc:
            # Key.esc = la touche Echap (escape)
            
            arreter_bot()
            # On arrête le bot


# ========== FONCTION DU BOT ==========

def bot_clic():
    """Cette fonction fait cliquer le bot en boucle"""
    
    global bot_actif, en_pause
    
    # Compte à rebours de 3 secondes
    for i in range(3, 0, -1):
        if not bot_actif:
            return
        
        label_status.config(text=f"⏱️ Démarrage dans {i}s...")
        root.update()
        time.sleep(1)
    
    label_status.config(text="✅ Bot actif !", foreground="green")
    
    # Boucle principale du bot
    while bot_actif:
        if not en_pause:
            pyautogui.click()
            time.sleep(0.01)
        else:
            time.sleep(0.1)


# ========== FONCTIONS DES BOUTONS ==========

def demarrer_bot():
    """Fonction appelée quand on clique sur le bouton START"""
    
    global bot_actif, en_pause
    
    if not bot_actif:
        bot_actif = True
        en_pause = False
        
        btn_start.config(state="disabled")
        btn_pause.config(state="normal")
        btn_stop.config(state="normal")
        
        # Lancer le bot dans un thread
        thread = threading.Thread(target=bot_clic, daemon=True)
        thread.start()
        
        # NOUVEAU : Lancer l'écoute du clavier
        listener = keyboard.Listener(on_press=gerer_touches)
        # keyboard.Listener = crée un "écouteur" de clavier
        # on_press=gerer_touches = quand une touche est appuyée, appelle gerer_touches()
        
        listener.start()
        # .start() = démarre l'écoute en arrière-plan
        # Maintenant, dès que tu appuies sur une touche, gerer_touches() est appelée


def basculer_pause():
    """Fonction appelée quand on clique sur PAUSE ou qu'on appuie sur P"""
    
    global en_pause
    
    if bot_actif:
        en_pause = not en_pause
        
        if en_pause:
            label_status.config(text="⏸️ En pause", foreground="orange")
            btn_pause.config(text="▶️ Reprendre")
        else:
            label_status.config(text="✅ Bot actif !", foreground="green")
            btn_pause.config(text="⏸️ Pause")


def arreter_bot():
    """Fonction appelée quand on clique sur STOP ou qu'on appuie sur Echap"""
    
    global bot_actif, en_pause
    
    bot_actif = False
    en_pause = False
    
    label_status.config(text="⛔ Bot arrêté", foreground="red")
    btn_pause.config(text="⏸️ Pause")
    
    btn_start.config(state="normal")
    btn_pause.config(state="disabled")
    btn_stop.config(state="disabled")


# ========== CRÉATION DE L'INTERFACE ==========

root = tk.Tk()
root.title("AutoClicker 🎯")
root.geometry("400x280")
root.resizable(False, False)
root.configure(bg="#2c3e50")


# ========== TITRE ==========

label_titre = tk.Label(
    root,
    text="🎯 AutoClicker ",
    font=("Arial", 20, "bold"),
    bg="#2c3e50",
    fg="white"
)
label_titre.pack(pady=20)


# ========== STATUS ==========

label_status = tk.Label(
    root,
    text="⏸️ En attente",
    font=("Arial", 14),
    bg="#2c3e50",
    fg="orange"
)
label_status.pack(pady=10)


# ========== BOUTONS ==========

frame_boutons = tk.Frame(root, bg="#2c3e50")
frame_boutons.pack(pady=20)

btn_start = ttk.Button(
    frame_boutons,
    text="▶️ START",
    command=demarrer_bot,
    width=15
)
btn_start.grid(row=0, column=0, padx=5, pady=5)

btn_pause = ttk.Button(
    frame_boutons,
    text="⏸️ PAUSE",
    command=basculer_pause,
    width=15,
    state="disabled"
)
btn_pause.grid(row=0, column=1, padx=5, pady=5)

btn_stop = ttk.Button(
    frame_boutons,
    text="⏹️ STOP",
    command=arreter_bot,
    width=32,
    state="disabled"
)
btn_stop.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


# ========== INSTRUCTIONS ==========

frame_info = tk.Frame(root, bg="#34495e", relief="ridge", bd=2)
frame_info.pack(pady=10, padx=20, fill="x")

label_info = tk.Label(
    frame_info,
    text="📌 Place ta souris avant START\n⌨️ Touche P = Pause | Touche Echap = Stop",
    # "\n" = saut de ligne (retour à la ligne)
    font=("Arial", 9),
    bg="#34495e",
    fg="white",
    justify="center"
    # justify="center" = centre le texte (au lieu de "left" par défaut)
)
label_info.pack(pady=8)


# ========== LANCER L'INTERFACE ==========

root.mainloop()