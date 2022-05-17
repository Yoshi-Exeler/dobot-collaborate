from game.game import TicTacToe
import game
import asyncio
import random


class AIPlayer:
    __game: TicTacToe

    def __init__(self, game: TicTacToe):
        self.__game = game
        print("[AIPlayer] initialized")
        pass

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

    # Utilizes the minimax to find the best move and returns the move (index of the list)
    def __findMove(self, board, depth, isMaximizing) -> (int, int):

        if depth == 0 or self.__evaluate(board) != 0:
            return (board, self.__evaluate(board))

        if isMaximizing:
            # Human is maximizing player
            bestMoves = []
            bestScore = -69
            for child in self.__findPossibleMoves(board):
                (void, score) = self.__findMove(self.__makeMove(board, child, isMaximizing), depth - 1, False)

                if score >= bestScore:
                    if score > bestScore:
                        bestScore = score
                        bestMoves.clear()
                    bestMoves.append(child)

            return (random.choice(bestMoves), bestScore)

        else:
            # AI is minimizing player
            bestMoves = []
            bestScore = 69
            for child in self.__findPossibleMoves(board):
                (void, score) = self.__findMove(self.__makeMove(board, child, isMaximizing), depth - 1, True)

                if score <= bestScore:
                    if score < bestScore:
                        bestScore = score
                        bestMoves.clear()
                    bestMoves.append(child)

            return (random.choice(bestMoves), bestScore)

    def __findPossibleMoves(self, board):
        possibleMoves = []
        for position in range(len(board)):
            if board[position] == "":
                possibleMoves.append(position)
        return possibleMoves

    def __makeMove(self, board, position, isMaximizing):
        boardWithMove = board.copy()
        boardWithMove[position] = 'X' if isMaximizing else 'O'
        return boardWithMove

    def __evaluate(self, board) -> int:
        evaluation = self.__game.evaluate(board)

        if evaluation == 1:
            return 69
        if evaluation == 2:
            return -69
        return 0

