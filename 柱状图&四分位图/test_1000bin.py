import pandas as pd
import argparse



def get_input(my_file):

    data = []
    with open(my_file, 'r') as file:
        for line in file:
            line=line.strip().split()
            if  (not line[1].isdigit()) or (not  line[3].replace(".", "", 1).isdigit()):
                continue

            data.append((line[0],int(line[2]),int(line[4]),int(line[5])))


    df_A = pd.DataFrame(data, columns=['chr', 'pos', 'mod', 'unmod'])
    df_A['level'] = df_A['mod'] / (df_A['mod'] + df_A['unmod'])
    df_A['deep']=df_A['mod']+df_A['unmod']

    if  df_A['level'].max() > 1:
        df_A.loc[:, 'level'] = df_A['level'] / 100


    return df_A



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process bed file.")
    parser.add_argument("filename", help="Input bed file.")
    parser.add_argument("--bin", type=int, default=1000, help="Bin size.")
    args = parser.parse_args()

    df_A=get_input(args.filename)
    df_A['bin'] = df_A['pos'] // args.bin

    df_result = df_A.groupby(['chr', 'bin']).agg({'level': 'mean', 'deep': 'sum'}).reset_index()


    for threshold in range(1, 10):
        filtered_df = df_result[df_result['deep'] >= threshold]
        avg_level = filtered_df['level'].mean()
        count = len(filtered_df)

        print(f"Threshold: {threshold}, Average Level: {avg_level}, Number of Rows: {count}")



