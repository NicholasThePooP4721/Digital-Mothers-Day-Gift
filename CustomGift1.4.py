import tkinter as tk
import math
import random
import time

BG = "#0d0d1a"
ANIM_DURATION = 4000

LANG = {
    "de": {
        "window_title":    "Personalisierung",
        "app_title":       "Animiertes Glueckwunsch-Programm",
        "app_subtitle":    "Personalisiere dein Erlebnis",
        "label_anlass":    "Anlass:",
        "label_haupttext": "Haupttext (wird animiert):",
        "label_von":       "Abschlusstext (z.B. 'von Julia'):",
        "label_titel":     "Titel im Finale:",
        "btn_start":       "  Start!  ",
        "esc_hint":        "ESC zum Beenden",
        "vorlagen": {
            "Muttertag":   {"text": "Frohen Muttertag!",            "finale": "Alles Liebe, Mama!",          "farbe": "#ff79c6"},
            "Vatertag":    {"text": "Frohen Vatertag!",             "finale": "Du bist der beste Papa!",     "farbe": "#8be9fd"},
            "Geburtstag":  {"text": "Alles Gute zum Geburtstag!",   "finale": "Happy Birthday!",             "farbe": "#f1fa8c"},
            "Weihnachten": {"text": "Frohe Weihnachten!",           "finale": "Frohes Fest!",                "farbe": "#50fa7b"},
            "Eigener Text":{"text": "",                             "finale": "",                            "farbe": "#bd93f9"},
        },
        "default_von":     "von deinem Kind  <3",
        "finale_esc":      "(ESC zum Beenden)",
        "anim_names": ["Schreibmaschine","Wellen","Einflug","Regenbogen","Enthuellung","Matrix"],
    },
    "en": {
        "window_title":    "Personalization",
        "app_title":       "Animated Greeting Program",
        "app_subtitle":    "Personalize your experience",
        "label_anlass":    "Occasion:",
        "label_haupttext": "Main text (will be animated):",
        "label_von":       "Closing text (e.g. 'from Julia'):",
        "label_titel":     "Finale title:",
        "btn_start":       "  Start!  ",
        "esc_hint":        "Press ESC to quit",
        "vorlagen": {
            "Mother's Day":  {"text": "Happy Mother's Day!",         "finale": "Love you, Mom!",              "farbe": "#ff79c6"},
            "Father's Day":  {"text": "Happy Father's Day!",         "finale": "Best Dad ever!",              "farbe": "#8be9fd"},
            "Birthday":      {"text": "Happy Birthday!",             "finale": "Have an amazing day!",        "farbe": "#f1fa8c"},
            "Christmas":     {"text": "Merry Christmas!",            "finale": "Season's Greetings!",         "farbe": "#50fa7b"},
            "Custom":        {"text": "",                            "finale": "",                            "farbe": "#bd93f9"},
        },
        "default_von":     "from your child  <3",
        "finale_esc":      "(Press ESC to quit)",
        "anim_names": ["Typewriter","Waves","Slide In","Rainbow","Reveal","Matrix"],
    },
}


# ─── Setup-Fenster ────────────────────────────────────────────────────────────

