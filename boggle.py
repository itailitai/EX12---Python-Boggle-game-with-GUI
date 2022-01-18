import tkinter.messagebox

import boggle_board_randomizer as randomizer
import boggle_gui as gui
import ex12_utils as utils

INITIAL_TIME = 180  # initial time in seconds
HINT_ATTEMPTS = 3


class GameEngine:
    def __init__(self, board, words_list):
        """
        Initialize Boggle game
        :param board: board list
        :param words_list: words dictionary
        """
        self.__board = board
        self.__gui = gui.BoggleGUI(self.__board)
        self.__countdown_func = None
        self.reset(board, words_list)

    def reset(self, board, words_list):
        """
        Reset the game completely, this is seperated from __init__ due to the restart game functionality
        :param board:
        :param words_list:
        :return:
        """
        self.__board = board
        self.__words = words_list
        self.__score = 0
        self.__hint_attempts = HINT_ATTEMPTS
        self.__gui.update_hint(self.__hint_attempts)
        self.__game_lost = False
        self.__current_word = ''
        self.__current_path = []
        self.__gui.create_letters_buttons(True)
        for button in self.__gui.get_buttons():
            func = self.add_button_functionality(button, 'letter')
            self.__gui.set_button_action(button, func)

        # if we call the reset function and there's a countdown going on, terminate it and start a new one.
        if self.__countdown_func:
            self.__gui.root.after_cancel(self.__countdown_func)

        self.__time = INITIAL_TIME
        # change text in GUI time label
        mins, secs = divmod(self.__time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        self.__gui.update_timer(timer)

    def create_help_buttons(self):
        self.__hint_btn = self.__gui._make_hint_button()
        self.__gui.set_button_action(self.__hint_btn, self.add_button_functionality(self.__hint_btn, 'hint'))
        self.__restart_btn = self.__gui._make_restart_button()
        self.__gui.set_button_action(self.__restart_btn, self.add_button_functionality(self.__restart_btn, 'restart'))

    def check_if_neighbor(self, current_coordinate):
        """
        Check if a given coordinate is a neighbor of the last coordinate in our current path
        :param current_coordinate: given coordinate
        :return: True if neighbor, False otherwise
        """
        if len(self.__current_path) == 0:
            return True
        last_path_coordinate = self.__current_path[-1]
        if last_path_coordinate != current_coordinate and not (
                abs(last_path_coordinate[0] - current_coordinate[0]) > 1 or
                abs((last_path_coordinate[1] - current_coordinate[1])) > 1):
            return True
        return False

    def add_button_functionality(self, button, type):
        """
        Add GUI buttons functionality based on their type
        :param button: a given button
        :param type: a given button's type
        :return: the given button's function that'll fire when button's clicked
        """
        if type == 'letter':
            def letter_func():
                """
                Function to return when a letter button is clicked
                """
                if self.__time == INITIAL_TIME:
                    # If this is the first button press, uncover the letters, start countdown and create help buttons
                    self.__gui.show_letters_content()
                    self.create_help_buttons()
                    self.countdown()
                    return
                if not self.__game_lost:
                    position = self.__gui.button_coordinate(button)
                    letter = button['text']
                    if position not in self.__current_path:
                        if self.check_if_neighbor(position):
                            # If the clicked button is a neighbor of the last button in the path, add its content
                            # to the bottom indicator, add its coordinates to the path, and color it.
                            self.__current_word += letter
                            self.__current_path.append(position)
                            self.__gui.simulate_button_press(button,
                                                             self.__current_word)
                            # check if current words is valid, if so, add score and add the word to the guessed words
                            # list, in addition, display a message indicating the score added and play a nice animation.
                            word = utils.is_valid_path(self.__board,
                                                       self.__current_path,
                                                       self.__words)
                            if word and self.__words[word]:
                                added_score = self.__add_score()
                                for coord in self.__current_path:
                                    btn = self.__gui.get_button_from_coordinate(coord)
                                    self.__gui.run_animation('success', btn, 150)
                                self.__gui.add_user_message('Nice! +' + str(added_score), 2000)
                                self.__words[word] = False
                                self.__current_path = []
                                self.__gui.add_guessed_word(
                                    self.__current_word)
                                self.__gui.change_word_text('')
                                self.__current_word = ''
                                self.__gui.reset_board()
                        else:
                            # if button is not a neighbor, show a warning message and an animation showing which letters
                            # can be selected
                            buttons = self.__gui.get_buttons()
                            for btn in buttons:
                                if self.check_if_neighbor(buttons[btn][1]) and not buttons[btn][2]:
                                    self.__gui.run_animation('warning', btn, 150)
                                    self.__gui.add_user_message('ONLY NEARBY LETTERS\nCAN BE SELECTED', 3000, 9,
                                                                '#d64d3c')

                    else:
                        # if clicked button is already in our path, check if it can be deselected (if it's the last one
                        # in our path), if so, deselect it. Otherwise, show an appropriate message and animation.
                        last_path_button = self.__gui.get_button_from_coordinate(self.__current_path[-1])
                        if last_path_button == button:
                            self.__current_word = self.__current_word[
                                                  :-len(letter)]
                            self.__gui.simulate_button_press(button,
                                                             self.__current_word)
                            self.__current_path.pop()
                        else:
                            last_button_in_path = self.__gui.get_button_from_coordinate(self.__current_path[-1])
                            self.__gui.run_animation('warning', last_button_in_path, 75)
                            self.__gui.add_user_message('ONLY LAST LETTER\nCAN BE REMOVED', 3000, 9, '#d64d3c')

            return letter_func

        elif type == 'hint':
            def hint_func():
                """
                Function to return when a hint button is clicked
                """
                if self.__hint_attempts == 0:
                    self.__gui.add_user_message('NO REVEALS LEFT!', 4000, 12, '#d64d3c')
                    return
                hint_coordinates = self.__find_reveal()
                btn_list = []
                if not hint_coordinates:
                    # if there's no hint matching the current path, show the appropriate message.
                    self.__gui.add_user_message('NO WORDS\nMATCH THE PATH!', 4000, 10, '#d64d3c')
                else:
                    # If a hint is found, animate the letters of the word and remove one hint attempt.
                    self.__hint_attempts -= 1
                    self.__gui.update_hint(self.__hint_attempts)
                    for coord in hint_coordinates:
                        btn_list.append(self.__gui.get_button_from_coordinate(coord))
                    self.__gui.run_animation('hint', btn_list, 200)

            return hint_func
        elif type == 'restart':
            # if restart button is clicked, return a function that restart the game
            def restart_func():
                self.restart_game()

            return restart_func

    def __find_reveal(self):
        """
        A function that uses find_length_n_path from ex12_utils to find hints matching our path
        :return:
        """
        for n in range(len(self.__current_path) + 1, len(self.__board) ** 2 + 1):
            # search for paths larger than the current path
            paths = utils.find_length_n_paths(n, self.__board, list(self.__words.keys()))
            for path in paths:
                # if n = length of our path, then if the found path matches our path in the first n steps, and in
                # addition the word wasn't already found, then the path is valid hint and we shall return it.
                if self.__current_path == path[:len(self.__current_path)] and self.__words[self.__path_to_word(path)]:
                    return path

    def __path_to_word(self, path):
        # convert a path to a word
        word = ''
        for coordinate in path:
            word += self.__board[coordinate[0]][coordinate[1]]
        return word

    def __add_score(self):
        """
        Adds score, the score is the path length to the power of 2.
        :return: added score
        """
        added_score = len(self.__current_path) ** 2
        self.__score += added_score
        self.__gui.update_score('SCORE: ' + str(self.__score))
        return added_score

    def countdown(self):
        """
        Function that implements the game countdown
        :return:
        """
        # change text in GUI label
        mins, secs = divmod(self.__time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        self.__gui.update_timer(timer)

        if self.__time > 0:
            # call countdown again after 1000ms (1s)
            self.__time = self.__time - 1
            self.__countdown_func = self.__gui.root.after(1000, self.countdown)
        else:
            # if time's up, reset the board and run the game_over function.
            self.__gui.reset_board()
            self.__hint_btn.destroy()
            self.__gui.game_over(str(self.__score))
            self.__gui.add_user_message('YOU MAY RESTART BY\n USING THE BUTTON ABOVE', 60000, 8)

    def restart_game(self):
        """
        Restart the GUI and the game engine.
        :return:
        """
        board = randomizer.randomize_board()
        self.__gui.reset(board)
        words_list = utils.load_words_from_file("boggle_dict.txt")

        self.reset(board, words_list)

    @staticmethod
    def new_game():
        """
        Creates a new random game
        """
        board = randomizer.randomize_board()
        words_list = utils.load_words_from_file("boggle_dict.txt")
        controller = GameEngine(board, words_list)
        controller.start_game()

    def start_game(self):
        self.__gui.run()


if __name__ == '__main__':
    GameEngine.new_game()
