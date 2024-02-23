import tkinter as tk
from tkinter import messagebox
from stocks import *

class Chatbot(tk.Tk):

    """Main chatbot class, inherits from tkinter's Tk class"""

    def __init__(self):
        super().__init__()
        self._stocks = Stocks("stock_data.json")
        self._stock_exchange_list = self._stocks.get_stock_exchange_list()
        self._current_stock_exchange = None
        self._current_stock_list = None
        self._state = None

        # app window title
        self.title("LSEG chatbot")

        # prevent resizing of app window (otherwise resizing will incorrectly cover some of the widgets)
        self.resizable(False, False)

        # replace app window's title bar icon with a custom one
        self.title_icon = tk.PhotoImage(file="chatbot_icon.png")
        self.iconphoto(False, self.title_icon)

        # main frame to hold all widgets
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # chat area frame
        self.chat_frame = tk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        # text area to display chat messages and user input
        self.text_area = tk.Text(self.chat_frame, bg="white", wrap="word")
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar for the chat text area
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # configure the chat window to use the scrollbar
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # set the state of the text area to disabled to prevent editing but enable copy/paste
        self.text_area.config(state=tk.DISABLED)
        self.text_area.bind("<1>", lambda event: self.text_area.focus_set())

        # frame for user input area
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X)

        # text entry widget for user input
        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=50)
        self.input_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # set placeholder text
        self.set_placeholder_text()
        
        # bind the set_placeholder_text and clear_placeholder_text methods to the text entry widget
        self.input_entry.bind("<FocusIn>", self.clear_placeholder_text)
        self.input_entry.bind("<FocusOut>", self.set_placeholder_text)

        # load send arrow icon
        self.send_icon = tk.PhotoImage(file="send_arrow.png")

        # create label to display arrow icon
        self.send_label = tk.Label(self.input_frame, image=self.send_icon, cursor="hand2")
        self.send_label.pack(side=tk.RIGHT, padx=5, pady=5)

        # bind send arrow press and Enter key press to get_user_input method
        self.send_label.bind("<Button>", self.get_user_input)
        self.input_entry.bind("<Return>", self.get_user_input)    

        # display main menu when starting app
        self.display_main_menu()

    def set_placeholder_text(self, event=None):
        """ Description: 
                Set placeholder text for user input field
            Arguments:
                * event (default: None) - event to bind the method to (e.g. mouse click, keyboard press, focus in/out) 
            Return Value: 
                * n/a
        """
        if not self.input_entry.get():
            self.input_entry.insert(0, "Please pick an option.")
            self.input_entry.config(fg='grey')

    def clear_placeholder_text(self, event):
        """ Description: 
                Clear placeholder text at focus in or when user starts typing 
            Arguments:
                * event - event to bind the method to (e.g. mouse click, keyboard press, focus in/out) 
            Return Value: 
                * n/a
        """
        if self.input_entry.get() == "Please pick an option.":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg='black')
    
    def insert_and_scroll(self, text, is_user_input=False):
        """ Description: 
                Insert text into chat text area and autoscroll to keep content visible
            Arguments:
                * text - the string to insert
                * is_user_input (default: False) - mark text as user input to align it to the right 
            Return Value: 
                * n/a
        """
        self.text_area.config(state=tk.NORMAL)
        if is_user_input:
            self.text_area.tag_configure("right", justify="right")
            self.text_area.insert(tk.END, f"{text}\n", "right")
        else:
            self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def display_main_menu(self):
        """ Description: 
                Display chatbot's main menu (list of stock exchanges to choose from)
            Arguments:
                * n/a
            Return Value: 
                * n/a
        """
        self.insert_and_scroll("=== Hello! Welcome to LSEG. I'm here to help you. ===\n")
        self.insert_and_scroll("=== Please select a Stock Exchange. ===\n")
        for stock_exchange in self._stock_exchange_list:
            self.insert_and_scroll(f"      {stock_exchange}\n")
        self._state = "main_menu_displayed"

    def display_stock_menu(self, stock_exchange):
        """ Description: 
                Upon selection, display available stocks for given stock exchange
            Arguments:
                * stock_exchange - given stock exchange (e.g. Nasdaq)
            Return Value: 
                * n/a
        """
        if self._current_stock_list == None:
            self._current_stock_list = self._stocks.get_stock_list(stock_exchange)
        self.insert_and_scroll("=== Please select a stock. ===\n")
        for stock in self._current_stock_list:
            self.insert_and_scroll(f"      {stock}\n")
        self._state = "stock_menu_displayed"
        if self._current_stock_exchange == None:
            self._current_stock_exchange = stock_exchange
    
    def display_stock_price(self, stock_exchange, stock):
        """ Description: 
                Display stock price for a given stock, in a predefined format
            Arguments:
                * stock_exchange - given stock exchange (e.g. Nasdaq)
                * stock - given stock (e.g. AMD) 
            Return Value: 
                * n/a
        """
        stock_price = self._stocks.get_stock_price(stock_exchange, stock)
        self.insert_and_scroll(f"Stock Price of {stock} is "
                               f"{stock_price:.2f}.Please select an option.\n")
        self.insert_and_scroll("      Main menu\n")
        self.insert_and_scroll( "      Go Back\n")
        self._state = "stock_price_displayed"
    
    def get_user_input(self, event=None):
        """ Description: 
                Main logic to interpret user's input and display the proper response
            Arguments:
                * event (default: None) - event to bind the method to (e.g. mouse click, keyboard press, focus in/out)
            Return Value: 
                * n/a
        """
        displayed_user_input = self.input_entry.get()

        # exit method if send button is pressed, but there's no user input
        if not displayed_user_input or displayed_user_input == "Please pick an option.":
            return

        self.input_entry.delete(0, tk.END)
        self.insert_and_scroll(displayed_user_input.strip(), is_user_input=True)
        user_input = displayed_user_input.strip().lower()

        if self._state == "main_menu_displayed":
            try:
                idx = [x.lower() for x in self._stock_exchange_list].index(user_input)
                self.display_stock_menu(self._stock_exchange_list[idx])
            except ValueError:
                self.insert_and_scroll("ERROR 001: Invalid input. Please select a stock exchange from the list above.\n")
        elif self._state == "stock_menu_displayed":
            try:
                idx = [x.lower() for x in self._current_stock_list].index(user_input)
                self.display_stock_price(self._current_stock_exchange, self._current_stock_list[idx])
            except ValueError:
                self.insert_and_scroll("ERROR 002: Invalid input. Please select a stock from the list above.\n")
        elif self._state == "stock_price_displayed":
                if user_input == "main menu":
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.config(state=tk.DISABLED)
                    self._current_stock_exchange = None
                    self._current_stock_list = None
                    self.display_main_menu()
                elif user_input == "go back":
                    self.display_stock_menu(self._current_stock_exchange)
                else:
                    self.insert_and_scroll("ERROR 003: Invalid input. Please select a valid option to go back.\n")
        else:
            self.insert_and_scroll("ERROR 004: Invalid state. Displaying main menu.\n")
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(state=tk.DISABLED)
            self._current_stock_exchange = None
            self._current_stock_list = None
            self.display_main_menu()

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.mainloop()