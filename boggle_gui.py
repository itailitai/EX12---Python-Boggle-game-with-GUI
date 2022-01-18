import tkinter
import tkinter as tki
from typing import Dict, Any

TOP_COLOR = '#d64d3c'
RIGHT_SIDE_COLOR = '#1a1a1a'
BOTTOM_COLOR = '#ffc67f'
HINT_COLOR = '#553fd0'
MAIN_FONT = 'Aharoni'


class BoggleGUI:
    _buttons: Dict[str, tki.Button] = {}

    def __init__(self, board) -> None:
        """
        Initialize GUI with given 4x4 board list
        :param board: 2 dimensional lists representing the game board
        """
        # initialize root settings
        self.root = tki.Tk()
        self.root.configure(background='black')
        self.root.title("BOGGLE - Made by Itai & Idan")
        self.root.resizable(False, False)

        # set gradient background image
        self._background_image = tki.PhotoImage(file='images/bg2.png')

        # set images attributes, these are attributes in order to prevent removal by the garbage collector.
        self._button_image = tki.PhotoImage(file='images/button_bg2.png')
        self._button_warning = tki.PhotoImage(file='images/alert_button.png')
        self._button_success = tki.PhotoImage(file='images/success_button.png')
        self._hint_letter_button = tki.PhotoImage(file='images/hint_letter_button.png')
        self._selected_button_image = tki.PhotoImage(file='images/button_clicked.png')
        self._hover_button_image = tki.PhotoImage(file='images/selected_button.png')
        self._clock_image = tki.PhotoImage(file='images/time.png')
        self._logo_image = tki.PhotoImage(file='images/logo.png')
        self._hint_button_image = tki.PhotoImage(file='images/hint_button.png')
        self._hint_button_hover_image = tki.PhotoImage(file='images/hint_button_dark.png')
        self._restart_button_image = tki.PhotoImage(file='images/restart_button.png')
        self._restart_button_image_hover = tki.PhotoImage(file='images/restart_button_dark.png')
        self._main_window = self.root

        # creates the gui
        self.reset(board)

    def reset(self, board):
        """
        Reset GUI with a new board
        :param board: new board list
        :return:
        """
        self.__board = board
        for widget in self.root.winfo_children():
            widget.destroy()
        self._buttons = {}
        self.create_gui()

    def create_gui(self):
        """
        Creates the GUI using the tkinter library
        This function is separated from __init__ due to the restart game functionality
        :return: None
        """
        self._outer_frame = tki.Frame(self.root)
        background_label_1 = tki.Label(self._outer_frame,
                                       image=self._background_image)
        background_label_1.place(x=1, y=1, relwidth=1, relheight=1)
        ###
        self._top_frame = tki.Frame(self._outer_frame)

        # top labels
        self.__score_label = tki.Label(self._top_frame, font=(MAIN_FONT, 25),
                                       background=TOP_COLOR,
                                       highlightbackground=TOP_COLOR,
                                       highlightcolor=TOP_COLOR,
                                       highlightthickness=7, bd=0, fg="#fff",
                                       text='SCORE: 0', width=30)
        self._logo_label = tki.Label(self._top_frame, image=self._logo_image,
                                     background=TOP_COLOR)
        self._time_image = tki.Label(self._top_frame, image=self._clock_image,
                                     background=TOP_COLOR)
        self._time_label = tki.Label(self._top_frame, font=(MAIN_FONT, 20),
                                     width=0, background=TOP_COLOR,
                                     pady=15,
                                     highlightthickness=0, bd=0, fg="#fff",
                                     text='99:99')

        # initialize letter area, and current guess area
        self._letters_area = tki.Frame(self._outer_frame)
        background_label_2 = tki.Label(self._letters_area,
                                       image=self._background_image)
        background_label_2.place(x=1, y=1, relwidth=1, relheight=1)
        self._word_area = tki.Frame(self._outer_frame)
        self._word_label = tki.Label(self._word_area,
                                     font=(MAIN_FONT, 20, "bold"), width=0,
                                     background=BOTTOM_COLOR,
                                     pady=15,
                                     highlightbackground=RIGHT_SIDE_COLOR,
                                     highlightcolor=RIGHT_SIDE_COLOR,
                                     highlightthickness=0, bd=0, fg=RIGHT_SIDE_COLOR,
                                     text='')

        # create found words area
        self._guessed_words_area = tki.Frame(self._outer_frame,
                                             background=RIGHT_SIDE_COLOR)
        self._hint_area = tki.Frame(self._guessed_words_area, background=HINT_COLOR)
        self.__hints_attempts_label = tki.Label(self._guessed_words_area, font=('Arial', 12, 'bold'),
                                                background=HINT_COLOR, fg="#fff")
        self.__user_message_area = tki.Label(self._guessed_words_area,
                                             font=('Arial', 15, 'bold'),
                                             background=HINT_COLOR,
                                             pady=25, padx=10,
                                             highlightbackground=HINT_COLOR,
                                             highlightcolor=HINT_COLOR,
                                             highlightthickness=0, bd=0,
                                             fg="#fff", text='')

        self._guessed_words_label = tki.Label(self._guessed_words_area,
                                              font=(MAIN_FONT, 12),
                                              background=RIGHT_SIDE_COLOR,
                                              pady=25, padx=20,
                                              highlightbackground=RIGHT_SIDE_COLOR,
                                              highlightcolor=RIGHT_SIDE_COLOR,
                                              highlightthickness=0, bd=0,
                                              fg="#fff", text='WORDS FOUND:')

        self.list_of_words = tki.Listbox(self._guessed_words_area,
                                         background=RIGHT_SIDE_COLOR,
                                         highlightthickness=0,
                                         bd=0, width=0, font=(MAIN_FONT, 12),
                                         fg="#fff")
        self._scrollbar = tki.Scrollbar(self._guessed_words_area)
        self.list_of_words.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar.config(command=self.list_of_words.yview)

        # pack everything
        self.pack()

    def get_buttons(self):
        return self._buttons

    def set_button_action(self, button, action):
        button.configure(command=action)

    def create_letters_buttons(self, beginning=False):
        """
        Create Boggle letters 4x4 grid
        :return: None
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._letters_area, i,
                                     weight=0)  # type: ignore

        for i in range(4):
            tki.Grid.rowconfigure(self._letters_area, i,
                                  weight=1)  # type: ignore

        for i in range(4):
            for j in range(4):
                btn = self._make_button('PRESS\nANY TO \nREVEAL AND\nSTART', i, j)
                btn.config(font=(MAIN_FONT, 11))

    def show_letters_content(self):
        for i in range(4):
            for j in range(4):
                button = self.get_button_from_coordinate((i, j))
                button.config(text=self.__board[i][j], font=(MAIN_FONT, 40, 'bold'))

    def button_coordinate(self, button):
        return self._buttons[button][1]

    def reset_board(self):
        """
        reset all buttons to default state
        :return: None
        """
        for button in self._buttons:
            button.config(image=self._button_image)
            self._buttons[button][2] = False

    def _make_button(self, button_char: str, row: int, col: int):
        """
        Create a GUI letter button and add it to the buttons dictionary
        :param button_char: Button's text
        :param row: Button's position on the board: [row][col]
        :param col: Button's position on the board: [row][col]
        :return: Newly created button
        """
        button = tki.Button(self._letters_area)
        button.config(image=self._button_image, text=button_char, width=125, height=140,
                      compound="center",
                      fg='#000000', highlightbackground="#000000",
                      highlightcolor="#000000", highlightthickness=0, bd=0)
        button.grid(row=row, column=col, rowspan=1,
                    columnspan=1, pady=20, padx=20)
        self._buttons[button] = [button_char, (row, col), False]

        def _on_enter(event: Any):
            # on hover change button pic
            if not self._buttons[button][2]:
                button.config(image=self._hover_button_image)

        def _on_leave(event: Any):
            # reset button pic when hover ends
            if not self._buttons[button][2]:
                button.config(image=self._button_image)

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        return button

    def _make_hint_button(self):
        """
        Create a GUI hint button
        :return: hint button
        """
        button = tki.Button(self._hint_area)
        button.config(image=self._hint_button_image, text='',
                      font=(MAIN_FONT, 40, 'bold'), width=80, height=70,
                      compound="center",
                      fg='#000000', highlightbackground="#000000",
                      highlightcolor="#000000", highlightthickness=0, bd=0)

        def _on_enter(event: Any):
            # on hover change button pic
            button.config(image=self._hint_button_hover_image)

        def _on_leave(event: Any):
            # reset button pic when hover ends
            button.config(image=self._hint_button_image)

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        button.pack(side=tki.RIGHT)
        return button

    def _make_restart_button(self):
        """
        Create a GUI restart button
        :return: restart button
        """
        button = tki.Button(self._hint_area)
        button.config(image=self._restart_button_image, text='',
                      font=(MAIN_FONT, 40, 'bold'), width=80, height=70,
                      compound="center",
                      fg='#000000', highlightbackground="#000000",
                      highlightcolor="#000000", highlightthickness=0, bd=0)

        def _on_enter(event: Any):
            # on hover change button pic
            button.config(image=self._restart_button_image_hover)

        def _on_leave(event: Any):
            # reset button pic when hover ends
            button.config(image=self._restart_button_image)

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

        button.pack(side=tki.LEFT)
        return button

    def change_button_text(self, row, col, new_text):
        self._buttons[(row, col)][1].configure(text=new_text)

    def change_word_text(self, new_text):
        self._word_label.config(text=new_text)

    def add_guessed_word(self, new_word):
        self.list_of_words.insert(tki.END, new_word)

    def update_timer(self, time):
        self._time_label.config(text=time)

    def update_score(self, score):
        self.__score_label.config(text=score)

    def update_hint(self, num):
        self.__hints_attempts_label.config(text='REVEALS: ' + str(num))

    def simulate_button_press(self, button, word):
        """
        Change the button image on click and change bottom indicator content,
        reset the button image if clicked again
        :param button: a given button
        :param word: current word made by the current path
        :return: None
        """
        if self._buttons[button][2]:
            button.config(image=self._button_image)
            self._buttons[button][2] = False
        else:
            self._buttons[button][2] = True
            button.config(image=self._selected_button_image)
        self.change_word_text(word)

    def run_animation(self, type, button, time_delay):
        """
        Create letter buttons animation, calls the __animation_step function
        :param type: Animation type (success/warning/finished game)
        :param button: button to animate
        :param time_delay: delay between each animation frame
        :return: None
        """
        if type == 'hint' or type == 'finish':
            # In this case there are multiple buttons to be animated, number of frames and the buttons' images are saved
            # onto lists accordingly
            animation_frames = iter(range(0, len(button) + 1))
            temp_images = [btn['image'] for btn in button]
            self.__animation_step(animation_frames, type, button,
                                  temp_images, time_delay)
        else:
            animation_frames = iter(range(0, 6))
            self.__animation_step(animation_frames, type, button,
                                  button['image'], time_delay)

    def __animation_step(self, animation_frames, type, button,
                         temp_img, time_delay):
        """
        Recursive function that stops when the iteration of animation_frames is over
        Creates different animations based on the given animation type
        :param animation_frames: number of animation frames
        :param type: animation type to assign to the button
        :param button: button to animate
        :param temp_img: previous button image/images (saved for resetting the button image after the animation is over)
        :param time_delay: time delay between each animation frame
        :return: None
        """
        try:
            count = next(animation_frames)
        except StopIteration:
            return

        try:
            if type == 'warning':
                if count % 2 == 0:
                    button.config(image=self._button_warning)
                else:
                    button.config(image=temp_img)
            elif type == 'success':
                if count % 2 == 0:
                    button.config(image=self._button_success)
                else:
                    button.config(image=self._button_image)
            elif type == 'hint' or type == 'finish':
                if count == len(button):
                    # If this is the last frame of the animation, reset all the buttons to the default image
                    for i, btn in enumerate(button):
                        btn.config(image=temp_img[i])
                else:
                    img = self._hint_letter_button if type == 'hint' else self._button_success
                    button[count].config(image=img)

            self.root.after(time_delay, self.__animation_step, animation_frames,
                            type, button, temp_img, time_delay)
        except Exception:
            # an exception may occur if game restarts during an animation
            # if so, animation should abort
            return

    def add_user_message(self, message, message_time, font_size=15, color='white'):
        """
        Adds feedback messages on the right side of the GUI
        :param message: message content
        :param message_time: time to desplay the message
        :param font_size: self-explanatory
        :return: None
        """
        self.__user_message_area.config(text=message, font=('Arial', font_size, 'bold'), fg=color)

        def remove_messaege():
            # inner function to remove the message after a certain delay
            self.__user_message_area.config(text='', font=('Arial', 15, 'bold'))

        self.root.after(message_time, remove_messaege)

    def get_button_from_coordinate(self, coordinate):
        list_of_buttons = [key for key, value in self._buttons.items() if
                           coordinate == value[1]]
        return list_of_buttons[0]

    def game_over(self, score):
        """
        Display game-over screen.
        Divide 'GAME OVER' and the score between letters button, and do a little animation
        :param score: score to display on the game over screen
        :return: None
        """
        temp_score = score
        text_message = 'GAMEOVER'
        all_message_buttons = []
        for i, button in enumerate(self._buttons):
            # divide the game over message between buttons
            if i < len(text_message):
                button.config(text=text_message[i], image=self._hint_letter_button)
                all_message_buttons.append(button)
            else:
                button.config(text='')
            # remove buttons functionality
            button.config(command=tki.NONE)
            button.unbind("<Enter>")
            button.unbind("<Leave>")
        all_score_buttons = []
        for i in range(len(self._buttons) - 1,
                       len(self._buttons) - len(temp_score) - 1, -1):
            # divide score between letters buttons based on the score length
            list(self._buttons.keys())[i].config(text=temp_score[-1], image=self._button_success)
            all_score_buttons.append(list(self._buttons.keys())[i])
            temp_score = temp_score[:-1]
        # add 'Score:' to the appropriate button
        all_score_buttons.append(list(self._buttons.keys())[(len(self._buttons) - len(score) - 1)])
        list(self._buttons.keys())[(len(self._buttons) - len(score) - 1)].config(text='SCORE:', font=(MAIN_FONT, 14),
                                                                                 image=self._button_success)
        # reverse the list for the animation
        all_score_buttons = list(reversed(all_score_buttons))
        # run animations
        self.run_animation('finish', all_message_buttons, 150)
        self.run_animation('hint', all_score_buttons, 750)

    def pack(self):
        # Pack all GUI items
        self._outer_frame.pack()
        self._top_frame.pack(side=tki.TOP, fill=tki.BOTH)
        self._time_image.pack(side=tki.LEFT, fill=tki.BOTH)
        self._time_label.pack(side=tki.LEFT, fill=tki.BOTH)
        self.__score_label.pack(side=tki.LEFT, fill=tki.BOTH)
        self._logo_label.pack(side=tki.RIGHT, fill=tki.BOTH)
        self._word_label.pack(side=tki.BOTTOM, fill=tki.BOTH)
        self._guessed_words_area.pack(side=tki.RIGHT, fill=tki.BOTH,
                                      expand=True)
        self._hint_area.pack(fill=tki.BOTH)
        self.__hints_attempts_label.pack(side=tki.TOP, fill=tki.BOTH)
        self.__user_message_area.pack(side=tki.TOP, fill=tki.BOTH)
        self._guessed_words_label.pack(side=tki.TOP, fill=tki.BOTH)
        self.list_of_words.pack(padx=5, side=tki.LEFT, fill=tki.BOTH)
        self._scrollbar.pack(side=tki.RIGHT, fill=tki.BOTH)
        self._letters_area.pack(side=tki.TOP)
        self._word_area.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

    def run(self):
        self._main_window.mainloop()
