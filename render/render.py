from game.game import TicTacToe

class Renderer:

    def __init__(self):
        pass

    def render(game: TicTacToe):
        print(game.__board[0],game.__board[1],game.__board[2])
        
        print(game.__board[3],game.__board[4],game.__board[5])
        
        print(game.__board[6],game.__board[7],game.__board[8])