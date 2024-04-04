from tkinter import*
from tkinter import messagebox
import subprocess

def menu(tempo):
    match tempo:
        case 0:
            tempo = (entry.get())
        case 1:
            tempo = str(3600)
        case 2:
            tempo = str(3600*2)
        case 3:
            tempo = str(3600*3)         
    msg = subprocess.run(f"shutdown /s /t {tempo}",shell=True, capture_output=True, text=True)
    if msg.returncode == 0:
        messagebox.showinfo(None,"Programado para desligar com sucesso!")
        updtlabel(int(tempo))
    else:    
        if tempo.isnumeric():
            messagebox.showerror("Erro", msg.stderr)
        else:
            messagebox.showerror("Erro", "Informe um tempo valido")    

def cancel():    
    msg = subprocess.run("shutdown /a", shell=True, capture_output=True, text=True)
    if msg.returncode == 0:
        messagebox.showinfo(None,"Programação para desligar cancelada")
        window.after_cancel(window.after_id)
        label2.configure(text="")
    else:    
        messagebox.showerror("Erro", msg.stderr)

def updtlabel(tempo):
        label2.configure(text=f"O computador desligara em: {tempo} segundos")
        if tempo > 0:
            tempo -= 1
            window.after_id = window.after(1000,updtlabel,tempo)
                

if __name__ == '__main__':
    window = Tk()
    window.after_id = None
    window.title("Sleep Timer")
    window.config(padx=10, pady=100)
    window.iconbitmap("SleepTimerIcon.ico")

    # Labels
    label = Label(text="Informe o tempo que deseja, ou digite o tempo em segundos: ")
    label.grid(row=0, column=1,pady=3)
    label2 = Label(text="")
    label2.grid(row=7, column=1,pady=3)

    # Entries
    entry = Entry(width=35)
    entry.grid(row=4, column=1, columnspan=1,pady=10)
    entry.focus()

    # Buttons
    add_button3 = Button(text="Uma hora", width=36, command=lambda: menu(1))
    add_button3.grid(row=1, column=1, columnspan=2, pady=3)
    add_button4 = Button(text="Duas horas", width=36, command=lambda: menu(2))
    add_button4.grid(row=2, column=1, columnspan=2, pady=3)
    add_button5 = Button(text="Tres horas", width=36, command=lambda: menu(3))
    add_button5.grid(row=3, column=1, columnspan=2, pady=3)
    add_button = Button(text="Definir tempo", width=36, command=lambda: menu(0))
    add_button.grid(row=5, column=1, columnspan=2)
    add_button2 = Button(text="Cancelar desligamento", width=36, command=cancel)
    add_button2.grid(row=6, column=1, columnspan=2, pady=15)
    
    window.mainloop()