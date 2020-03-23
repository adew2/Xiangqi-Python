# Author: Alex DeWald
# Date: 3-10-2020
# Description: This program creates a game of Xiangqi (Chinese chess). The player plays the game by initializing a
# XiangqiGame() object and using the .make_move method of the XiangqiGame object. The Red player starts first. Other
# methods available to the player are .is_in_check('black) and .is_in_check('red'), which tells if a player is in check.
# The .get_game_state() method returns the state of the game, either "UNFINISHED", "RED_WON" or "BLACK_WON". Moves are
# performed by using algebraic notation i.e. "a1", "b1".


class XiangqiGame:
    """
    Represents a Xiangqi game object with methods to get the game board, print the game board, get the general
    coordinates, get the game state, get current player, switch player's turn, make a move, and return if a player is in
    check.
    """

    def __init__(self):
        """
        Constructs a Xiangqi game object with private data members of a game board, state of the game, the current
        player, red player check status, black player check status, and a coordinate dictionary.
        """
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._current_player = "RED"
        self._red_check = False
        self._black_check = False
        self._coord = \
            {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5, "6": 4, "7": 3, "8": 2, "9": 1, "10": 0,
             "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8
             }  # used to convert string coordinates to list coordinates

    def get_board(self):
        """returns the board data member's Board"""
        return self._board.get_board()

    def print_board(self):
        """prints the board data member's Board"""
        return self._board.print_board()

    def get_general_coords(self):
        """returns the board data member's general coordinates"""
        return self._board.general_location()

    def get_game_state(self):
        """returns the game's state"""
        return self._game_state

    def get_current_player(self):
        """returns which player's turn it is"""
        return self._current_player

    def set_current_player(self):
        """sets the next player's turn"""
        if self._current_player == "RED":
            self._current_player = "BLACK"
        elif self._current_player == "BLACK":
            self._current_player = "RED"

    def make_move(self, move_from, move_to):
        """
        checks if a move is valid for the game board, returns True if valid, False if not
        :param move_from - coordinate of piece to move
        :param move_to - coordinate of where piece is to move
        """
        if self._game_state != "UNFINISHED":
            return False
        # convert string coordinates to list
        move_from = list(move_from)
        move_to = list(move_to)
        if len(move_from) < 3 and "0" in move_from:
            return False
        if len(move_to) < 3 and "0" in move_to:
            return False
        # check if move_from coordinate contains a "1","0" and converts it to "10"
        if "0" in move_from:
            join = str(move_from[1] + move_from[2])
            move_from.remove("0")
            move_from.remove("1")
            move_from.append(join)
        # check if move_to coordinate contains a "1","0" and converts it to "10"
        if "0" in move_to:
            join = str(move_to[1] + move_to[2])
            move_to.remove("0")
            move_to.remove("1")
            move_to.append(join)
        # reverse the coordinates to function with game board list/array
        move_from.reverse()
        move_to.reverse()
        # convert list of string coordinates to integers using dictionary data member
        index = 0
        for i in move_from:
            if i in self._coord.keys():
                move_from[index] = self._coord.get(i)
                index += 1
        index = 0
        for i in move_to:
            if i in self._coord.keys():
                move_to[index] = self._coord.get(i)
                index += 1
        # check if coordinates are not valid i.e. "11", "22", etc.
        for num in move_from:
            if type(num) == str:
                return False
        for num in move_to:
            if type(num) == str:
                return False
        # attempt to make a move on the game board
        move = self._board.check_move(move_from, move_to, "NORMAL", self._current_player)
        if move:
            # check if black player is in check after move
            black_in_check = self._board.gen_check("RED")
            if black_in_check == "RED":  # black general found to be in check
                if self._current_player == "RED":  # player was red = black general now in check status
                    self._black_check = True
                elif self._current_player == "BLACK":  # player was black, clear invalid move
                    return self._board.clear_move(move_from, move_to)
            elif black_in_check == "NONE":  # if black player not in check, black now not in check status
                self._black_check = False

            # check if red player is in check after move
            red_in_check = self._board.gen_check("BLACK")
            if red_in_check == "BLACK":  # red general found to be in check
                if self._current_player == "BLACK":  # player was black = red general now in check status
                    self._red_check = True
                elif self._current_player == "RED":  # player was red, clear invalid move
                    return self._board.clear_move(move_from, move_to)
            elif black_in_check == "NONE":  # if red player not in check, red now not in check status
                self._red_check = False

            # check for stalemate or checkmate
            stale = self._board.stalemate()
            if stale == "RED":  # RED player has no valid moves to not put general in check
                self._game_state = "BLACK_WON"
            elif stale == "BLACK":  # BLACK player has no valid moves to not put general in check
                self._game_state = "RED_WON"

            self.set_current_player()  # change turn to next player
            return move  # return true if move valid
        else:
            return False  # return False if move not valid

    def is_in_check(self, player):
        """
        returns if player is in check
        :param player - 'red' or 'black'
        """
        if player == "red":
            return self._red_check
        elif player == "black":
            return self._black_check


