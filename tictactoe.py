print("Игра Крестики-нолики")
XO_input = ['X', 'O']
board = list(range(1, 10))


def draw_board(board):
    print('_' * 10)
    for i in range(3):
        print(board[i * 3], '|', board[1 + i * 3], '|', board[2 + i * 3])
        print('_' * 10)


def win(board):
    win_coord = ((0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 1, 2), (3, 4, 5), (6, 7, 8))
    for i in win_coord:
        if board[i[0]] == board[i[1]] == board[i[2]]:
            print(f'Выиграли {board[i[0]]}')
            return True
    return False


def game(XO):
    correct = False
    while not correct:
        move = input(f"В какую ячейку поставить {XO}? ")
        try:
            move = int(move)
        except:
            print('Неверный номер ячейки, введите цифру от 1 до 9.')
            continue
        if (move >= 1) and (move <= 9):
            if board[move - 1] != XO_input[0] and board[move - 1] != XO_input[1]:
                board[move - 1] = XO
                correct = True
            else:
                print('Эта ячейка уже занята, попробуйте ввод еще раз.')
        else:
            print('Неверный номер ячейки, попробуйте еще раз.')


def main():
    current_player = input("""Введите X, если первыми будут ходить крестики, 
                         O - если первыми будут ходить нолики: """).upper()

    if current_player not in XO_input:
        print('Некорректный ввод')
        return

    step = 0
    draw_board(board)

    while step < 9:
        game(current_player)
        draw_board(board)
        if win(board):
            return

        step += 1
        current_player = XO_input[(XO_input.index(current_player) + 1) % 2]  # Переключаем игроков

    print('Ничья')


if __name__ == "__main__":
    main()