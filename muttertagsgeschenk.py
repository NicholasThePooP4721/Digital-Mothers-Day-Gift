import tkinter as tk
import math
import random
import time

TEXT = "Frohen Muttertag Mama!"
BG = "#0d0d1a"
ANIM_DURATION = 4000


class MuttertagApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Frohen Muttertag!")
        self.root.configure(bg=BG)
        self.root.geometry("800x400")
        self.root.resizable(True, True)

        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.after_ids = []
        self.anim_index = 0
        self.running = True

        self.animations = [
            self.anim_typewriter,
            self.anim_wave,
            self.anim_slide_in,
            self.anim_rainbow,
            self.anim_center_reveal,
            self.anim_matrix,
        ]
        self.names = [
            "Schreibmaschine",
            "Wellen",
            "Einflug",
            "Regenbogen",
            "Enthuellung",
            "Matrix",
        ]

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.schedule(300, self.next_animation)

    def W(self):
        return self.canvas.winfo_width() or 800

    def H(self):
        return self.canvas.winfo_height() or 400

    def clear(self):
        self.canvas.delete("all")
        for aid in self.after_ids:
            self.root.after_cancel(aid)
        self.after_ids = []

    def draw_label(self, name):
        self.canvas.create_text(self.W()//2, 28, text=name,
            fill="#555577", font=("Consolas", 13))
        self.canvas.create_text(self.W()-10, self.H()-10,
            text="ESC zum Beenden", fill="#333355",
            font=("Consolas", 10), anchor="se")

    def schedule(self, delay, func):
        aid = self.root.after(delay, func)
        self.after_ids.append(aid)

    def next_animation(self):
        if not self.running:
            return
        self.clear()
        if self.anim_index >= len(self.animations):
            self.show_finale()
            return
        self.animations[self.anim_index]()
        self.anim_index += 1
        self.schedule(ANIM_DURATION + 600, self.next_animation)

    # 1 - Schreibmaschine
    def anim_typewriter(self):
        self.draw_label("~ Schreibmaschine ~")
        item = self.canvas.create_text(self.W()//2, self.H()//2,
            text="", fill="#ff79c6", font=("Consolas", 32, "bold"), anchor="center")
        cursor = self.canvas.create_text(self.W()//2, self.H()//2,
            text="|", fill="#ff79c6", font=("Consolas", 32, "bold"), anchor="w")

        def tick(i=0):
            if i > len(TEXT):
                return
            self.canvas.itemconfig(item, text=TEXT[:i])
            bb = self.canvas.bbox(item)
            cx = bb[2] if bb else self.W()//2
            self.canvas.coords(cursor, cx, self.H()//2)
            self.canvas.itemconfig(cursor, text="|" if i % 2 == 0 else " ")
            self.schedule(80, lambda: tick(i+1))
        tick()

    # 2 - Wellen
    def anim_wave(self):
        self.draw_label("~ Wellen ~")
        letters = []
        for ch in TEXT:
            item = self.canvas.create_text(0, 0, text=ch,
                fill="#8be9fd", font=("Consolas", 30, "bold"))
            letters.append(item)
        start = time.time()

        def tick():
            if not self.running:
                return
            t = time.time() - start
            cx, cy = self.W()//2, self.H()//2
            tw = len(TEXT) * 22
            for i, it in enumerate(letters):
                x = cx - tw//2 + i*22 + 11
                y = cy + math.sin(t*3 + i*0.5) * 30
                self.canvas.coords(it, x, y)
            if t < ANIM_DURATION/1000:
                self.schedule(30, tick)
        tick()

    # 3 - Einflug
    def anim_slide_in(self):
        self.draw_label("~ Einflug ~")
        item = self.canvas.create_text(-400, self.H()//2,
            text=TEXT, fill="#50fa7b",
            font=("Consolas", 30, "bold"), anchor="center")
        target = self.W()//2
        start = time.time()

        def tick():
            t = (time.time()-start)*1000
            p = min(t/800, 1.0)
            ease = 1-(1-p)**3
            self.canvas.coords(item, -400+(target+400)*ease, self.H()//2)
            if p < 1.0:
                self.schedule(16, tick)
        tick()

    # 4 - Regenbogen
    def anim_rainbow(self):
        self.draw_label("~ Regenbogen ~")
        colors = ["#ff5555","#ffb86c","#f1fa8c","#50fa7b","#8be9fd","#bd93f9","#ff79c6"]
        cx, cy = self.W()//2, self.H()//2
        tw = len(TEXT)*21
        letters = []
        for i, ch in enumerate(TEXT):
            x = cx - tw//2 + i*21 + 10
            it = self.canvas.create_text(x, cy, text=ch,
                fill=colors[i % len(colors)], font=("Consolas", 30, "bold"))
            letters.append(it)
        offset = [0]
        start = time.time()

        def tick():
            if time.time()-start > ANIM_DURATION/1000:
                return
            for i, it in enumerate(letters):
                self.canvas.itemconfig(it, fill=colors[(i+offset[0]) % len(colors)])
            offset[0] += 1
            self.schedule(100, tick)
        tick()

    # 5 - Enthuellung von Mitte
    def anim_center_reveal(self):
        self.draw_label("~ Enthuellung ~")
        cx, cy = self.W()//2, self.H()//2
        tw = len(TEXT)*21
        letters = []
        for i, ch in enumerate(TEXT):
            x = cx - tw//2 + i*21 + 10
            it = self.canvas.create_text(x, cy, text=".",
                fill="#444466", font=("Consolas", 30, "bold"))
            letters.append(it)
        mid = len(TEXT)//2
        order = []
        for i in range(mid+1):
            if mid-i >= 0:
                order.append(mid-i)
            if mid+i < len(TEXT) and i != 0:
                order.append(mid+i)

        def reveal(step=0):
            if step >= len(order):
                return
            idx = order[step]
            self.canvas.itemconfig(letters[idx], text=TEXT[idx], fill="#bd93f9")
            self.schedule(60, lambda: reveal(step+1))
        reveal()

    # 6 - Matrix
    def anim_matrix(self):
        self.draw_label("~ Matrix ~")
        W, H = self.W(), self.H()
        cols = list(range(0, W, 18))
        drops = {c: random.randint(0, H//14) for c in cols}
        mchars = list("01#@%!ABCXYZ")
        start = time.time()

        def tick():
            if not self.running:
                return
            t = time.time()-start
            self.canvas.delete("mc")
            for col in cols:
                y = drops[col]*14
                if y < H:
                    self.canvas.create_text(col, y,
                        text=random.choice(mchars),
                        fill=random.choice(["#00ff41","#00cc33","#009922"]),
                        font=("Consolas", 13, "bold"), tags="mc")
                drops[col] = (drops[col]+1) % (H//14+5)
            if t > 2.2:
                self.canvas.delete("mc")
                self.canvas.create_text(W//2, H//2,
                    text=TEXT, fill="#00ff41",
                    font=("Consolas", 32, "bold"), tags="mc")
                return
            self.schedule(55, tick)
        tick()

    # Finale
    def show_finale(self):
        self.clear()
        cx, cy = self.W()//2, self.H()//2
        self.canvas.create_text(cx, cy-40, text="Alles Liebe,",
            fill="#ff79c6", font=("Consolas", 26, "bold"))
        self.canvas.create_text(cx, cy+10, text="von Nicholas  <3",
            fill="#bd93f9", font=("Consolas", 22, "bold"))
        self.canvas.create_text(cx, cy+60, text="(ESC zum Beenden)",
            fill="#555577", font=("Consolas", 12))
        colors = ["#ff5555","#ff79c6","#ffb86c","#f1fa8c","#bd93f9"]
        for _ in range(35):
            x = random.randint(50, self.W()-50)
            y = random.randint(20, self.H()-20)
            self.canvas.create_text(x, y, text="<3",
                fill=random.choice(colors),
                font=("Consolas", random.randint(10, 18)))


root = tk.Tk()
app = MuttertagApp(root)
root.mainloop()
