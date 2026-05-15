import curses
import random
import time

# --- Configuration & Data ---
RARITY_DATA = {
    "Common": {"color_id": 1, "weight": 60},
    "Uncommon": {"color_id": 2, "weight": 25},
    "Rare": {"color_id": 3, "weight": 10},
    "Epic": {"color_id": 4, "weight": 5},
}

SPECIES_DATA = {
    "Blob": {
        "art": {
            "Baby": ["  ( )  ", "  ( o ) "],
            "Teen": ["  (   )  ", "  ( O O ) "],
            "Adult": [" (       ) ", " (  O   O  ) ", "  (_______)  "]
        }
    },
    "Cat": {
        "art": {
            "Baby": ["  ^..^  ", "   (oo)  "],
            "Teen": ["  (=^.^=) ", "   (  u  ) "],
            "Adult": ["  (=;^;=)  ", "  /  V  \\  ", "  |_|  |_|  "]
        }
    },
    "Dragon": {
        "art": {
            "Baby": ["   ~<  ", "   ( )  "],
            "Teen": ["  ~< * > ", "   (oo)  "],
            "Adult": ["  ~< * V * > ", "   / \\ / \\   ", "  /   V   \\  "]
        }
    },
    "Robot": {
        "art": {
            "Baby": ["  [ . ] ", "  [___]  "],
            "Teen": ["  [o-o]  ", "  |___|  "],
            "Adult": ["  [ O-O ]  ", "  /|___|\\ ", "  |_|   |_| "]
        }
    },
    "Slime": {
        "art": {
            "Baby": ["  ~_~  ", "  ( )   "],
            "Teen": ["  ~_0_~ ", "  ( o )  "],
            "Adult": ["  ~_00_~ ", " (  O O  ) ", "  `~~~~~`  "]
        }
    }
}

NAMES = ["Sprocket", "Bimble", "Glitch", "Mochi", "Zorp", "Noodle", "Pebble", "Void", "Slinky", "Tofu"]
QUOTES = [
    "I can taste the pixels.",
    "Is it just me or is the terminal getting smaller?",
    "I'm thinking of a number between 1 and infinity.",
    "Feed me or I'll start eating the source code.",
    "I've evolved! Now I can... wait, what can I do?",
    "Your keyboard smells like coffee.",
    "I'm not lazy, I'm just in power-saving mode.",
    "Why are we in a terminal? I want a GUI!",
    "I've seen the void, and it looks like a segmentation fault.",
    " petting me is the only thing keeping me sane."
]

def get_stage(age):
    if age < 3: return "Baby"
    if age < 6: return "Teen"
    return "Adult"

class Creature:
    def __init__(self, name, species, rarity):
        self.name = name
        self.species = species
        self.rarity = rarity
        # 0 = Starving, 10 = Full
        self.hunger = random.randint(7, 10)
        self.happiness = random.randint(5, 10)
        self.age = 0
        self.is_alive = True
        self.last_update = time.time()
        self.current_quote = ""

        # Timers for decay
        self.hunger_timer = 0
        self.happiness_timer = random.randint(300, 1200) # Initial random mood drop

    def update(self):
        if not self.is_alive:
            return

        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # Update Age (every 10 real minutes = 1 game age increment)
        # To make it feel like it evolves, we'll use a simpler tick
        # but only increment age occasionally.
        # Actually, let's just keep it based on dt for everything.

        # Hunger Decay Logic
        stage = get_stage(self.age)
        hunger_rate = 1800 if stage == "Baby" else 3600 # seconds per 1 point
        self.hunger_timer += dt
        if self.hunger_timer >= hunger_rate:
            self.hunger = max(0, self.hunger - 1)
            self.hunger_timer = 0
            if self.hunger == 0:
                self.is_alive = False
                self.current_quote = "..."

        # Happiness Decay Logic
        happy_rate_min = 300 if stage == "Baby" else 1200
        happy_rate_max = 1200 if stage == "Baby" else 3600

        self.happiness_timer -= dt
        if self.happiness_timer <= 0:
            self.happiness = max(0, self.happiness - 1)
            if self.happiness == 0:
                self.is_alive = False
                self.current_quote = "..."

            # Schedule next random drop
            self.happiness_timer = random.randint(happy_rate_min, happy_rate_max)

        # Age Increment (Every 1 hour of real time)
        # Using a simple approach: if we've lived 3600s since last age inc
        # (Would need a separate timer, let's just use the total lifetime)
        # For now, let's just laisibly increase age every few mins for demo
        # so user sees evolution.
        # REAL logic:
        # if now - self.birth_time >= (self.age + 1) * 3600: self.age += 1
        # To keep it simple, we'll just track total seconds lived.

        # Random quote
        if self.is_alive and random.random() < 0.001: # Very rare check per update (1Hz)
            self.current_quote = random.choice(QUOTES)

    def feed(self):
        if not self.is_alive: return
        self.hunger = min(10, self.hunger + 3)
        self.current_quote = "Mmm, binary delicious!"

    def pet(self):
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

