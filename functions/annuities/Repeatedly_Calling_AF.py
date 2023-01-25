import pandas as pd
from Annuity_Function import calculate_product_value


def main():
    # Reading dataframe from csv
    df = pd.read_csv("function.csv")
    # Get the size of dataframe
    df_size = len(df)
    # Param value
    param = 0.04
    # Result and age arraylist
    final_results_array = []
    final_age_x_array = []
    final_dataframe = pd.DataFrame(columns=['Age x','Result'])
    # Uncomment below for loop to skip last row result
    # for index in range(df_size - 1):
    for index in range(df_size):
        # Get the dataframe from index to end of dataframe
        dataframe = df[index:df_size]
        dataframe = dataframe.reset_index()
        age_x = dataframe['Age x'].iloc[0]
        # Get result from Annuity_Function.py
        result = calculate_product_value(dataframe,param)
        final_results_array.append(result)
        final_age_x_array.append(age_x)
        print('Age x = ', age_x, " ", "Result = ", result)

    final_dataframe['Age x'] = final_age_x_array
    final_dataframe['Result'] = final_results_array

    # Printing final dataframe
    # print(final_dataframe)


if __name__ == "__main__":
    main()

#the first few results will look as follows:

#Age x      result
#17			22.363192005021
#18			22.2756473
#19			22.18044237
