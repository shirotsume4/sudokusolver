import pulp

def solve_sudoku(puzzle):
    # 数独のグリッドを定義（1から9までの数字）
    VALS = ROWS = COLS = range(1, 10)

    # 数独問題を解くための線形プログラミングの問題インスタンスを作成
    prob = pulp.LpProblem("Sudoku Problem")

    # 各セルに入る可能性のある数字に対してバイナリ変数を定義（0または1）
    choices = pulp.LpVariable.dicts("Choice", [(val, row, col) for val in VALS for row in ROWS for col in COLS], cat="Binary")
    
    # 数独パズルの初期状態を設定（与えられた数値を固定）
    for row in ROWS:
        for col in COLS:
            if puzzle[row-1][col-1] != 0:  # 0は空欄を意味する
                for val in VALS:
                    if val == puzzle[row-1][col-1]:
                        prob += choices[val, row, col] == 1  # 与えられた数値を固定
                    else:
                        prob += choices[val, row, col] == 0  # 他の数値を排除

    # 数独のルールに従った制約を設定
    for val in VALS:
        # 各行において、各数字が1回だけ現れるように制約を設定
        for row in ROWS:
            prob += pulp.lpSum([choices[val, row, col] for col in COLS]) == 1
        # 各列において、各数字が1回だけ現れるように制約を設定
        for col in COLS:
            prob += pulp.lpSum([choices[val, row, col] for row in ROWS]) == 1
        # 各3x3ボックスにおいて、各数字が1回だけ現れるように制約を設定
        for box_row in range(3):
            for box_col in range(3):
                prob += pulp.lpSum([choices[val, 3*box_row + i, 3*box_col + j] for i in range(1, 4) for j in range(1, 4)]) == 1

    # 各セルには1つの数字のみが入るという制約を設定
    for row in ROWS:
        for col in COLS:
            prob += pulp.lpSum([choices[val, row, col] for val in VALS]) == 1

    # 線形プログラミング問題を解く
    prob.solve()

    # 解決策を取得して整理（数独盤面を作成）
    solution = [[0 for _ in range(9)] for _ in range(9)]
    for val in VALS:
        for row in ROWS:
            for col in COLS:
                if pulp.value(choices[val, row, col]) == 1:
                    solution[row-1][col-1] = val  # 解決策を盤面に反映
    return solution

def show_sudoku(puzzle):
    # 数独の盤面を視覚的に表示する関数
    for r in range(len(puzzle)):
        # 3行ごとに区切り線を表示して盤面を区切る
        if r in [0, 3, 6]:
            print("+-------+-------+-------+")
        for c in range(len(puzzle[r])):
            # 各3列ごとに左境界を表示
            if c in [0, 3, 6]:
                print("| ", end="")
            # セルに数字がある場合は数字を、ない場合は空白を表示
            if puzzle[r][c] != 0:
                print(puzzle[r][c], end=" ")
            else:
                print(end="  ")
            # 行の最後に右境界を表示
            if c == 8:
                print("|")
    # 最後に底の境界線を表示
    print("+-------+-------+-------+")

# 数独パズルの例（0は空欄を意味する）
puzzle = [
    # ここに数独パズルの初期状態が格納される
    [7, 2, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 9, 5, 3, 7, 0, 8, 2],
    [5, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 2, 0, 5, 6, 3],
    [3, 5, 0, 6, 8, 0, 1, 0, 9],
    [9, 7, 6, 0, 0, 0, 4, 2, 0],
    [6, 0, 7, 2, 4, 1, 8, 3, 0],
    [0, 0, 5, 9, 7, 8, 0, 4, 0],
    [2, 8, 0, 3, 6, 5, 9, 1, 0]
]

solution = solve_sudoku(puzzle)
# 問題と解答を表示

print("問題:")
show_sudoku(puzzle)
print("")
print("解答:")
show_sudoku(solution)