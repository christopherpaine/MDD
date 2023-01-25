import math
import pandas as pd

# add print statements to test this function

def calculate_product(df):
    # =F16*G16
    product_values = []
    for index, row in df.iterrows():
        val = row['n_p_x'] * row['discounted payment']
        product_values.append(val)
    df['product'] = product_values
    result = df['product'].sum()
    result = round(result, 12)
    print(result)
    return result


def calculate_discounted_payment(df, param2):
    # =D5 * (1 +$M$2) ^ -C5
    D5 = 1
    discount_value = []
    for index, row in df.iterrows():
        val = D5 * (1 + param2)
        val = pow(val, -(index + 1))
        val = round(val, 12)
        discount_value.append(val)
    df['discounted payment'] = discount_value
    calculate_product(df)


def calculate_n_p_x(df, param2):
    n_p_x_col = []
    p_x_values = df['p_x'].values
    length = len(p_x_values)
    for i in range(0,length):
        product_list = []
        for j in range(0,i + 1):
            product_list.append(p_x_values[j])
        if len(product_list) == 0:
            continue
        n_p_x = math.prod(product_list)
        n_p_x = round(n_p_x, 9)
        n_p_x_col.append(n_p_x)
    df['n_p_x'] = n_p_x_col
    calculate_discounted_payment(df, param2)


def calculate_p_x(df, param2):
    col_p_x = []
    for index, row in df.iterrows():
        # =(1-B5)
        val = row['Durations 2+']
        column_value = (1-val)
        column_value = round(column_value, 4)
        col_p_x.append(column_value)
    df['p_x'] = col_p_x
    calculate_n_p_x(df, param2)


def calculate_product_value(df, param2):
    calculate_p_x(df, param2)


def main():
    # Param 2 value

    #THIS SHOULD BE A PARAMETER AND NOT HARDCODED
    param2 = 0.04
    # Read dataframe from csv

    #THIS SHOULD BE A PARAMETER AND NOT HARDCODED
    df = pd.read_csv(".\\function.csv")




    # Call this function to get final result
    calculate_product_value(df, param2)
    print(df)
    


if __name__ == "__main__":
    main()