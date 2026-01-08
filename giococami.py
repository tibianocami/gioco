import random

# =========================
# DATI INIZIALI
# =========================
edifici = ["Casa", "Banca", "Farmacia"]

armi_base = [
    {"nome": "Coltello", "danno": 5, "tipo": "melee"},
    {"nome": "Spada Leggera", "danno": 10, "tipo": "melee"},
    {"nome": "Ascia", "danno": 15, "tipo": "melee"},
    {"nome": "Mazza", "danno": 20, "tipo": "melee"},
    {"nome": "Martello da Guerra", "danno": 25, "tipo": "melee"},
    {"nome": "Bastone Magico", "danno": 30, "tipo": "magico"},
    {"nome": "Spada Pesante", "danno": 35, "tipo": "melee"},
    {"nome": "Arco Leggero", "danno": 40, "tipo": "a distanza"},
    {"nome": "Lancia Divina", "danno": 45, "tipo": "a distanza"}
]

armature_base = [
    {"nome": "Armatura di Pelle", "hp_bonus": 15, "immunita": False},
    {"nome": "Armatura Medievale", "hp_bonus": 25, "immunita": False},
    {"nome": "Armatura Antibatteriologica", "hp_bonus": 10, "immunita": True},
    {"nome": "Armatura Antisommossa", "hp_bonus": 30, "immunita": False}  
]

# =========================
# FUNZIONI
# =========================

def crea_personaggio():
    nome = input("Inserisci il nome del personaggio: ")
    return {
        "nome": nome,
        "hp": 100,
        "hp_max": 100,
        "fame": 100,
        "arma": armi_base[0],  # Coltello di default
        "armatura": None,
        "mostri_uccisi": 0,
        "edifici_visitati": 0,
        "giorno_max": 0,
        "infetto": False,
        "vaccino": False,
        "monete": 0,
        "zaino": {
            "cibo": 0,
            "vaccino": 0
        }
    }

# =========================
# INVENTARIO INTERATTIVO
# =========================

def inventario_interattivo(personaggio):
    while True:
        print("\n====== INVENTARIO ======")
        print(f"HP: {personaggio['hp']}/{personaggio['hp_max']}")
        print(f"Fame: {personaggio['fame']}/100")
        print(f"Cibo: {personaggio['zaino']['cibo']}")
        print(f"Vaccini: {personaggio['zaino']['vaccino']}")
        print(f"Monete: {personaggio['monete']}")
        print(f"Infetto: {'Sì' if personaggio['infetto'] else 'No'}")
        print(f"Protezione da vaccino attiva: {'Sì' if personaggio['vaccino'] else 'No'}")
        print("========================")
        print("1: Mangia")
        print("2: Usa vaccino")
        print("3: Torna al menu")

        scelta = input("Scegli (1-3) >> ")

        if scelta == "1":
            # Mangiare: fame +15, e se supera 100 cura HP fino a max
            if personaggio["zaino"]["cibo"] > 0:
                personaggio["zaino"]["cibo"] -= 1
                personaggio["fame"] += 15
                if personaggio["fame"] > 100:
                    eccesso = personaggio["fame"] - 100
                    personaggio["fame"] = 100
                    personaggio["hp"] += eccesso
                    if personaggio["hp"] > personaggio["hp_max"]:
                        personaggio["hp"] = personaggio["hp_max"]
                    print(f"Hai mangiato! Fame al massimo, HP +{eccesso}")
                else:
                    print(f"Hai mangiato! Fame +15")
                print(f"Fame: {personaggio['fame']} | HP: {personaggio['hp']}")
            else:
                print("Non hai cibo!")
        elif scelta == "2":
            # Usa vaccino: blocca infezione finché non reinfettato
            if personaggio["zaino"]["vaccino"] > 0:
                personaggio["zaino"]["vaccino"] -= 1
                personaggio["vaccino"] = True
                personaggio["infetto"] = False
                print("Vaccino usato! Sei immune finché non vieni infettato di nuovo.")
            else:
                print("Non hai vaccini!")
        elif scelta == "3":
            print("Tornando al menu principale...")
            break
        else:
            print("Scelta non valida!")

# =========================
# FUNZIONI GIOCO
# =========================

