import tkinter as tk
from tkinter import messagebox
import webbrowser
import time

# ---------------------- TELA DE BOAS-VINDAS ----------------------
class WelcomeScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Bem-vindo ao TypeFast Java")
        self.master.geometry("800x600")
        self.master.configure(bg="#1e1e1e")
        self.master.state("zoomed")

        title = tk.Label(master, text="TypeFast Java", font=("Consolas", 28, "bold"),
                         fg="#569CD6", bg="#1e1e1e")
        title.pack(pady=(30,10))

        welcome_msg = ("Bem-vindo ao TypeFast Java!\n"
                       "Desenvolvido por Mateus Veras\n"
                       "Aluno de Sistemas de Informação - UAST")
        welcome_label = tk.Label(master, text=welcome_msg, font=("Consolas", 14),
                                 fg="#d4d4d4", bg="#1e1e1e", justify="center")
        welcome_label.pack(pady=10)

        social_frame = tk.Frame(master, bg="#1e1e1e")
        social_frame.pack(pady=20)

        self.links = {
            "Instagram": "https://www.instagram.com/1mateusveras",
            "LinkedIn": "https://www.linkedin.com/in/mateuscandidoveras",
            "GitHub": "https://github.com/mateuscandidoveras/mateuscandidoveras"
        }

        for i, key in enumerate(self.links):
            btn = tk.Button(social_frame, text=key, bg="#1e1e1e", fg="#569CD6", bd=0,
                            font=("Consolas",12,"underline"),
                            command=lambda link=self.links[key]: webbrowser.open(link))
            btn.grid(row=0, column=i, padx=15)

        start_btn = tk.Button(master, text="Iniciar TypeFast", font=("Consolas", 16),
                              fg="#ffffff", bg="#007ACC", activebackground="#005A9E",
                              command=self.start_typefast)
        start_btn.pack(pady=40, ipadx=10, ipady=5)

    def start_typefast(self):
        input_dialog = CodeInputDialog(self.master)
        self.master.wait_window(input_dialog.top)

        codigo_usuario = input_dialog.result
        if codigo_usuario:
            editor_window = tk.Toplevel(self.master)
            editor_window.title("Mini-IDE TypeFast Java")
            editor_window.geometry("900x650")
            editor_window.state("zoomed")
            MiniIDETypeFast(editor_window, codigo_usuario)
            self.master.withdraw()

