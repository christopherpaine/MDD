import pandas as pd

def calculate_power_value(df, interest_rate):
    #create empty list called col3
    col3 = []

    for index, row in df.iterrows():
        #calculate (1+i)
        val1 = 1 + interest_rate
        #calculate a column of discount factors
        column_value = pow(val1, -(index + 1))
        #keep things to a health 6 decimal places
        column_value = round(column_value, 6)
        #add the newly calculated value to our col3 list
        col3.append(column_value)

    #add column of discount factors to our supplied dataframe of mortality rates
    df['col3'] = col3
    
    #calculate product of product 
    col4 = calculate_final_value(df)
    df['col4'] = col4
    final_result = df['col4'].sum()
    final_result = round(final_result, 5)
    print(final_result)
    return col3


def calculate_final_value(df):
    col4 = []
    for index, row in df.iterrows():
        print(index)
        # =G4*(1-E4)
        column_value = row['col3'] * (1-row['col2'])
        column_value = round(column_value, 6)
        col4.append(column_value)
    return col4


def main():
    # Param 2 value
    interest_rate = 0.05
    # Read dataframe from csv
    df = pd.read_csv(".\\power_func.csv")

    # Call this function to get final result
    calculate_power_value(df, interest_rate)


if __name__ == "__main__":
    main()