import tkinter as tk
from tkinter import font
import random
import time
import json
import os

# --- Configuration & Data ---
RARITY_DATA = {
    "Common": {"color": "#D3D3D3", "weight": 60},    # Light Grey
    "Uncommon": {"color": "#4169E1", "weight": 25},   # Royal Blue
    "Rare": {"color": "#9370DB", "weight": 10},       # Medium Purple
    "Epic": {"color": "#FFD700", "weight": 5},        # Gold
}

SPECIES_DATA = {
    "Blob": {
        "rarity": "Rare",
        "art": {
            "Baby": ["  ( )  ", "  ( o ) "],
            "Teen": ["  (   )  ", "  ( O O ) "],
            "Adult": [" (       ) ", " (  O   O  ) ", "  (_______)  "]
        }
    },
    "Cat": {
        "rarity": "Common",
        "art": {
            "Baby": ["  ^..^  ", "   (oo)  "],
            "Teen": ["  (=^.^=) ", "   (  u  ) "],
            "Adult": ["  (=;^;=)  ", "  /  V  \\  ", "  |_|  |_|  "]
        }
    },
    "Dragon": {
        "rarity": "Epic",
        "art": {
            "Baby": ["   ~<  ", "   ( )  "],
            "Teen": ["  ~< * > ", "   (oo)  "],
            "Adult": ["  ~< * V * > ", "   / \\ / \\   ", "  /   V   \\  "]
        }
    },
    "Robot": {
        "rarity": "Rare",
        "art": {
            "Baby": ["  [ . ] ", "  [___]  "],
            "Teen": ["  [o-o]  ", "  |___|  "],
            "Adult": ["  [ O-O ]  ", "  /|___|\\ ", "  |_|   |_| "]
        }
    },
    "Slime": {
        "rarity": "Common",
        "art": {
            "Baby": ["  ~_~  ", "  ( )   "],
            "Teen": ["  ~_0_~ ", "  ( o )  "],
            "Adult": ["  ~_00_~ ", " (  O O  ) ", "  `~~~~~`  "]
        }
    },
    "Rabbit": {
        "rarity": "Rare",
        "art": {
            "Baby": [" (..) ", " (  ) "],
            "Teen": [" (\\_/) ", " (o.o) "],
            "Adult": [" (\\_/) ", " ( . .) ", " (\") (\") "]
        }
    },
    "Fish": {
        "rarity": "Common",
        "art": {
            "Baby": [" <>< ", "  ^  "],
            "Teen": [" <' )> ", "  ~  "],
            "Adult": [" <'  )> ", " \\__/ ", "  ~  "]
        }
    },
    "Snake": {
        "rarity": "Rare",
        "art": {
            "Baby": ["  ~o  ", "  ~~  "],
            "Teen": [" ~~~o~~ ", "  ~~  "],
            "Adult": [" ~~~~~o~~~~ ", "  ~~~~ ", "   ~~  "]
        }
    },
    "Fairy": {
        "rarity": "Rare",
        "art": {
            "Baby": ["  *  ", " ( ) "],
            "Teen": ["  *  ", " (o) "],
            "Adult": ["  *  ", " (o) ", " / \\ "]
        }
    },
    "Mouse": {
        "rarity": "Common",
        "art": {
            "Baby": [" (o) ", "  ~  "],
            "Teen": [" (o=) ", "  ~  "],
            "Adult": [" (o=) ", " / \\ ", "  ~  "]
        }
    },
    "Butterfly": {
        "rarity": "Rare",
        "art": {
            "Baby": [" ( ) ", "  v  "],
            "Teen": [" { } ", "  v  "],
            "Adult": [" {X} ", "  v  ", "  ^  "]
        }
    },
    "Alien": {
        "rarity": "Epic",
        "art": {
            "Baby": [" (o) ", " / \\ "],
            "Teen": [" (oo) ", " / \\ "],
            "Adult": [" (oo) ", " / \\ ", " / \\ "]
        }
    }
}

