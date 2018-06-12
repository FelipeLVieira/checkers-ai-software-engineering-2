from AI import *

def test_heuristic1():
    testBoard = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x: x == 0
    
    board = Board.Board(testBoard)
    assert(heuristicEvaluation(heuristic(board, RED, False, 0)))

def test_heuristic2():
    testBoard = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "# # # # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x: x > 0
    
    board = Board.Board(testBoard)
    assert(heuristicEvaluation(heuristic(board, RED, False, 0)))

def test_heuristic3():
    testBoard = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r# #r#r",
            " # # # #",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x: x < 0
    
    board = Board.Board(testBoard)
    assert(heuristicEvaluation(heuristic(board, RED, False, 0)))

def test_heuristic4():
    testBoard = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "# # # # ",
            "w#w#W#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x: x < 0
    
    board = Board.Board(testBoard)
    assert(heuristicEvaluation(heuristic(board, RED, False, 0)))

def test_heuristic5():
    testBoard = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#R#r#r",
            " # # # #",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x: x > 0
    
    board = Board.Board(testBoard)
    assert(heuristicEvaluation(heuristic(board, RED, False, 0)))

def test_heuristic6():
    testBoard1 = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "#w# # # ",
            "w# #w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    testBoard2 = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r#r#r",
            " # # # #",
            "# # #w# ",
            "w#w# #w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x, y: x == y
    
    board1 = Board.Board(testBoard1)
    board2 = Board.Board(testBoard2)
    assert(heuristicEvaluation(
            heuristic(board1, RED, False, 0),
            heuristic(board2, RED, False, 0)))

def test_heuristic7():
    testBoard1 = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r#r# #r",
            " # # #r#",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    testBoard2 = [
            "#r#r#r#r",
            "r#r#r#r#",
            "#r# #r#r",
            " #r# # #",
            "# # # # ",
            "w#w#w#w#",
            "#w#w#w#w",
            "w#w#w#w#"
            ]
    heuristicEvaluation = lambda x, y: x == y
    
    board1 = Board.Board(testBoard1)
    board2 = Board.Board(testBoard2)
    assert(heuristicEvaluation(
            heuristic(board1, RED, False, 0),
            heuristic(board2, RED, False, 0)))

