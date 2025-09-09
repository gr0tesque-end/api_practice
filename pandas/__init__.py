import pandas as pd
import numpy as np
import string

def generate_random_matrix():
    numbers = np.random.permutation(np.arange(1, 101))
    df = pd.DataFrame(
        numbers.reshape(10, 10),
        columns=[f"Column {i}" for i in range(10)]
    )
    df.to_csv("random_numbers.csv", index=False)
    
if __name__ == "__main__":
    generate_random_matrix()
    df = pd.read_csv("random_numbers.csv")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    print("Primary DataFrame:")
    print(df, "\n")

    df_sums = df.copy()

    df_sums["Sum of row"] = df_sums.sum(axis=1)

    col_sums = df_sums.sum(axis=0)
    col_sums["Sum of row"] = col_sums[:-1].sum()
    df_sums.loc["Sum of column"] = col_sums

    print("DataFrame with sums:")
    print(df_sums, "\n")

    multiples_of_5 = np.argwhere(df.values % 5 == 0)
    print("Divisible by 5:")
    for r, c in multiples_of_5:
        print(f"Number {df.iloc[r, c]} -> Row {r}, Column {c}")
    print()

    pos_42 = np.argwhere(df.values == 42)
    if pos_42.size > 0:
        r, c = pos_42[0]
        print(f"Number 42 was found in Row {r}, Column {c}\n")

    sorted_numbers = np.sort(df.values.flatten())
    df_sorted = pd.DataFrame(
        sorted_numbers.reshape(10, 10),
        columns=[f"Column {i}" for i in range(10)]
    )
    print("Sorted DataFrame:")
    print(df_sorted, "\n")

    df_sorted.to_excel("sorted_numbers.xlsx", index=False)

    def number_to_letters(n):
        result = ""
        while n > 0:
            n, r = divmod(n - 1, 26)
            result = chr(97 + r) + result
        return result

    df_letters = df.copy().map(number_to_letters)
    print("DataFrame with letters :")
    print(df_letters, "\n")

    df_letters.to_csv("letters.csv", index=False)
    