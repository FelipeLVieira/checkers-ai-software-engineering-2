from Board import *

def test_simple():
    boardStart = [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r#r#r",
        " # # # #",
        "# # # # ",
        "w#w#w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (2, 5)
    movement = [[(2, 5), (1, 4)], [(2, 5), (3, 4)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_capture_simple():
    boardStart = [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_capture_enforce():
    boardStart = [
        "#r#r#r#r",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (4, 5)
    movement = []
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_capture_multiple():
    boardStart = [
        "#r#r#r# ",
        "r#r#r#r#",
        "#r#r# #r",
        " # #r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_capture_multiple_enforce():
    boardStart = [
        "#r#r#r# ",
        "r#r#r#r#",
        "# #r# #r",
        " #r#r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_capture_multiple_crosspaths():
    boardStart = [
        "#r# #r# ",
        "r#r#r#r#",
        "# #r# #r",
        " #r#r# #",
        "# #w# # ",
        "w# #w#w#",
        "#w#w#w#w",
        "w#w#w#w#"
    ]
    selectedPiece = (3, 4)
    movement = [
        [(3, 4), (4, 3), (5, 2), (4, 1),
         (3, 0), (2, 1), (1, 2), (2, 3), (3, 4)],
        [(3, 4), (2, 3), (1, 2), (2, 1),
         (3, 0), (4, 1), (5, 2), (4, 3), (3, 4)],
        [(3, 4), (2, 3), (1, 2), (2, 1),
         (3, 0), (4, 1), (5, 2), (6, 1), (7, 0)]
    ]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_king_move():
    boardStart = [
        "# # # #r",
        " # # # #",
        "# # # # ",
        " # # # #",
        "# #W# # ",
        " # # # #",
        "#w# # # ",
        " # # # #"
    ]
    selectedPiece = (3, 4)
    movement = [
        [(3, 4), (2, 5)],
        [(3, 4), (4, 5)],
        [(3, 4), (4, 5), (5, 6)],
        [(3, 4), (4, 5), (5, 6), (6, 7)],
        [(3, 4), (2, 3)],
        [(3, 4), (2, 3), (1, 2)],
        [(3, 4), (2, 3), (1, 2), (0, 1)],
        [(3, 4), (4, 3)],
        [(3, 4), (4, 3), (5, 2)],
        [(3, 4), (4, 3), (5, 2), (6, 1)]
    ]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement


def test_king_capture():
    boardStart = [
        "#R#R#R# ",
        " # # # #",
        "# # #R# ",
        " # # # #",
        "# #W#W# ",
        " # # # #",
        "# # # # ",
        " # #W#W#"
    ]
    selectedPiece = (3, 4)
    movement = [[(3, 4), (4, 3), (5, 2), (6, 1)], [(3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]]
    board = Board(boardStart)
    result = board.getLegalMoves(selectedPiece)
    assert len(result) == len(movement)
    for move in result:
        assert move in movement
