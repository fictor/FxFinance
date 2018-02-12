

from DemoWithMatplotLib import MatPlotLibDemo
#if __name__ == "__main__":
#    MatPlotLibDemo()

from tkinter import *
from tkinter.ttk import *
#import ttk

class ManagedComboBox:
    def __init__(self, parent):
        self.parent = parent
        self.value_of_combo = 'X'
        self.combo()

    def newselection(self, event):
        self.value_of_combo = self.box.get()
        print(self.value_of_combo)

    def get_current_value(self):
        return self.box.get()

    def combo(self):
        self.box_value = StringVar()
        self.box = Combobox(self.parent, textvariable=self.box_value)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box['values'] = ['x','y','z']

        self.box.current(0)
        self.box.grid(column=0, row=0)
        self.box.pack()
        # ...



root = Tk()

#combo_content = ['test1','test2']
#tkCombo = Combobox(root, textvariable=combo_content)
#tkCombo.pack()

mcb = ManagedComboBox(root)

def callback():
    print("click!")
    MatPlotLibDemo()
    print(mcb.get_current_value())

f = Frame(root, height=32, width=32)
f.pack_propagate(0) # don't shrink
f.pack()

tkLabel = Label(root, text="This is a label")

b = Button(root, text="OK", command=callback)
b.pack()
tkLabel.pack()
root.mainloop()
