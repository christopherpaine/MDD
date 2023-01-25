import math
import pandas as pd
pd.options.mode.chained_assignment = None

# add print statements to test this function

def calculate_product(df):
    # =F16*G16
    product_values = []
    for index, row in df.iterrows():
        val = row['n_p_x'] * row['discounted payment']
        product_values.append(val)
    df['product'] = product_values
    result = df['product'].sum()
    result = round(result, 7)
    return result


def calculate_discounted_payment(df, param):
    # =D5 * (1 +$M$2) ^ -C5
    D5 = 1
    discount_value = []
    for index, row in df.iterrows():
        val = D5 * (1 + param)
        val = pow(val, -(index + 1))
        val = round(val, 12)
        discount_value.append(val)
    df['discounted payment'] = discount_value
    return calculate_product(df)


def calculate_n_p_x(df, param):
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
    return calculate_discounted_payment(df, param)


def calculate_p_x(df, param):
    col_p_x = []
    for index, row in df.iterrows():
        # =(1-B5)
        val = row['Rates']
        column_value = (1-val)
        column_value = round(column_value, 4)
        col_p_x.append(column_value)
    df['p_x'] = col_p_x
    return calculate_n_p_x(df, param)


def calculate_product_value(df, param):
    return calculate_p_x(df, param)