# ---------------------- JANELA PARA COLAR CÓDIGO ----------------------
class CodeInputDialog:
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.title("Cole o código Java")
        top.geometry("850x600")
        top.configure(bg="#1e1e1e")
        top.state("zoomed")

        instructions = tk.Label(
            top,
            text="Cole abaixo o bloco de código Java.\n"
                 "Use CTRL + e CTRL - para dar zoom.\n"
                 "Use as barras de rolagem para navegar.\n"
                 "Cole o código com a definição comentada para treinar também o conceito.",
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 11),
            justify="left"
        )
        instructions.pack(padx=10, pady=10, anchor="w")

        self.confirm_button = tk.Button(
            top,
            text="Confirmar e iniciar TypeFast",
            command=self.on_confirm,
            font=("Consolas", 12),
            bg="#0078D7",
            fg="white",
            relief="flat",
            height=2
        )
        self.confirm_button.pack(fill="x", padx=10, pady=(0, 10))

        text_frame = tk.Frame(top, bg="#1e1e1e")
        text_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.text_widget = tk.Text(
            text_frame,
            wrap="none",
            font=("Consolas", 14),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="white"
        )
        self.text_widget.pack(side="left", expand=True, fill="both")

        y_scroll = tk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        y_scroll.pack(side="right", fill="y")
        x_scroll = tk.Scrollbar(top, orient="horizontal", command=self.text_widget.xview)
        x_scroll.pack(fill="x")

        self.text_widget.config(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.result = None

    def on_confirm(self):
        self.result = self.text_widget.get("1.0", "end-1c")
        self.top.destroy()

# ---------------------- EDITOR TYPEFAST ----------------------
class MiniIDETypeFast:
    def __init__(self, master, codigo_java):
        self.master = master
        self.font_size = 14

        self.start_time = None
        self.running = False
        self.time_label = tk.Label(master, text="Tempo: 00:00", font=("Consolas", 12),
                                   bg="#1e1e1e", fg="#d4d4d4")
        self.time_label.pack(side="top", fill="x")

        frame = tk.Frame(master)
        frame.pack(expand=True, fill="both")

        self.v_scroll = tk.Scrollbar(frame, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll = tk.Scrollbar(frame, orient="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")

        self.text_widget = tk.Text(frame, font=("Consolas", self.font_size), wrap="none",
                                   bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                                   insertwidth=2,
                                   yscrollcommand=self.v_scroll.set,
                                   xscrollcommand=self.h_scroll.set)
        self.text_widget.pack(expand=True, fill="both")
        self.v_scroll.config(command=self.text_widget.yview)
        self.h_scroll.config(command=self.text_widget.xview)

        # Código sombra todo branco
        self.text_widget.insert("1.0", codigo_java)
        self.text_widget.tag_add("shadow", "1.0", "end")
        self.text_widget.tag_config("shadow", foreground="white")

        # Cursor e caracteres digitados
        self.cursor_tag = "cursor"
        self.text_widget.tag_config("typed", foreground="#007ACC")  # azul
        self.text_widget.tag_config("error", foreground="#f44747")

        self.text_chars = list(codigo_java.rstrip())
        self.pos = 0
        self.line_start = 0
        self.update_cursor()

        # Bindings
        self.text_widget.bind("<Key>", self.verificar_tecla)
        self.text_widget.bind("<Return>", self.enter_key)
        self.text_widget.bind("<Tab>", self.tab_key)
        self.text_widget.bind("<Up>", self.up_key)
        self.text_widget.bind("<Down>", self.down_key)
        self.text_widget.bind("<Left>", self.left_key)
        self.text_widget.bind("<Right>", self.right_key)
        self.text_widget.bind("<Control-plus>", self.zoom_in)
        self.text_widget.bind("<Control-minus>", self.zoom_out)
        self.text_widget.bind("<Control-equal>", self.zoom_in)
        self.text_widget.focus_set()

    # Cronômetro
    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.update_timer()

    def update_timer(self):
        if self.running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.time_label.config(text=f"Tempo: {minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.running = False

    # Cursor
    def update_cursor(self):
        self.text_widget.tag_remove(self.cursor_tag, "1.0", "end")
        self.text_widget.tag_add(self.cursor_tag, f"1.0 + {self.pos} chars")
        self.text_widget.mark_set("insert", f"1.0 + {self.pos} chars")

    # Highlight vazio (não altera nada)
    def highlight_syntax(self):
        pass

    # Digitação
    def verificar_tecla(self, event):
        if len(event.char) == 0:
            return "break"
        if not self.running:
            self.start_timer()
        if event.keysym == "BackSpace":
            if self.pos > self.line_start:
                self.pos -= 1
                self.text_widget.delete(f"1.0 + {self.pos} chars")
                self.text_widget.insert(f"1.0 + {self.pos} chars", self.text_chars[self.pos], "shadow")
                self.update_cursor()
            else:
                self.text_widget.bell()
            self.highlight_syntax()
            return "break"
        if self.pos >= len(self.text_chars):
            return "break"

        correto = self.text_chars[self.pos]
        if event.char == correto:
            self.text_widget.delete(f"1.0 + {self.pos} chars")
            self.text_widget.insert(f"1.0 + {self.pos} chars", event.char, "typed")
            self.pos += 1
            if self.pos == len(self.text_chars):
                self.end_time = time.time()
                total = self.end_time - self.start_time
                minutos = int(total // 60)
                segundos = int(total % 60)
                self.stop_timer()
                popup = tk.Toplevel(self.master)
                popup.title("Parabéns!")
                popup.configure(bg="#1e1e1e")
                popup.geometry("500x300")
                popup.resizable(False, False)
                popup.grab_set()
                title_label = tk.Label(popup, text="🎉 Parabéns! 🎉",
                                       font=("Consolas", 28, "bold"),
                                       fg="#569CD6", bg="#1e1e1e")
                title_label.pack(pady=(40, 10))
                time_label = tk.Label(popup, text=f"Você finalizou tudo em {minutos} min e {segundos} s!",
                                      font=("Consolas", 16), fg="#d4d4d4", bg="#1e1e1e")
                time_label.pack(pady=10)
                close_btn = tk.Button(popup, text="Fechar", font=("Consolas", 14, "bold"),
                                      bg="#007ACC", fg="white", activebackground="#005A9E",
                                      activeforeground="white", relief="flat", width=12,
                                      command=popup.destroy)
                close_btn.pack(pady=30)
                popup.update_idletasks()
                width = popup.winfo_width()
                height = popup.winfo_height()
                x = (popup.winfo_screenwidth() // 2) - (width // 2)
                y = (popup.winfo_screenheight() // 2) - (height // 2)
                popup.geometry(f"+{x}+{y}")
        else:
            self.text_widget.delete(f"1.0 + {self.pos} chars")
            self.text_widget.insert(f"1.0 + {self.pos} chars", correto, "error")
            self.text_widget.bell()
        self.update_cursor()
        self.highlight_syntax()
        return "break"

    # Enter, tab, setas
    def enter_key(self, event):
        if self.pos >= len(self.text_chars):
            return "break"
        if self.text_chars[self.pos] == "\n":
            self.pos += 1
            self.line_start = self.pos
            while self.pos < len(self.text_chars) and self.text_chars[self.pos] == " ":
                self.pos += 1
            self.line_start = self.pos
            self.update_cursor()
        else:
            self.text_widget.bell()
        self.highlight_syntax()
        return "break"

    def tab_key(self, event):
        for _ in range(4):
            self.verificar_tecla(type("Event", (object,), {"char": " ", "keysym": "space"}))
        return "break"

    def up_key(self, event):
        self.pos = max(0, self.pos - 50)
        self.update_cursor()
        return "break"

    def down_key(self, event):
        self.pos = min(len(self.text_chars)-1, self.pos + 50)
        self.update_cursor()
        return "break"

    def left_key(self, event):
        if self.pos > self.line_start:
            self.pos -= 1
            self.update_cursor()
        else:
            self.text_widget.bell()
        return "break"

    def right_key(self, event):
        if self.pos < len(self.text_chars):
            self.pos += 1
            self.update_cursor()
        else:
            self.text_widget.bell()
        return "break"

    # Zoom
    def zoom_in(self, event):
        self.font_size += 2
        self.text_widget.config(font=("Consolas", self.font_size))
        return "break"

    def zoom_out(self, event):
        if self.font_size > 6:
            self.font_size -= 2
            self.text_widget.config(font=("Consolas", self.font_size))
        return "break"

# ---------------------- EXECUÇÃO ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    WelcomeScreen(root)
    root.mainloop()