class Board:
    """
    Represents a Xiangqi game board with methods to retrieve the board, get the general locations, print the board,
    check if a move is valid, check if a player is in check, and check for stalemate or checkmate.

    """

    def __init__(self):
        """
        Constructs a Xiangqi Board object with private data members of all game pieces, a board, general location
        coordinates, and a temporary piece holder.
        """
        self._G1 = General("RED")
        self._G2 = General("BLACK")
        self._A1 = Advisor("RED")
        self._A2 = Advisor("RED")
        self._A3 = Advisor("BLACK")
        self._A4 = Advisor("BLACK")
        self._E1 = Elephant("RED")
        self._E2 = Elephant("RED")
        self._E3 = Elephant("BLACK")
        self._E4 = Elephant("BLACK")
        self._H1 = Horse("RED")
        self._H2 = Horse("RED")
        self._H3 = Horse("BLACK")
        self._H4 = Horse("BLACK")
        self._R1 = Chariot("RED")
        self._R2 = Chariot("RED")
        self._R3 = Chariot("BLACK")
        self._R4 = Chariot("BLACK")
        self._C1 = Cannon("RED")
        self._C2 = Cannon("RED")
        self._C3 = Cannon("BLACK")
        self._C4 = Cannon("BLACK")
        self._S1 = Soldier("RED")
        self._S2 = Soldier("RED")
        self._S3 = Soldier("RED")
        self._S4 = Soldier("RED")
        self._S5 = Soldier("RED")
        self._S6 = Soldier("BLACK")
        self._S7 = Soldier("BLACK")
        self._S8 = Soldier("BLACK")
        self._S9 = Soldier("BLACK")
        self._S10 = Soldier("BLACK")
        self._general_check = [[0, 4], [9, 4]]  # [0] = black, # [1] = red
        self._temp = None
        self._board = \
            [[self._R3, self._H3, self._E3, self._A3, self._G2, self._A4, self._E4, self._H4, self._R4],
             ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
             ["  ", self._C3, "  ", "  ", "  ", "  ", "  ", self._C4, "  "],
             [self._S6, "  ", self._S7, "  ", self._S8, "  ", self._S9, "  ", self._S10],
             ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
             ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
             [self._S1, "  ", self._S2, "  ", self._S3, "  ", self._S4, "  ", self._S5],
             ["  ", self._C1, "  ", "  ", "  ", "  ", "  ", self._C2, "  "],
             ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
             [self._R1, self._H1, self._E1, self._A1, self._G1, self._A2, self._E2, self._H2, self._R2]
             ]

    def get_board(self):
        """returns the game board"""
        return self._board

    def general_location(self):
        """returns the coordinates for both player's generals"""
        return self._general_check

    def print_board(self):
        """prints the game board"""  # NOTE: this must be used after the LAST turn has taken place
        print("     a", "    b ", "   c", "    d", "    e"  "     f", "    g", "    h", "    i")
        i = 10
        for row in self._board:
            ecx = 0
            for piece in row:
                if piece != "  ":
                    if piece.get_player() == "RED":
                        row[ecx] = str("R" + piece.get_code())
                    else:
                        row[ecx] = str("B" + piece.get_code())
                ecx += 1
            if i == 10:
                print(i, row)
                i -= 1
            else:
                print(i, "", row)
                i -= 1
        print("     a", "    b ", "   c", "    d", "    e"  "     f", "    g", "    h", "    i")

    def check_move(self, move_from, move_to, function, player):
        """
        checks if the player entered move is valid
        :param move_from - piece to move coordinates
        :param move_to - coordinates to move piece
        :param function - 'NORMAL', 'STALE', or 'GENCHECK'
        :param player - 'RED' or 'BLACK'
        """
        # check if coordinates are on the board
        if (move_from[0] > 9 or move_to[0] > 9) or (move_from[1] > 8 or move_to[1] > 8):
            return False
        # check if actual piece is being moved, not a blank space
        if self._board[move_from[0]][move_from[1]] == "  ":
            return False
        # castle coordinates for red and black players
        castle = [[9, 4], [9, 5], [9, 3], [8, 4], [8, 5], [8, 3], [7, 4], [7, 5], [7, 3]]
        castle2 = [[0, 4], [0, 5], [0, 3], [1, 4], [1, 5], [1, 3], [2, 4], [2, 5], [2, 3]]
        piece = self._board[move_from[0]][move_from[1]]  # piece being moved
        landing = self._board[move_to[0]][move_to[1]]  # piece/space being moved to
        current = move_from
        # check if piece being moved belongs to current player
        if piece.get_player() != player:
            return False
        # check if location being moved to is not of same color/player
        if landing != "  ":
            if landing.get_player() == piece.get_player():
                return False

        # if piece has diagonal movement and is an elephant/advisor
        if piece.get_direction() == "DIAG":
            i = 0  # space counter
            while i < piece.get_spaces():
                diag1 = [[current[0] - 1, current[1] - 1], [current[0] - 1, current[1] + 1],
                         [current[0] + 1, current[1] - 1],
                         [current[0] + 1, current[1] + 1]
                         ]  # list of possible diagonal locations

                if piece.get_code() == "E" or piece.get_code() == "A":
                    # check if elephant is trying to cross the "river"
                    if piece.get_player() == "RED" and piece.get_code() == "E":
                        if move_to[0] < 5:
                            return False
                    elif piece.get_player() == "BLACK" and piece.get_code() == "E":
                        if move_to[0] > 4:
                            return False
                    # find proper diagonal current of next immediate diagonal space to move
                    # this is based on its move_to location
                    if current[0] > move_to[0]:
                        if current[1] < move_to[1]:
                            current = diag1[1]
                        else:
                            current = diag1[0]
                    if current[0] < move_to[0]:
                        if current[1] > move_to[1]:
                            current = diag1[2]
                        else:
                            current = diag1[3]
                    # check if current spot is in the castle if an advisor
                    if piece.get_code() == "A" and piece.get_player() == "RED":
                        if current not in castle:
                            return False
                    elif piece.get_code() == "A" and piece.get_player() == "BLACK":
                        if current not in castle2:
                            return False
                    # if current spot is off the board
                    if current[0] > 9 or current[1] > 8:
                        return False
                    # check if elephant for "blinding"
                    # the adjacent diagonal position of it's current location cannot be occupied
                    if self._board[current[0]][current[1]] != "  ":
                        if i == 0 and piece.get_code() == "E":
                            return False
                i += 1  # increment counter for next diagonal spot if elephant
                # check if elephant is trying to move only one diagonal location
                if piece.get_code() == "E" and current == move_to and i != 2:
                    return False
            if current != move_to:
                return False

        # if the piece to move is a horse
        if piece.get_code() == "H":
            otrho1 = [[current[0], current[1] - 1], [current[0], current[1] + 1],
                      [current[0] - 1, current[1]],
                      [current[0] + 1, current[1]]
                      ]  # possible orthogonal movements for horse's first move spot

            # find the initial orthogonal movement based on horse's move_to destination
            if move_to in otrho1:
                return False
            if current[0] > move_to[0] and (move_to[1] == move_from[1] + 1 or move_to[1] == move_from[1] - 1):
                current = otrho1[2]
            elif current[1] - 2 == move_to[1]:
                current = otrho1[0]
            elif current[1] + 2 == move_to[1]:
                current = otrho1[1]
            else:
                current = otrho1[3]
            # check if horse orthogonal movement goes off the board
            if current[0] > 9 or current[1] > 8:
                return False
            # check if horse is blocked/"hobbled"
            if self._board[current[0]][current[1]] != "  ":
                return False
            # find the horse's next spot, based on diagonal movement
            diag1 = [[current[0] - 1, current[1] - 1], [current[0] - 1, current[1] + 1],
                     [current[0] + 1, current[1] - 1],
                     [current[0] + 1, current[1] + 1]
                     ]

            if current[0] > move_to[0]:
                if current[1] < move_to[1]:
                    current = diag1[1]
                else:
                    current = diag1[0]
            if current[0] < move_to[0]:
                if current[1] > move_to[1]:
                    current = diag1[2]
                else:
                    current = diag1[3]

        # if piece to be moved has orthogonal ONLY movement
        if piece.get_direction() == "ORTHO":
            cannon_count = 0  # used to check that cannon has a "screen"
            i = 0
            while i < piece.get_spaces() and current != move_to:
                otrho1 = [[current[0], current[1] - 1], [current[0], current[1] + 1],
                          [current[0] - 1, current[1]],
                          [current[0] + 1, current[1]]
                          ]  # possible orthogonal movement spaces

                # if piece is a General check that movement is within castle walls
                if piece.get_code() == "G":
                    if piece.get_player() == "RED":
                        if move_to in castle and move_to in otrho1:
                            i += 1
                            if function != "GENCHECK":
                                self._general_check[1] = move_to  # set new red general location
                        else:
                            return False

                    elif move_to in castle2 and move_to in otrho1:  # if black general
                        i += 1
                        if function != "GENCHECK":
                            self._general_check[0] = move_to  # set new black general location
                    else:
                        return False

                # move piece to next adjacent orthogonal spot based on move_to
                if current[0] == move_to[0] and current != move_to:
                    if current[1] > move_to[1]:
                        current = otrho1[0]
                    else:
                        current = otrho1[1]
                if current[1] == move_to[1] and current != move_to:
                    if current[0] > move_to[0]:
                        current = otrho1[2]
                    else:
                        current = otrho1[3]
                i += 1  # increment move counter
                # check if current spot is off the board
                if current[0] > 9 or current[1] > 8:
                    return False
                # check if current orthogonal spot is occupied and piece not yet at final destination
                check = self._board[current[0]][current[1]]
                if check != "  " and piece.get_code() != "C" and current != move_to:
                    return False
                # check for cannon screen
                if self._board[current[0]][current[1]] != "  ":
                    if piece.get_code() == "C" and current != move_to:
                        cannon_count += 1  # increments cannon's "screen" count

            # check for cannon specifics
            if piece.get_code() == "C":
                # check if cannon has no screen and is trying to move to occupied spot
                if cannon_count != 1 and self._board[current[0]][current[1]] != "  ":
                    return False
                # check if cannon trying to capture, it has a screen
                if cannon_count == 1 and landing == "  ":
                    return False

                if cannon_count > 1:
                    return False

        # piece is a soldier
        if piece.get_code() == "S":
            if piece.get_direction() == "DRY":
                if piece.get_player() == "RED":
                    # soldier is RED and "DRY", only move straight
                    straight = [move_from[0] - 1, move_from[1]]
                    if straight != move_to:
                        return False
                    # if piece is is not crossing the river
                    if move_to[0] > 4:
                        current = move_to
                    elif move_to[0] < 5 and function == "NORMAL":
                        # if piece is being moved across the river, becomes "WET"
                        piece.set_direction("WET")
                        current = move_to
                    # if checking move for stalemate function, ignore setting the direction
                    elif move_to[0] < 5 and function == "STALE":
                        current = move_to
                else:
                    # soldier is BLACK and "DRY", only move straight
                    straight = [move_from[0] + 1, move_from[1]]
                    if straight != move_to:
                        return False
                    if move_to[0] < 5:
                        current = move_to
                    elif move_to[0] > 4 and function == "NORMAL":
                        # if black soldier goes across the river, becomes "WET"
                        piece.set_direction("WET")
                        current = move_to
                    elif move_to[0] > 4 and function == "STALE":
                        current = move_to
            # if piece is "WET" and RED
            elif piece.get_player() == "RED":
                otrho2 = [[current[0], current[1] - 1], [current[0], current[1] + 1],
                          [current[0] - 1, current[1]]
                          ]  # possible orthogonal movements except no backwards
                if move_to not in otrho2:
                    return False
                else:
                    current = move_to
            # if piece is "WET" and BLACK
            elif piece.get_player() == "BLACK":
                otrho2 = [[current[0], current[1] - 1], [current[0], current[1] + 1],
                          [current[0] + 1, current[1]]
                          ]
                if move_to not in otrho2:
                    return False
                else:
                    current = move_to
            if current[0] > 9 or current[1] > 8:
                return False
        # if any piece's current position is not it's intended destination, return False
        if current != move_to:
            return False

        # if using this method with gen_check method, no actual moving of pieces
        if function == "GENCHECK":
            return True

        # moving the piece to its destination and replacing with "  "
        self._board[move_from[0]][move_from[1]] = "  "
        self._board[move_to[0]][move_to[1]] = piece
        # storing a temporary of the piece it landed on/captured
        # this temporary piece is used for clearing moves in make_move and stalemate if move ends up not being valid
        self._temp = landing

        # check that the General's don't see each other
        if self._general_check[0][1] == self._general_check[1][1]:
            column = self._general_check[0][1]
            i = 0
            for row in self._board:
                if row[column] == "  ":
                    i += 1
            if i == 8:
                return self.clear_move(move_from, move_to)
        return True

    def clear_move(self, move_from, move_to):
        """
        Returns a moved piece to it's original location
        :param move_from - piece's original location
        :param move_to - piece's current location
        """
        piece = self._board[move_to[0]][move_to[1]]
        # check if General being reset, if so, reset general location data member
        if piece.get_code() == "G":
            if piece.get_player() == "RED":
                self._general_check[1] = move_from
            elif piece.get_player() == "BLACK":
                self._general_check[0] = move_from
        # move piece to it's original location and restore piece/spot it took
        self._board[move_from[0]][move_from[1]] = piece
        self._board[move_to[0]][move_to[1]] = self._temp
        return False

    def stalemate(self):
        """Determines if a player is in a stalemate or is in checkmate"""
        red_stale_count = 0  # counter for red pieces that can't move
        black_stale_count = 0  # counter for black pieces that can't move
        red_piece_count = 0
        black_piece_count = 0
        # [a,b] represents the current spot/piece being checked on the board
        a = -1  # main index
        b = -1  # main index
        for row in self._board:
            a += 1
            b = -1
            for piece in row:
                # [c,d] represents the current spot being checked on the board for each piece
                # starts at [0,0] and moves to [9,8] for each piece to see if a valid move can be made
                b += 1
                c = 0  # loop index
                d = 0  # loop index
                if piece != "  ":
                    if piece.get_player() == "RED":
                        red_piece_count += 1
                    elif piece.get_player() == "BLACK":
                        black_piece_count += 1
                    current = [a, b]  # piece's current location on the board
                    while c < 10:
                        move_to = [c, d]  # starting at [0,0]...[9,8]
                        # current black/red piece tries to make a move to move_to
                        make_move = self.check_move(current, move_to, "STALE",
                                                    piece.get_player())
                        # valid move was found
                        if make_move:
                            if piece.get_player() == "RED":  # piece trying to move is red
                                gencheck = self.gen_check("BLACK")  # check if black checks red's move
                                if gencheck == "BLACK":  # black checked red's general after move
                                    self.clear_move(current, move_to)  # clear turn and try again
                                elif gencheck == "NONE":  # black did not check red's general
                                    self.clear_move(current, move_to)  # clear move and move to next piece
                                    c = 10
                            elif piece.get_player() == "BLACK":  # piece trying to move is black
                                gencheck2 = self.gen_check("RED")  # check if red checks black's move
                                if gencheck2 == "RED":  # red checked black's general
                                    self.clear_move(current, move_to)  # clear turn, try again
                                elif gencheck2 == "NONE":  # red did not check black's general
                                    self.clear_move(current, move_to)  # clear move and move to next piece
                                    c = 10

                        # if all locations for piece have been tried, increment stale counter
                        if c == 9 and d == 8:
                            if piece.get_player() == "RED":
                                red_stale_count += 1
                            elif piece.get_player() == "BLACK":
                                black_stale_count += 1
                        d += 1
                        if d == 10:
                            d = 0
                            c += 1
        if black_stale_count == black_piece_count:
            return "BLACK"  # black is stalemated/lost
        elif red_stale_count == red_piece_count:
            return "RED"  # red is stalemated/lost
        else:
            return "NONE"  # no stalemate/checkmate

    def gen_check(self, player):
        """
        checks if a player is in check
        :param player - 'RED' or 'BLACK
        """
        a = -1  # main index
        b = -1  # main index
        for row in self._board:
            # [a,b] represents the current spot/piece being checked on the board
            a += 1
            b = -1
            for piece in row:
                b += 1
                if piece != "  ":
                    if piece.get_player() == player:
                        current = [a, b]
                        if player == "RED":
                            make_move = self.check_move(current, self._general_check[0], "GENCHECK",
                                                        player)  # see if red checks black general
                            if make_move:
                                return "RED"  # black general was captured

                        if player == "BLACK":
                            make_move = self.check_move(current, self._general_check[1], "GENCHECK",
                                                        player)  # see if black checks red general
                            if make_move:
                                return "BLACK"  # red general was captured

        return "NONE"  # general is not in check for player


