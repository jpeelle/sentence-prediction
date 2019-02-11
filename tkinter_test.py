from tkinter import *

class Output_Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Search Results")
        self.pack(fill=BOTH, expand=1)

class GUI_Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.entropy_lower_string = StringVar()
        self.entropy_upper_string = StringVar()
        self.num_resp_lower_string = StringVar()
        self.num_resp_upper_string = StringVar()
        self.answer_word_string = StringVar()
        self.answer_lower_string = StringVar()
        self.answer_upper_string = StringVar()
        #self.output_text = Text(self, wrap=WORD) #Create new window for text instead of adding it to current one
        self.init_window()

    def init_window(self):
        self.master.title("Sentence Predictability Analysis")
        self.pack(fill=BOTH, expand=1)

        quit_button = Button(self, text="Quit", command=self.client_exit, font=("Helvetica", 18))
        search_button = Button(self, text="Search", command=self.search, font=("Helvetica", 18))

        entropy_label = Label(self, text="Response Entropy", font=("Helvetica", 18))
        entropy_lower_label = Label(self, text='Lower Bound:')
        entropy_lower_entry = Entry(self, textvariable=self.entropy_lower_string)
        entropy_upper_label = Label(self, text='Upper Bound:')
        entropy_upper_entry = Entry(self, textvariable=self.entropy_upper_string)

        num_resp_label = Label(self, text="Number of Responses", font=("Helvetica", 18))
        num_resp_lower_label = Label(self, text='Lower Bound:')
        num_resp_lower_entry = Entry(self, textvariable=self.num_resp_lower_string)
        num_resp_upper_label = Label(self, text='Upper Bound:')
        num_resp_upper_entry = Entry(self, textvariable=self.num_resp_upper_string)

        answer_label = Label(self, text="Target Response", font=("Helvetica", 18))
        answer_word_label = Label(self, text='Response:')
        answer_word_entry = Entry(self, textvariable=self.answer_word_string)
        answer_lower_label = Label(self, text='Lower Bound:')
        answer_lower_entry = Entry(self, textvariable=self.answer_lower_string)
        answer_upper_label = Label(self, text='Upper Bound:')
        answer_upper_entry = Entry(self, textvariable=self.answer_upper_string)

        for i in range(10):
            Grid.rowconfigure(self, i, weight=1)
        for j in range(4):
            Grid.columnconfigure(self, j, weight=1)

        entropy_label.grid(row='1', columnspan='4', pady='10', sticky=N+S+E+W)
        entropy_lower_label.grid(row='2', column='0', pady='10', padx='10', sticky=N+S+E+W)
        entropy_lower_entry.grid(row='2', column='1', pady='10', sticky=N+S+E+W)
        entropy_upper_label.grid(row='2', column='2', pady='10', sticky=N+S+E+W)
        entropy_upper_entry.grid(row='2', column='3', pady='10', padx='10', sticky=N+S+E+W)

        num_resp_label.grid(row='3', columnspan='4', pady='10', sticky=N+S+E+W)
        num_resp_lower_label.grid(row='4', column='0', pady='10', padx='10', sticky=N+S+E+W)
        num_resp_lower_entry.grid(row='4', column='1', pady='10', sticky=N+S+E+W)
        num_resp_upper_label.grid(row='4', column='2', pady='10', sticky=N+S+E+W)
        num_resp_upper_entry.grid(row='4', column='3', pady='10', padx='10', sticky=N+S+E+W)

        answer_label.grid(row='5', columnspan='4', pady='10', sticky=N+S+E+W)
        answer_word_label.grid(row='6', column='0', pady='10', sticky=N+S+E+W)
        answer_word_entry.grid(row='6', column='1', pady='10', sticky=N+S+E+W)
        answer_lower_label.grid(row='7', column='0', pady='10', padx='10', sticky=N+S+E+W)
        answer_lower_entry.grid(row='7', column='1', pady='10', sticky=N+S+E+W)
        answer_upper_label.grid(row='7', column='2', pady='10', sticky=N+S+E+W)
        answer_upper_entry.grid(row='7', column='3', pady='10', padx='10', sticky=N+S+E+W)

        #self.output_text.grid(row='10', columnspan='4')

        search_button.grid(row='8', columnspan='4', pady='10')
        quit_button.grid(row='9', columnspan='4', pady='10')

    def client_exit(self):
        exit()

    def search(self):
        entropy_lower = self.entropy_lower_string.get()
        entropy_upper = self.entropy_upper_string.get()
        num_resp_lower = self.num_resp_lower_string.get()
        num_resp_upper = self.num_resp_upper_string.get()
        answer_word = self.answer_word_string.get()
        answer_lower = self.answer_lower_string.get()
        answer_upper = self.answer_upper_string.get()
        if entropy_lower:
            #self.output_text.insert(INSERT, entropy_lower)
            #self.output_text.insert(INSERT, '\n')
            print(entropy_lower)
        if entropy_upper:
            #self.output_text.insert(INSERT, entropy_upper)
            #self.output_text.insert(INSERT, '\n')
            print(entropy_upper)
        if num_resp_lower:
            #self.output_text.insert(INSERT, num_resp_lower)
            #self.output_text.insert(INSERT, '\n')
            print(num_resp_lower)
        if num_resp_upper:
            #self.output_text.insert(INSERT, num_resp_upper)
            #self.output_text.insert(INSERT, '\n')
            print(num_resp_upper)
        if answer_word:
            answer_word_list = answer_word.split(',')
            for w in answer_word_list:
                #self.output_text.insert(INSERT, w)
                #self.output_text.insert(INSERT, '\n')
                print(w)
        if answer_lower:
            #self.output_text.insert(INSERT, answer_lower)
            #self.output_text.insert(INSERT, '\n')
            print(answer_lower)
        if answer_upper:
            #self.output_text.insert(INSERT, answer_upper)
            #self.output_text.insert(INSERT, '\n')
            print(answer_upper)

root = Tk()

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
app = GUI_Window(root)


root.mainloop()
