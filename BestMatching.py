import time
import random
import pandas as pd
from ortools.graph import pywrapgraph
import csv

def overall_profit_ans(data_s, data_c, n_s, n_c):

    ans = [0] * n_s
    weights = [[0]*(n_c) for _ in range(n_c)]

    #生徒の重みづけ
    for i in range(n_s):
        flag = 0
        for j in range(n_c+1):
            if data_s[i][j] == -1:
                flag = 1
            elif flag == 1:
                weights[i][data_s[i][j]] = "NA"
            else:
                weights[i][data_s[i][j]] = n_s - j

    #企業の重みづけ
    for i in range(n_c):
        flag = 0
        for j in range(n_s+1):
            if data_c[i][j] == -1:
                flag = 1
            elif flag == 1:
                weights[data_c[i][j]][i] = "NA"
            elif weights[data_c[i][j]][i] != "NA":
                weights[data_c[i][j]][i] += n_c - j

    #どこにもマッチング出来ない人の処理
    for index, i in enumerate(weights):
        if len(set(i)) == 1 and i[0] == "NA":
            weights[index] = [-1]*n_c
            ans[index] = -1

    assignment = pywrapgraph.LinearSumAssignment()

    #重みをもとにマッチングの最適化
    for i in range(n_c):
        for j in range(n_c):
            if weights[i][j] != "NA":
                assignment.AddArcWithCost(i, j, weights[i][j])

    #解を探す
    solve_status = assignment.Solve()

    #解が出た場合
    if solve_status == assignment.OPTIMAL:
        for i in range(n_s):
            #マッチングする人のみ企業番号を返す
            if ans[i] != -1:
                ans[i] = assignment.RightMate(i)

        return ans


def main():
    input_file_path = "./InputData/input_"
    output_file_path = "./OutputData/output_"
    pass_list =[["p2s_c1.csv", "p2c_c1.csv"],
                ["p2s_c2.csv", "p2c_c2.csv"],
                ["p2s_c3.csv", "p2c_c3.csv"]]
    output_list = ["p2_c1.csv",
                   "p2_c2.csv",
                   "p2_c3.csv",]

    for index, i in enumerate(pass_list):
        strat_time = time.time()
        data_s = pd.read_csv(input_file_path + i[0], header=None).values.tolist()
        data_c = pd.read_csv(input_file_path + i[1], header=None).values.tolist()
        n_s = len(data_s)
        n_c = len(data_c)

        ans = overall_profit_ans(data_s, data_c, n_s, n_c)
        # print(index,ans)
        # print("経過時間 : ", time.time() - strat_time, "秒")

        if ans != None:
            with open(output_file_path + output_list[index], 'w') as csv_file:
                csv.writer(csv_file).writerow(ans)
        else:
            break

if __name__ == '__main__':
    main()
