from game.game import TicTacToe
import game
import asyncio
import random
import math

class AIPlayer:
    __game: TicTacToe
    __invertMinimax: False

    def __init__(self, game: TicTacToe):
        self.__game = game
        self.__invertMinimax = False

        # Decide whether or not to play like an idiot
        if math.floor(random.random() * 15) == 0:
            self.__invertMinimax = True
            print("\n[AIPlayer] Computer is going to play really bad\n")

        print("[AIPlayer] initialized")

    async def run(self):
        print("[AIPlayer] enter main loop")

        while True:
            # first, block until its our turn
            await self.__game.awaitTurn(False)

            if self.__game.getGameState() != 0:
                print("[AIPlayer] game state is not in progress, exiting")
                self.__game.passTurn()
                return

            print("[AIPlayer] begin turn")
            # next, generate a turn and execute it
            self.__game.placeSymbol(self.__computeTurn())

            # finally, check the game state and process it
            state = self.__game.getGameState()
            # ... react to the state here
            print("[AIPlayer] end turn")
            self.__game.passTurn()
        pass

    def __computeTurn(self) -> int:
        # returns the index of the cell that the AI wants to place a symbol in
        print("Please wait, computing move...")
        (move, score) = self.__findMove(self.__game.getBoard(), len(self.__findPossibleMoves(self.__game.getBoard())), self.__game.getTurn())
        return move

    # utilizes the minimax algoritm to find the best move and returns the move (index of the list)
    def __findMove(self, board, depth, isMaximizing) -> (int, int):
        # return the evaluation of the current board if we are at the frontier or the current board is a win/draw
        if depth == 0 or self.__evaluate(board) != 0:
            return (board, self.__evaluate(board))

        # if this iteration is maximizing the evaluation
        if isMaximizing ^ self.__invertMinimax:
            # prepare the movelist
            bestMoves = []
            bestScore = -69
            # generate the children of the current node and iterate over them
            for child in self.__findPossibleMoves(board):
                # recursively find the maximum within the children of this node
                (void, score) = self.__findMove(self.__makeMove(board, child, isMaximizing ^ self.__invertMinimax), depth - 1, False)
                
                if score >= bestScore:
                    if score > bestScore:
                        bestScore = score
                        bestMoves.clear()
                    bestMoves.append(child)
            # yield a random move of the moves tied for bestmove, to decrease deteminism
            return (random.choice(bestMoves), bestScore)
        
        # if this iteration is maximizing the evaluation
        else:
            # prepare the movelist
            bestMoves = []
            bestScore = 69
            # generate the children of the current node and iterate over them
            for child in self.__findPossibleMoves(board):
                # recursively find the minimum within the children of this node
                (void, score) = self.__findMove(self.__makeMove(board, child, isMaximizing ^ self.__invertMinimax), depth - 1, True)

                if score <= bestScore:
                    if score < bestScore:
                        bestScore = score
                        bestMoves.clear()
                    bestMoves.append(child)
            
            # yield a random move of the moves tied for bestmove, to decrease deteminism
            return (random.choice(bestMoves), bestScore)

    # returns all possible child moves from the specified board
    def __findPossibleMoves(self, board):
        possibleMoves = []
        for position in range(len(board)):
            if board[position] == "":
                possibleMoves.append(position)
        return possibleMoves

    # plays the specified move on the board
    def __makeMove(self, board, position, isMaximizing):
        boardWithMove = board.copy()
        boardWithMove[position] = 'X' if isMaximizing else 'O'
        return boardWithMove

    # returns the evaluation of the specified board
    def __evaluate(self, board) -> int:
        evaluation = self.__game.evaluate(board)

        if evaluation == 1:
            return 69
        if evaluation == 2:
            return -69
        return 0