def regole():
    print("\n===== REGOLE DEL GIOCO =====")
    curiosita = [
        "1. Puoi mangiare solo se hai cibo nello zaino. Mangiare aumenta la fame di 15.",
        "   Se la fame supera il massimo (100), l'eccesso cura anche i tuoi HP fino al massimo.",
        "2. I vaccini ti proteggono dall'infezione fino a quando non vieni infettato di nuovo.",
        "3. Ogni arma ha un danno specifico. Equipaggia sempre quella più potente che trovi.",
        "4. Le armature riducono il danno subito dai mostri e alcune conferiscono immunità alle infezioni.",
        "5. Puoi equipaggiare solo un'arma e un'armatura alla volta.",
        "6. Esplorando edifici puoi trovare loot casuale: cibo, armi, armature, vaccini e monete.",
        "7. Se sei infetto e non sei protetto dal vaccino, perdi HP ogni giorno.",
        "8. Ogni 5 giorni appare il mercante, che permette di incantare armi (+15 danno) o armature (+30 HP bonus).",
        "9. Puoi scappare dai mostri evitando il combattimento ma senza ricevere loot.",
        "10. Monete e cibo possono essere accumulati nello zaino e utilizzati strategicamente.",
        "11. L'inventario è interattivo: puoi scegliere di mangiare o usare un vaccino in qualsiasi momento dal menu.",
        "12. Se la fame scende a 0, perdi HP ogni giorno finché non mangi."
    ]
    for c in curiosita:
        print(c)
    print("============================\n")


def loot(personaggio, edificio):
    if random.randint(1,100) <= 57:
        arma = random.choice(armi_base)
        print(f"Hai trovato un'arma: {arma['nome']} (Danno: {arma['danno']})")
        scelta = input(f"Vuoi equipaggiare {arma['nome']} (Danno: {arma['danno']}) al posto di {personaggio['arma']['nome']} (Danno: {personaggio['arma']['danno']}? (s/n): ")
        if scelta.lower() == 's':
            personaggio['arma'] = arma
            print(f"Hai equipaggiato {arma['nome']}!")

    if random.randint(1,100) <= 25:
        arm = random.choice(armature_base)
        print(f"Hai trovato un'armatura: {arm['nome']} (HP bonus: {arm['hp_bonus']})")
        if personaggio['armatura']:
            scelta = input(f"Vuoi sostituire {personaggio['armatura']['nome']} (HP bonus: {personaggio['armatura']['hp_bonus']}) con {arm['nome']} (Hp bonus:{arm['hp_bonus']}? (s/n): ")
            if scelta.lower() == 's':
                personaggio['armatura'] = arm
                print(f"Hai equipaggiato {arm['nome']}!")
        else:
            scelta = input(f"Vuoi equipaggiare {arm['nome']}? (s/n): ")
            if scelta.lower() == 's':
                personaggio['armatura'] = arm
                print(f"Hai equipaggiato {arm['nome']}!")

    if random.randint(1,100) <= 50:
        cibo = random.choice([1,2,3])
        personaggio["zaino"]["cibo"] += cibo
        print(f"Hai trovato {cibo} unità di cibo!")

    if edificio=="Farmacia" and random.randint(1,100)<=50:
        personaggio["zaino"]["vaccino"] += 1
        print("Hai trovato un vaccino!")

    if edificio=="Banca" and random.randint(1,100)<=50:
        monete = random.randint(1,3)
        personaggio["monete"] += monete
        print(f"Hai trovato {monete} monete!")

def combattimento(personaggio, mostri):
    for mostro in mostri:
        print(f"\nMostro con {mostro['hp']} HP e {mostro['danno']} danno!")
        while mostro["hp"] > 0:
            scelta = input("1: Attacca 2: Scappa >> ")
            if scelta == "2":
                print("Sei fuggito!")
                return
            else:
                danno = personaggio['arma']['danno']
                mostro["hp"] -= danno
                print(f"Hai inflitto {danno} danno. Mostro HP: {mostro['hp']}")
                if mostro["hp"] > 0:
                    danno_m = mostro["danno"]
                    if personaggio['armatura']:
                        danno_m -= personaggio['armatura']['hp_bonus']//10
                        if danno_m<0: danno_m=0
                    personaggio["hp"] -= danno_m
                    print(f"Il mostro ti colpisce! HP: {personaggio['hp']}")
                    if not personaggio["armatura"] and random.randint(1,100)<=20 and not personaggio["vaccino"]:
                        personaggio["infetto"] = True
                        print("Sei stato infettato!")
                if personaggio["hp"] <= 0:
                    print("Sei morto!")
                    return
        personaggio["mostri_uccisi"] += 1

def esplora_edificio(personaggio):
    edificio = random.choice(edifici)
    print(f"\nEdificio trovato: {edificio}")
    personaggio["edifici_visitati"] += 1
    scelta = input("1: Esplora 2: Continua il viaggio >> ")
    if scelta=="1":
        if edificio=="Farmacia" and random.randint(1,100)<=50:
            personaggio['zaino']['vaccino'] += 1
            print("Hai trovato un vaccino!")
        elif random.randint(1,100)<=50:
            num_mostri = random.randint(1,3)
            print(f"hai incontrato {num_mostri} mostri!")
            mostri = [{"hp": random.choice([25,50]), "danno": random.choice([5,10])} for _ in range(num_mostri)]
            combattimento(personaggio, mostri)
        else:
            loot(personaggio, edificio)