class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.result = None
        self.current_lang = "de"

        self.root.title("Language / Sprache")
        self.root.geometry("520x540")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        self._build_language_bar()
        self.content_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self._build_content()

    # ── Sprach-Leiste oben ────────────────────────────────────

    def _build_language_bar(self):
        bar = tk.Frame(self.root, bg="#12122a", pady=6)
        bar.pack(fill=tk.X)
        tk.Label(bar, text="🌐", bg="#12122a", fg="#aaa",
            font=("Consolas", 11)).pack(side=tk.LEFT, padx=(12,4))
        self.lang_var = tk.StringVar(value="de")
        for code, label in [("de", "Deutsch"), ("en", "English")]:
            tk.Radiobutton(bar, text=label, variable=self.lang_var, value=code,
                bg="#12122a", fg="#ccc", selectcolor="#0d0d1a",
                activebackground="#12122a", activeforeground="#fff",
                font=("Consolas", 10),
                command=self._on_lang_change
            ).pack(side=tk.LEFT, padx=6)

    def _on_lang_change(self):
        self.current_lang = self.lang_var.get()
        # remember current field values
        saved_text  = self.text_var.get()
        saved_von   = self.von_var.get()
        saved_titel = self.titel_var.get()
        for w in self.content_frame.winfo_children():
            w.destroy()
        self._build_content()
        # restore if user had typed something custom
        self.text_var.set(saved_text)
        self.von_var.set(saved_von)
        self.titel_var.set(saved_titel)

    # ── Haupt-Inhalt ──────────────────────────────────────────

    def _build_content(self):
        L = LANG[self.current_lang]
        pad = {"padx": 18, "pady": 5}
        f = self.content_frame

        tk.Label(f, text=L["app_title"],
            bg="#1a1a2e", fg="#bd93f9",
            font=("Consolas", 13, "bold")).pack(pady=(18, 2))
        tk.Label(f, text=L["app_subtitle"],
            bg="#1a1a2e", fg="#555577",
            font=("Consolas", 10)).pack(pady=(0, 14))

        # Anlass / Occasion
        tk.Label(f, text=L["label_anlass"],
            bg="#1a1a2e", fg="#ccc", font=("Consolas", 11)).pack(anchor="w", **pad)

        vorlagen = L["vorlagen"]
        first_key = list(vorlagen.keys())[0]
        self.vorlage_var = tk.StringVar(value=first_key)

        radio_frame = tk.Frame(f, bg="#1a1a2e")
        radio_frame.pack(anchor="w", padx=18, pady=2)
        for name in vorlagen:
            tk.Radiobutton(radio_frame, text=name, variable=self.vorlage_var,
                value=name, bg="#1a1a2e", fg="#ccc", selectcolor="#0d0d1a",
                activebackground="#1a1a2e", activeforeground="#fff",
                font=("Consolas", 10),
                command=self._on_vorlage_change
            ).pack(anchor="w")

        # Haupttext
        tk.Label(f, text=L["label_haupttext"],
            bg="#1a1a2e", fg="#ccc", font=("Consolas", 11)).pack(anchor="w", **pad)
        self.text_var = tk.StringVar(value=vorlagen[first_key]["text"])
        tk.Entry(f, textvariable=self.text_var,
            bg="#0d0d1a", fg="#ff79c6", insertbackground="#ff79c6",
            font=("Consolas", 12), relief="flat", width=40
        ).pack(anchor="w", padx=18, pady=2, ipady=5)

        # Von-Text
        tk.Label(f, text=L["label_von"],
            bg="#1a1a2e", fg="#ccc", font=("Consolas", 11)).pack(anchor="w", **pad)
        self.von_var = tk.StringVar(value=L["default_von"])
        tk.Entry(f, textvariable=self.von_var,
            bg="#0d0d1a", fg="#bd93f9", insertbackground="#bd93f9",
            font=("Consolas", 12), relief="flat", width=40
        ).pack(anchor="w", padx=18, pady=2, ipady=5)

        # Finale-Titel
        tk.Label(f, text=L["label_titel"],
            bg="#1a1a2e", fg="#ccc", font=("Consolas", 11)).pack(anchor="w", **pad)
        self.titel_var = tk.StringVar(value=vorlagen[first_key]["finale"])
        tk.Entry(f, textvariable=self.titel_var,
            bg="#0d0d1a", fg="#f1fa8c", insertbackground="#f1fa8c",
            font=("Consolas", 12), relief="flat", width=40
        ).pack(anchor="w", padx=18, pady=2, ipady=5)

        # Start
        tk.Button(f, text=L["btn_start"],
            bg="#bd93f9", fg="#0d0d1a",
            font=("Consolas", 13, "bold"),
            relief="flat", cursor="hand2",
            command=self._start
        ).pack(pady=18)

    def _on_vorlage_change(self):
        L = LANG[self.current_lang]
        v = L["vorlagen"][self.vorlage_var.get()]
        if v["text"]:
            self.text_var.set(v["text"])
        self.titel_var.set(v["finale"])

    def _start(self):
        L = LANG[self.current_lang]
        haupttext = self.text_var.get().strip()  or "Hello!"
        von_text  = self.von_var.get().strip()   or L["default_von"]
        titel     = self.titel_var.get().strip() or haupttext
        farbe     = L["vorlagen"][self.vorlage_var.get()]["farbe"]
        anim_names = L["anim_names"]
        esc_hint   = L["esc_hint"]
        finale_esc = L["finale_esc"]
        self.result = (haupttext, von_text, titel, farbe, anim_names, esc_hint, finale_esc)
        self.root.destroy()