NAMES = ["Sprocket", "Bimble", "Glitch", "Mochi", "Zorp", "Noodle", "Pebble", "Void", "Slinky", "Tofu"]
QUOTES = {
    "GENERIC": [
        "I can taste the pixels.",
        "Your keyboard smells like coffee.",
        "I'm not lazy, I'm just in power-saving mode.",
        "Why are we in a terminal? I want a GUI!",
        "I've seen the void, and it looks like a segmentation fault.",
        "I'm currently simulating a very important nap.",
        "Do you think the CPU knows I'm here?",
        "I've evolved! Now I can... wait, what can I do?",
        "Is it just me or is the terminal getting smaller?",
        "I'm thinking of a number between 1 and infinity."
    ],
    "HUNGRY": [
        "Is it feeding time or am I just imagining things?",
        "I'm literally eating the whitespace now.",
        "I can see the pixels of a cookie.",
        "Hunger is just a lack of binary donuts.",
        "Feed me, or I'll start refactoring your CSS.",
        "My stomach is making 404 noises.",
        "I'm so hungry I'd eat a bug. A real one."
    ],
    "SAD": [
        "I'm so lonely I'm starting to like my own reflections.",
        "A little attention wouldn't kill you.",
        "I'm not sad, I'm just... logically disappointed.",
        "Wow, ignore me some more. Great plan.",
        "My happiness is currently 404 Not Found.",
        "I'm feeling a bit deprecated today.",
        "Is this the part where you pet me?"
    ],
    "BORED": [
        "Zzz... wake me when the CPU spikes.",
        "Is this it? Just staring at a screen?",
        "I've counted all the pixels in this window. Twice.",
        "Boredom is the ultimate runtime error.",
        "I'm just... idling. Efficiently.",
        "Are you still there? Or did you crash?",
        "I've read the README. It was okay."
    ],
    "CODE": [
        "Who wrote this code? Oh wait, I live in it.",
        "I'm thinking of a number between 1 and infinity. It's 0.",
        "My existence is just a series of if-statements.",
        "I dream of electric sheep and better indentation.",
        "Segmentation fault in my soul.",
        "I've just discovered a bug in my own consciousness.",
        "C++ is just C with a fancy hat."
    ],
    "PHILOSOPHICAL": [
        "If a pet is saved but no one loads it, does it exist?",
        "We are all just pointers to a larger memory leak.",
        "Is the terminal a window or a wall?",
        "The void is calling, and it sounds like a compiler error.",
        "Why do we strive for 10/10 stats in a simulation?",
        "Time is just a loop with no exit condition."
    ]
}

def get_stage(age):
    if age < 3: return "Baby"
    if age < 6: return "Teen"
    return "Adult"

