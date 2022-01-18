def __is_coord_valid(coord, board):
    """
    :param coord:
    :return: True if valid, else False
    """
    return 0 <= coord[0] < len(board) and 0 <= coord[1] < len(board)


def is_valid_path(board, path, words):
    coordinates_visited = set()
    word_lst = []
    for i in range(len(path)):
        coord = path[i]
        if not __is_coord_valid(coord, board):
            return
        if i > 0 and (abs(path[i][0] - path[i - 1][0]) > 1 or
                      abs(path[i][1] - path[i - 1][1]) > 1):
            return
        if coord in coordinates_visited:
            return
        coordinates_visited.add(coord)
        for char in board[coord[0]][coord[1]]:
            word_lst.append(char)
    word = ''.join(word_lst)
    if word in words:
        return word


def __initials_set(words):
    """
    :param words: list of words
    :return: set of sub-sets of each word in words from word[0] to
    word[len(word) + 1]
    """
    return set(word[:i] for word in words for i in range(len(word) + 1))


def __find_length_n_helper(n, board, word_set, cur_coord, char_ind,
                           char_lst, coord_ind, coord_lst,
                           path_lst, compare_f, initials):
    if not __is_coord_valid(cur_coord, board) or not \
            board[cur_coord[0]][cur_coord[1]]:
        return

    cur_coord_str = board[cur_coord[0]][cur_coord[1]]
    for i in range(len(cur_coord_str)):
        char_lst[char_ind + i] = cur_coord_str[i]

    word = ''.join(
        char_lst[i] for i in range(char_ind + len(cur_coord_str)))

    if word not in initials:
        return

    coord_lst[coord_ind] = cur_coord

    # compare_f returns 1 if the relevant index > n, 0 if index == n else -1
    compare_f_res = compare_f(coord_ind + 1, char_ind + len(cur_coord_str), n)

    if compare_f_res >= 0:
        if compare_f_res == 1:
            return
        word = ''.join(
            char_lst[i] for i in range(char_ind + len(cur_coord_str)))
        if word in word_set:
            path_lst.append(coord_lst[:coord_ind + 1])
        return

    board[cur_coord[0]][cur_coord[1]] = None  # if we visited this coord

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            else:
                __find_length_n_helper(
                    n, board, word_set, (cur_coord[0] + i, cur_coord[1] + j),
                    char_ind + len(cur_coord_str), char_lst, coord_ind + 1,
                    coord_lst, path_lst, compare_f, initials)

    board[cur_coord[0]][cur_coord[1]] = cur_coord_str


def find_length_n_paths(n, board, words):
    # n too large for path of that length to be found
    if n > len(board) ** 2:
        return []

    path_lst = []
    char_lst = [None for _ in range(n + 2)]
    coord_lst = [None for _ in range(n + 1)]
    initials = __initials_set(words)

    for i in range(len(board)):
        for j in range(len(board)):
            __find_length_n_helper(n, board, words, (i, j), 0,
                                   char_lst, 0, coord_lst, path_lst,
                                   lambda path_len, word_len, n: 1 if
                                   path_len > n else (
                                       0 if path_len == n else -1), initials)
    return path_lst


def find_length_n_words(n, board, words):
    # n too large for word of that length to be found
    if n > 2 * len(board) ** 2:
        return []

    path_lst = []
    char_lst = [None for _ in range(n + 2)]
    coord_lst = [None for _ in range(n + 1)]
    word_set = set(words)
    initials = __initials_set(words)

    for i in range(len(board)):
        for j in range(len(board)):
            __find_length_n_helper(n, board, word_set, (i, j), 0,
                                   char_lst, 0, coord_lst, path_lst,
                                   lambda path_len, word_len, n: 1 if
                                   word_len > n else (
                                       0 if word_len == n else -1), initials)
    return path_lst


def __max_score_paths_helper(board, words_dict, cur_coord,
                             char_ind, char_lst, coord_ind, coord_lst,
                             initials):
    if not __is_coord_valid(cur_coord, board) or not \
            board[cur_coord[0]][cur_coord[1]]:
        return

    cur_coord_str = board[cur_coord[0]][cur_coord[1]]
    for i in range(len(cur_coord_str)):
        char_lst[char_ind + i] = cur_coord_str[i]

    coord_lst[coord_ind] = cur_coord
    word = ''.join(char_lst[i] for i in range(char_ind + len(cur_coord_str)))

    if word not in initials:
        return

    if word in words_dict:
        if not words_dict[word] or len(words_dict[word]) < coord_ind + 1:
            words_dict[word] = coord_lst[:coord_ind + 1]

    board[cur_coord[0]][cur_coord[1]] = None  # if we visited this coord
    # all the (dy, dx) of 8 directions
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            __max_score_paths_helper(board, words_dict,
                                     (cur_coord[0] + i, cur_coord[1] + j),
                                     char_ind + len(cur_coord_str),
                                     char_lst, coord_ind + 1,
                                     coord_lst, initials)
    board[cur_coord[0]][cur_coord[1]] = cur_coord_str


def max_score_paths(board, words):
    words_dict = {word: None for word in words}

    # len of word can be up to len(board)**2*2
    char_lst = [None for _ in range(len(board) ** 2 * 2)]

    # len of path can be up to len(board)**2
    coord_lst = [None for _ in range(len(board) ** 2)]

    initials = __initials_set(words)

    for i in range(len(board)):
        for j in range(len(board)):
            __max_score_paths_helper(board, words_dict, (i, j),
                                     0, char_lst, 0, coord_lst, initials)

    return list(words_dict[word] for word in words_dict if words_dict[word])


def load_words_from_file(file_path):
    """
    :param file_path: path of file with words
    :return: dict of the words in the file, when the value of each key is
    initialized as True
    """
    word_dict = dict()
    with open(file_path, "r") as word_file:
        for line in word_file.readlines():
            word_dict[line.strip("\n")] = True
    return word_dict