# ─── Animations-Fenster ───────────────────────────────────────────────────────

class AnimApp:
    def __init__(self, root, haupttext, von_text, titel, accent, anim_names, esc_hint, finale_esc):
        self.root    = root
        self.TEXT    = haupttext
        self.VON     = von_text
        self.TITEL   = titel
        self.ACCENT  = accent
        self.ESC     = esc_hint
        self.FIN_ESC = finale_esc

        self.root.title("Greeting!")
        self.root.configure(bg=BG)
        self.root.geometry("820x420")
        self.root.resizable(True, True)

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.after_ids  = []
        self.anim_index = 0
        self.running    = True

        self.animations = [
            (anim_names[0], self.anim_typewriter),
            (anim_names[1], self.anim_wave),
            (anim_names[2], self.anim_slide_in),
            (anim_names[3], self.anim_rainbow),
            (anim_names[4], self.anim_center_reveal),
            (anim_names[5], self.anim_matrix),
        ]

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.schedule(300, self.next_animation)

    def W(self): return self.canvas.winfo_width() or 820
    def H(self): return self.canvas.winfo_height() or 420

    def clear(self):
        self.canvas.delete("all")
        for aid in self.after_ids:
            self.root.after_cancel(aid)
        self.after_ids = []

    def schedule(self, delay, func):
        aid = self.root.after(delay, func)
        self.after_ids.append(aid)

    def draw_label(self, name):
        self.canvas.create_text(self.W()//2, 26, text=f"~ {name} ~",
            fill="#555577", font=("Consolas", 12))
        self.canvas.create_text(self.W()-8, self.H()-8,
            text=self.ESC, fill="#333355",
            font=("Consolas", 9), anchor="se")

    def next_animation(self):
        if not self.running: return
        self.clear()
        if self.anim_index >= len(self.animations):
            self.show_finale()
            return
        name, func = self.animations[self.anim_index]
        func(name)
        self.anim_index += 1
        self.schedule(ANIM_DURATION + 600, self.next_animation)

    # ── Animationen ───────────────────────────────────────────

    def anim_typewriter(self, name):
        self.draw_label(name)
        cy = self.H()//2
        item   = self.canvas.create_text(self.W()//2, cy, text="",
            fill=self.ACCENT, font=("Consolas", 30, "bold"), anchor="center")
        cursor = self.canvas.create_text(self.W()//2, cy, text="|",
            fill=self.ACCENT, font=("Consolas", 30, "bold"), anchor="w")

        def tick(i=0):
            if i > len(self.TEXT): return
            self.canvas.itemconfig(item, text=self.TEXT[:i])
            bb = self.canvas.bbox(item)
            cx = bb[2] if bb else self.W()//2
            self.canvas.coords(cursor, cx, cy)
            self.canvas.itemconfig(cursor, text="|" if i%2==0 else " ")
            self.schedule(85, lambda: tick(i+1))
        tick()

    def anim_wave(self, name):
        self.draw_label(name)
        letters = [self.canvas.create_text(0, 0, text=ch,
            fill=self.ACCENT, font=("Consolas", 28, "bold"))
            for ch in self.TEXT]
        start = time.time()

        def tick():
            if not self.running: return
            t = time.time()-start
            cx, cy = self.W()//2, self.H()//2
            tw = len(self.TEXT)*21
            for i, it in enumerate(letters):
                x = cx - tw//2 + i*21 + 10
                y = cy + math.sin(t*3 + i*0.5)*28
                self.canvas.coords(it, x, y)
            if t < ANIM_DURATION/1000:
                self.schedule(30, tick)
        tick()

    def anim_slide_in(self, name):
        self.draw_label(name)
        item = self.canvas.create_text(-500, self.H()//2,
            text=self.TEXT, fill=self.ACCENT,
            font=("Consolas", 28, "bold"), anchor="center")
        target = self.W()//2
        start  = time.time()

        def tick():
            t = (time.time()-start)*1000
            p = min(t/900, 1.0)
            ease = 1-(1-p)**3
            self.canvas.coords(item, -500+(target+500)*ease, self.H()//2)
            if p < 1.0: self.schedule(16, tick)
        tick()

    def anim_rainbow(self, name):
        self.draw_label(name)
        colors = ["#ff5555","#ffb86c","#f1fa8c","#50fa7b","#8be9fd","#bd93f9","#ff79c6"]
        cx, cy = self.W()//2, self.H()//2
        tw = len(self.TEXT)*21
        letters = []
        for i, ch in enumerate(self.TEXT):
            x = cx - tw//2 + i*21 + 10
            it = self.canvas.create_text(x, cy, text=ch,
                fill=colors[i%len(colors)], font=("Consolas", 28, "bold"))
            letters.append(it)
        offset = [0]
        start = time.time()

        def tick():
            if time.time()-start > ANIM_DURATION/1000: return
            for i, it in enumerate(letters):
                self.canvas.itemconfig(it, fill=colors[(i+offset[0])%len(colors)])
            offset[0] += 1
            self.schedule(100, tick)
        tick()

    def anim_center_reveal(self, name):
        self.draw_label(name)
        cx, cy = self.W()//2, self.H()//2
        tw = len(self.TEXT)*21
        letters = []
        for i, ch in enumerate(self.TEXT):
            x = cx - tw//2 + i*21 + 10
            it = self.canvas.create_text(x, cy, text=".",
                fill="#444466", font=("Consolas", 28, "bold"))
            letters.append(it)
        mid = len(self.TEXT)//2
        order = []
        for i in range(mid+1):
            if mid-i >= 0: order.append(mid-i)
            if mid+i < len(self.TEXT) and i != 0: order.append(mid+i)

        def reveal(step=0):
            if step >= len(order): return
            idx = order[step]
            self.canvas.itemconfig(letters[idx], text=self.TEXT[idx], fill=self.ACCENT)
            self.schedule(55, lambda: reveal(step+1))
        reveal()

    def anim_matrix(self, name):
        self.draw_label(name)
        W, H   = self.W(), self.H()
        cols   = list(range(0, W, 18))
        drops  = {c: random.randint(0, H//14) for c in cols}
        mchars = list("01#@%!ABCXYZ")
        start  = time.time()

        def tick():
            if not self.running: return
            t = time.time()-start
            self.canvas.delete("mc")
            for col in cols:
                y = drops[col]*14
                if y < H:
                    self.canvas.create_text(col, y,
                        text=random.choice(mchars),
                        fill=random.choice(["#00ff41","#00cc33","#009922"]),
                        font=("Consolas", 12, "bold"), tags="mc")
                drops[col] = (drops[col]+1) % (H//14+5)
            if t > 2.3:
                self.canvas.delete("mc")
                self.canvas.create_text(W//2, H//2,
                    text=self.TEXT, fill="#00ff41",
                    font=("Consolas", 30, "bold"), tags="mc")
                return
            self.schedule(55, tick)
        tick()

    # ── Finale ────────────────────────────────────────────────

    def show_finale(self):
        self.clear()
        cx, cy = self.W()//2, self.H()//2
        self.canvas.create_text(cx, cy-45, text=self.TITEL,
            fill=self.ACCENT, font=("Consolas", 24, "bold"))
        self.canvas.create_text(cx, cy+8, text=self.VON,
            fill="#bd93f9", font=("Consolas", 20, "bold"))
        self.canvas.create_text(cx, cy+55, text=self.FIN_ESC,
            fill="#555577", font=("Consolas", 11))
        colors = ["#ff5555","#ff79c6","#ffb86c","#f1fa8c","#bd93f9","#8be9fd"]
        for _ in range(40):
            x = random.randint(40, self.W()-40)
            y = random.randint(15, self.H()-15)
            self.canvas.create_text(x, y, text="<3",
                fill=random.choice(colors),
                font=("Consolas", random.randint(9, 18)))


# ─── Start ────────────────────────────────────────────────────────────────────

def main():
    setup_root = tk.Tk()
    app = SetupWindow(setup_root)
    setup_root.mainloop()

    if app.result is None:
        return

    haupttext, von_text, titel, farbe, anim_names, esc_hint, finale_esc = app.result

    anim_root = tk.Tk()
    AnimApp(anim_root, haupttext, von_text, titel, farbe, anim_names, esc_hint, finale_esc)
    anim_root.mainloop()


if __name__ == "__main__":
    main()