class Piece:
    """
    Represents a game piece with methods to get a piece's particular attributes.
    """

    def __init__(self, player, code, direction, spaces):
        """
        Constructs a game Piece object with attributes of piece's player, code/symbol, direction, and spaces to move.
        """
        self._player = player
        self._code = code
        self._direction = direction
        self._spaces = spaces

    def get_player(self):
        """returns a piece's player"""
        return self._player

    def get_code(self):
        """returns a piece's code/symbol"""
        return self._code

    def get_direction(self):
        """returns a piece's movement type"""
        return self._direction

    def get_spaces(self):
        """returns how many spaces a piece can move"""
        return self._spaces

    def set_direction(self, new):
        """changes piece's direction type"""
        self._direction = new


class General(Piece):
    """represents a general piece"""

    def __init__(self, player, code="G", direction="ORTHO", spaces=1):
        """constructs a General object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Advisor(Piece):
    """represents an advisor piece"""

    def __init__(self, player, code="A", direction="DIAG", spaces=1):
        """constructs an Advisor object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Elephant(Piece):
    """represents an elephant piece"""

    def __init__(self, player, code="E", direction="DIAG", spaces=2):
        """constructs an Elephant object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Horse(Piece):
    """represents a horse piece"""

    def __init__(self, player, code="H", direction="L", spaces=3):
        """constructs a Horse piece object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Chariot(Piece):
    """represents a chariot piece"""

    def __init__(self, player, code="R", direction="ORTHO", spaces=9):
        """constructs a chariot piece object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Cannon(Piece):
    """represents a cannon piece"""

    def __init__(self, player, code="C", direction="ORTHO", spaces=9):
        """constructs a cannon piece object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)


class Soldier(Piece):
    """represents a soldier piece"""

    def __init__(self, player, code="S", direction="DRY", spaces=1):
        """constructs a cannon piece object with methods inherited from the Piece class"""
        super().__init__(player, code, direction, spaces)

