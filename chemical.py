from pulp import LpMaximize, LpProblem, LpVariable, value

M = LpProblem(sense=LpMaximize)  #数理モデル．今回は最大化なのでLpMaximize
a = LpVariable("a")  #変数a
b = LpVariable("b")  #変数b

#制約条件の追加
M += 48 * a + 35 * b <= 8400
M += 36 * a + 49 * b <= 10800
M += a >= 0
M += b >= 0

#目的関数の追加
M += 1000 * a + 1000 * b
M.solve()

print(M.objective.value())  #目的関数の値を確認
print(value(a), value(b))  #変数a,bの値を確認