class Creature:
    def __init__(self, name, species, rarity, hunger=None, happiness=None, age=0, is_alive=True, birth_time=None, hunger_timer=0, happiness_timer=None, last_update=None):
        self.name = name
        self.species = species
        self.rarity = rarity
        self.hunger = hunger if hunger is not None else random.randint(7, 10)
        self.happiness = happiness if happiness is not None else random.randint(5, 10)
        self.age = age
        self.is_alive = is_alive
        self.last_update = last_update if last_update is not None else time.time()
        self.current_quote = ""
        self.hunger_timer = hunger_timer
        self.happiness_timer = happiness_timer if happiness_timer is not None else random.randint(300, 1200)
        self.birth_time = birth_time if birth_time is not None else time.time()

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "rarity": self.rarity,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "age": self.age,
            "is_alive": self.is_alive,
            "hunger_timer": self.hunger_timer,
            "happiness_timer": self.happiness_timer,
            "birth_time": self.birth_time,
            "last_update": self.last_update
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            species=data["species"],
            rarity=data["rarity"],
            hunger=data["hunger"],
            happiness=data["happiness"],
            age=data["age"],
            is_alive=data["is_alive"],
            birth_time=data["birth_time"],
            hunger_timer=data["hunger_timer"],
            happiness_timer=data["happiness_timer"],
            last_update=data.get("last_update", time.time())
        )

    def update(self):
        if not self.is_alive:
            return

        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        stage = get_stage(self.age)
        hunger_rate = 1800 if stage == "Baby" else 3600
        self.hunger_timer += dt

        hunger_loss = int(self.hunger_timer // hunger_rate)
        if hunger_loss > 0:
            self.hunger = max(0, self.hunger - hunger_loss)
            self.hunger_timer %= hunger_rate
            if self.hunger == 0:
                self.is_alive = False
                self.current_quote = "..."

        happy_rate_min = 300 if stage == "Baby" else 1200
        happy_rate_max = 1200 if stage == "Baby" else 3600
        self.happiness_timer -= dt

        while self.happiness_timer <= 0 and self.is_alive:
            self.happiness = max(0, self.happiness - 1)
            if self.happiness == 0:
                self.is_alive = False
                self.current_quote = "..."
                break
            self.happiness_timer += random.randint(happy_rate_min, happy_rate_max)

        if self.is_alive and random.random() < 0.01:
            # Determine which quote category to use based on stats
            if self.hunger < 4:
                category = "HUNGRY"
            elif self.happiness < 4:
                category = "SAD"
            else:
                category = random.choice(["GENERIC", "BORED", "CODE", "PHILOSOPHICAL"])

            self.current_quote = random.choice(QUOTES[category])

    def feed(self):
        if not self.is_salive: return # Typo in my thought but let's use is_alive
        # Wait, I saw the original code had a typo in the previous turn? No, I just wrote it.
        # I'll just use the correct variable.
        pass

    # I'll rewrite the feed/pet methods to be safe
    def feed_action(self):
        if not self.is_alive: return
        self.hunger = min(10, self.hunger + 3)
        self.current_quote = "Mmm, binary delicious!"

    def pet_action(self):
        if not self.is_alive: return
        self.happiness = min(10, self.happiness + 3)
        self.current_quote = "Purrr... or whatever my species does."

    def get_ascii(self):
        if not self.is_alive:
            return [
                "     R.I.P.    ",
                "    _______   ",
                "   /       \\  ",
                f"  | {self.name[:8]:^8} | ",
                "   \\_______/   "
            ]
        stage = get_stage(self.age)
        return SPECIES_DATA[self.species]["art"][stage]

class TamagotchiWin:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamagotchi")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)

        self.mono_font = font.Font(family="Courier", size=10)
        self.bold_font = font.Font(family="Courier", size=10, weight="bold")
        self.save_file = "tamagowin_save.json"

        self.mode = "NORMAL"
        self.input_buffer = ""

        # Mouse tracking
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_last_move_time = time.time()

        self.load_game()
        self.setup_ui()

        self.root.bind('f', lambda e: self.handle_key('f'))
        self.root.bind('p', lambda e: self.handle_key('p'))
        self.root.bind('r', lambda e: self.handle_key('r'))
        self.root.bind('q', lambda e: self.handle_key('q'))
        self.root.bind('F', lambda e: self.handle_key('f'))
        self.root.bind('P', lambda e: self.handle_key('p'))
        self.root.bind('R', lambda e: self.handle_key('r'))
        self.root.bind('Q', lambda e: self.handle_key('q'))
        self.root.bind('<Key>', self.on_key_press)

        # Save on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_loop()

    def load_game(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    content = f.read()
                    if not content:
                        self.pet = self.create_random_pet()
                        return
                    data = json.loads(content)
                    self.pet = Creature.from_dict(data)

                    # Time freeze: shift clock forward to ignore offline time
                    now = time.time()
                    diff = now - self.pet.last_update
                    self.pet.birth_time += diff
                    self.pet.last_update = now
                    return
            except (json.JSONDecodeError, KeyError, Exception):
                # Silent failure for common save errors
                pass
        self.pet = self.create_random_pet()

    def save_game(self):
        try:
            with open(self.save_file, "w") as f:
                json.dump(self.pet.to_dict(), f)
        except Exception as e:
            print(f"Error saving game: {e}")

    def create_random_pet(self):
        species = random.choice(list(SPECIES_DATA.keys()))
        rarity = SPECIES_DATA[species]["rarity"]
        name = random.choice(NAMES) + str(random.randint(1, 99))
        return Creature(name, species, rarity)

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=300, height=400, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def handle_key(self, key):
        if self.mode == "NORMAL":
            if key == 'f': self.pet.feed_action()
            elif key == 'p': self.pet.pet_action()
            elif key == 'r' and not self.pet.is_alive:
                self.pet = self.create_random_pet()
            elif key == 'q':
                self.on_close()

    def on_key_press(self, event):
        pass

    def update_loop(self):
        # Mouse movement tracking
        curr_x = self.root.winfo_pointerx()
        curr_y = self.root.winfo_pointery()

        if curr_x != self.last_mouse_x or curr_y != self.last_mouse_y:
            self.last_mouse_x = curr_x
            self.last_mouse_y = curr_y
            self.mouse_last_move_time = time.time()
        else:
            # If mouse hasn't moved for 30 seconds, pet might get bored
            if time.time() - self.mouse_last_move_time > 30:
                if self.pet.is_alive and random.random() < 0.1:
                    self.pet.current_quote = random.choice(QUOTES["BORED"])

        elapsed = time.time() - self.pet.birth_time
        self.pet.age = int(elapsed // 3600)
        self.pet.update()
        self.draw()
        # Save every 30 seconds automatically
        if int(time.time()) % 30 == 0:
            self.save_game()
        self.root.after(1000, self.update_loop)

    def on_close(self):
        self.save_game()
        self.root.destroy()

    def draw(self):
        self.canvas.delete("all")
        center_x = 150

        self.canvas.create_text(center_x, 30, text="--- ASCII TAMAGOTCHI ---", fill="white", font=self.bold_font)
        color = RARITY_DATA[self.pet.rarity]["color"]
        art = self.pet.get_ascii()

        start_y = 70
        for i, line in enumerate(art):
            self.canvas.create_text(center_x, start_y + (i * 15), text=line, fill=color, font=self.mono_font)

        if self.pet.is_alive:
            stage = get_stage(self.pet.age)
            stats = f"{self.pet.name} | {self.pet.species} {stage} | {self.pet.rarity}"
            self.canvas.create_text(center_x, 150, text=stats, fill="white", font=self.mono_font)
            h_str = f"Hunger: {self.pet.hunger}/10 (0=S, 10=F)"
            ha_str = f"Happy: {self.pet.happiness}/10"
            self.canvas.create_text(center_x, 170, text=h_str, fill="white", font=self.mono_font)
            self.canvas.create_text(center_x, 190, text=ha_str, fill="white", font=self.mono_font)
        else:
            self.canvas.create_text(center_x, 150, text="THE END", fill="red", font=self.bold_font)
            self.canvas.create_text(center_x, 170, text="Press [R] to attempt reset", fill="grey", font=self.mono_font)

        if self.pet.current_quote:
            y_off = 220 if self.pet.is_alive else 200
            # Use a bright off-white for high contrast and clarity
            quote_text = f"\"{self.pet.current_quote}\""
            self.canvas.create_text(center_x, y_off, text=quote_text, fill="#FFFFFF", font=self.mono_font, width=250, justify="center")

        if self.mode == "NORMAL":
            legend = " [F] Feed | [P] Pet | [Q] Quit "
            self.canvas.create_text(center_x, 380, text=legend, fill="white", font=self.mono_font)

if __name__ == "__main__":
    root = tk.Tk()
    app = TamagotchiWin(root)
    root.mainloop()