class TamagotchiApp:
    def __init__(self):
        self.pet = self.create_random_pet()
        self.running = True
        self.mode = "NORMAL" # "NORMAL" or "INPUT"
        self.input_buffer = ""
        self.start_time = time.time()

    def create_random_pet(self):
        species = random.choice(list(SPECIES_DATA.keys()))
        name = random.choice(NAMES) + str(random.randint(1, 99))

        rarities = list(RARITY_DATA.keys())
        weights = [RARITY_DATA[r]["weight"] for r in rarities]
        rarity = random.choices(rarities, weights=weights, k=1)[0]

        pet = Creature(name, species, rarity)
        # Add a birth_time to track age in real-time
        pet.birth_time = time.time()
        return pet

    def run(self, stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1) # Common
        curses.init_pair(2, curses.COLOR_BLUE, -1)  # Uncommon
        curses.init_pair(3, curses.COLOR_MAGENTA, -1) # Rare
        curses.init_pair(4, curses.COLOR_YELLOW, -1) # Epic

        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(1000)

        while self.running:
            stdscr.clear()

            # Track real-time age
            elapsed = time.time() - self.pet.birth_time
            self.pet.age = elapsed // 3600 # 1 year = 1 hour of real time

            self.pet.update()
            self.render_ui(stdscr)

            try:
                key = stdscr.getch()
                if key == ord('q'):
                    self.running = False

                if self.mode == "NORMAL":
                    if key == ord('f'):
                        self.pet.feed()
                    elif key == ord('p'):
                        self.pet.pet()
                    elif key == ord('r') and not self.pet.is_alive:
                        self.mode = "INPUT"
                        self.input_buffer = ""

                elif self.mode == "INPUT":
                    if key == 10 or key == 13: # Enter
                        if self.input_buffer.strip().lower() == self.pet.name.lower():
                            self.pet = self.create_random_pet()
                            self.mode = "NORMAL"
                        else:
                            self.mode = "NORMAL"
                    elif key == 27: # Esc
                        self.mode = "NORMAL"
                    elif 32 <= key <= 126:
                        self.input_buffer += chr(key)
                    elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                        self.input_buffer = self.input_buffer[:-1]

            except Exception:
                pass

            stdscr.refresh()

    def render_ui(self, stdscr):
        h, w = stdscr.getmaxyx()

        center_x = w // 2
        center_y = h // 2

        # Title (Slightly higher)
        stdscr.addstr(center_y - 8, center_x - 10, "--- ASCII TAMAGOTCHI ---", curses.A_BOLD)

        # Pet Info
        color = curses.color_pair(RARITY_DATA[self.pet.rarity]["color_id"])

        # Render Pet
        art = self.pet.get_ascii()
        for line_idx, line in enumerate(art):
            # Use bounds checking to prevent crash in very small windows
            try:
                stdscr.addstr(center_y - 3 + line_idx, center_x - (len(line) // 2), line, color)
            except curses.error:
                pass

        # Stats
        if self.pet.is_alive:
            stage = get_stage(self.pet.age)
            stats = f"{self.pet.name} | {self.pet.species} {stage} | {self.pet.rarity}"
            try:
                stdscr.addstr(center_y + 3, center_x - (len(stats) // 2), stats)
                hunger_str = f"Hunger (0=S, 10=F): {self.pet.hunger}/10"
                happy_str = f"Happy (0=S, 10=F): {self.pet.happiness}/10"
                stdscr.addstr(center_y + 4, center_x - (len(hunger_str) // 2), hunger_str)
                stdscr.addstr(center_y + 5, center_x - (len(happy_str) // 2), happy_str)
            except curses.error:
                pass
        else:
            try:
                stdscr.addstr(center_y + 3, center_x - 5, "THE END", curses.A_BOLD)
                stdscr.addstr(center_y + 4, center_x - 12, "Press [R] to attempt reset", curses.A_DIM)
            except curses.error:
                pass

        # Quote
        if self.pet.current_quote:
            try:
                stdscr.addstr(center_y + 7, center_x - 15, f"\"{self.pet.current_quote}\"", curses.A_DIM)
            except curses.error:
                pass

        # Input Prompt
        if self.mode == "INPUT":
            prompt = f"Enter pet name to reset: {self.input_buffer}_"
            try:
                stdscr.addstr(h - 5, center_x - (len(prompt) // 2), prompt, curses.A_BOLD | curses.A_REVERSE)
                stdscr.addstr(h - 6, center_x - 15, "Type name exactly then hit Enter", curses.A_DIM)
            except curses.error:
                pass

        # Footer
        if self.mode == "NORMAL":
            legend = " [F] Feed | [P] Pet | [Q] Quit "
            try:
                stdscr.addstr(h - 2, center_x - (len(legend) // 2), legend, curses.A_REVERSE)
            except curses.error:
                pass

if __name__ == "__main__":
    app = TamagotchiApp()
    curses.wrapper(app.run)
