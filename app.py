from tkinter import *
import ctypes
import api

def export():
    w = int(length.get())
    total_weight = int(weight.get())

    possible_cuts = []

    if s145.get() == 1:
        possible_cuts.append(145)
    if s165.get() == 1:
        possible_cuts.append(165)
    if s185.get() == 1:
        possible_cuts.append(185)
    if s250.get() == 1:
        possible_cuts.append(250)
    if s280.get() == 1:
        possible_cuts.append(280)

    api.main(w, total_weight, possible_cuts, int(sol_num.get()))

    print("\nExport to csv successfully completed\n")


ctypes.windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.title("GUI")
root.minsize(500, 500)  # width, height
root.maxsize(500, 500)  # width x height
root.config(bg="lightgrey")
root.call('tk', 'scaling', 1.9)


# Enter specific information for your profile into the following widgets
enter_info = Label(root, text="Εισάγετε τις παρακάτω πληροφορίες: ", bg="lightgrey")
enter_info.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

# Length and Weight labels and entry widgets
Label(root, text="Πλάτος", bg="lightgrey").grid(row=1, column=1, padx=5, pady=5, sticky=E)
Label(root, text="millimeters", bg="lightgrey").grid(row=1, column=3, sticky=W)

length = Entry(root, bd=3)
length.grid(row=1, column=2, padx=5, pady=5)

Label(root, text="Βάρος", bg="lightgrey").grid(row=2, column=1, padx=5, pady=5, sticky=E)
Label(root, text="kg", bg="lightgrey").grid(row=2, column=3, sticky=W)

weight = Entry(root, bd=3)
weight.grid(row=2, column=2, padx=5, pady=5)

Label(root, text="Επιθυμητές λύσεις", bg="lightgrey").grid(row=3, column=1, padx=5, pady=5, sticky=E)

sol_num = Entry(root, bd=3)
sol_num.insert(0, 100)  # default value 100
sol_num.grid(row=3, column=2, padx=5, pady=5)

frame = Frame(root, bg="lightgrey")
frame.grid(row=4, column=1, columnspan=4, padx=5, pady=5)

Label(frame, text="Επιλέξτε μεγέθη κομματιών που θέλετε: ", bg="lightgrey").grid(row=0)

# Create variables and checkbuttons
s145 = IntVar()
Checkbutton(frame, width=10, text = '145', variable=s145, bg="lightgrey").grid(row=1)

s165 = IntVar()
Checkbutton(frame, width=10, text = '165', variable=s165, bg="lightgrey").grid(row=2)

s185 = IntVar()
Checkbutton(frame, width=10, text = '185', variable=s185, bg="lightgrey").grid(row=3)

s250 = IntVar()
Checkbutton(frame, width=10, text = '250', variable=s250, bg="lightgrey").grid(row=4)

s280 = IntVar()
Checkbutton(frame, width=10, text = '280', variable=s280, bg="lightgrey").grid(row=5)


Button(root, text="Εξαγωγή σε csv", command=export).grid(row=5, column=1, columnspan=4, padx=5, pady=5)

root.mainloop()