def mercante(personaggio):
    print("\nÈ apparso un mercante!")
    scelta = input("Vuoi incantare arma (+15 danno per 5 monete) o armatura (+30 HP per 10 monete)? (arma/armatura/no) >> ")
    if scelta=="arma" and personaggio["monete"]>=5:
        personaggio["arma"]["danno"] += 15
        personaggio["monete"] -=5
        print(f"Arma incantata! Nuovo danno: {personaggio['arma']['danno']}")
    elif scelta=="armatura" and personaggio["monete"]>=10:
        if personaggio["armatura"]:
            personaggio["armatura"]["hp_bonus"] += 30
            personaggio["monete"] -=10
            print(f"Armatura incantata! Nuovo HP bonus: {personaggio['armatura']['hp_bonus']}")
        else:
            print("Non hai armatura equipaggiata!")
    else:
        print("Non hai monete o hai scelto di non incantare.")

def gioca(personaggio):
    global giorno
    print(f"\nGiorno {giorno+1} - HP: {personaggio['hp']} | Fame: {personaggio['fame']} | Infetto: {'Sì' if personaggio['infetto'] else 'No'} | Monete: {personaggio['monete']}")
    personaggio["fame"] -= 5
    if personaggio["fame"]<0:
        personaggio["fame"]=0
        personaggio["hp"]-=10
        print("Hai fame! HP -10")
    if personaggio["infetto"]:
        if not personaggio["vaccino"]:
            personaggio["hp"]-=5
            print("Sei infetto! HP -5 oggi.")
        else:
            personaggio["vaccino"]=False
    esplora_edificio(personaggio)
    giorno += 1
    personaggio["giorno_max"]=giorno
    if giorno%5==0:
        mercante(personaggio)
    if personaggio["hp"]<=0:
        print("Sei morto!")
        return False
    print(f"Fine giorno {giorno}\n{'-'*60}")
    return True

def game_over(personaggio):
    print("\n" + "="*60)
    print("      💀 SEI MORTO! 💀")
    print("="*60)
    print(f"Nome: {personaggio['nome']}")
    print(f"Giorni sopravvissuti: {personaggio['giorno_max']}")
    print(f"Mostri uccisi: {personaggio['mostri_uccisi']}")
    print(f"Edifici visitati: {personaggio['edifici_visitati']}")
    print(f"Monete raccolte: {personaggio['monete']}")
    print("="*60)
    
    while True:
        print("1: Riprova")
        print("2: Esci")
        scelta = input("Scegli un'opzione (1-2) >> ")
        if scelta=="1":
            nuovo_personaggio = crea_personaggio()
            return nuovo_personaggio
        elif scelta=="2":
            print("Grazie per aver giocato!")
            return None
        else:
            print("Scelta non valida, riprova.")

# =========================
# CICLO PRINCIPALE
# =========================

personaggio = crea_personaggio()
giorno = 0
txt = -1
TITOLO = f"\n{'='*60}\n{' '*25}UTOPIA{' '*20}\n{'='*60}\n"

while True:
    if giorno == 0:
        print(TITOLO)
    else:
        print(f"- Giorno {giorno} - HP: {personaggio['hp']} | Fame: {personaggio['fame']} | Infetto: {'Sì' if personaggio['infetto'] else 'No'} | Monete: {personaggio['monete']}")
    if giorno == 0 :
        txt = ("Gioca")
    else:
        txt = ("Continua")

    print(f"1: {txt}")
    print("2: Inventario")
    print("3: Statistiche")
    print("4: Regole")
    print("5: Esci")
    scelta = input("Scegli (1-5) >> ")

    if scelta=="1":
        alive=gioca(personaggio)
        if not alive:
            personaggio = game_over(personaggio)
            if not personaggio:
                break
    elif scelta=="2":
        inventario_interattivo(personaggio)  
    elif scelta=="3":
        print(f"Nome: {personaggio['nome']}, Mostri uccisi: {personaggio['mostri_uccisi']}, Giorni: {personaggio['giorno_max']}, Edifici: {personaggio['edifici_visitati']}, Monete: {personaggio['monete']}")
    elif scelta=="4":
        regole()
    elif scelta=="5":
        print("Grazie per aver giocato!")
        break
    else:
        print("Scelta non valida.")
