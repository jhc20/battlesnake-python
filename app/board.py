def fillBoard(height, width, snakes, food, li):
    board = []
    for i in xrange(height):
        board.append([])
        for j in xrange(width):
            board[i].append(0)
    for snake in snakes:
        if snake.snake_id == li:
            if len(snake.coord) == 0:
                continue
            for coord in snake.coords:
                board[coord[0]][coord[1]] = 1
            board[snake.coords[-1][0]][board[snake.coords[-1][1]]] = 0
        else:
            if len(snake.coord) == 0:
                continue
            for coord in snake.coords:
                board[coord[0], coord[1]] = 2
            board[snake.coords[-1][0]][board[snake.coords[-1][1]]] = 0
    for coord in food:
        board[coords[0]][coords[1]] = 3
    
    print(board)
    return board