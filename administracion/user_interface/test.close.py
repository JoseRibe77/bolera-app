import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.mainloop()

    def _on_closing(self, event=None):
        print("Cerrando...")
        self.quit()

if __name__ == "__main__":
    MainWindow()