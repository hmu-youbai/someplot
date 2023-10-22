from scipy import stats
import argparse
import pandas as pd


def parse_columns(s):
    return [int(x) for x in s.split(',')]







def get_input(my_file,mode,col):
    ucol1 = parse_columns(col)
    data = []
    with open(my_file, 'r') as file:
        for line in file:
            line=line.strip().split()
            if  (not line[ucol1[1]].isdigit()) or (not  line[ucol1[2]].replace(".", "", 1).isdigit()):
                continue



            if mode==1:
                data.append((line[ucol1[0]],int(line[ucol1[1]]),int(line[ucol1[2]]),int(line[ucol1[3]])))
            elif mode==2:
                data.append((line[ucol1[0]], int(line[ucol1[1]]), float(line[ucol1[2]]), int(line[ucol1[3]])))
            elif mode==3:
                data.append((line[ucol1[0]], int(line[ucol1[1]]), float(line[ucol1[2]])))

    if mode==1:
        df_A = pd.DataFrame(data, columns=['chr', 'pos', 'mod', 'unmod'])
        df_A['level'] = df_A['mod'] / (df_A['mod'] + df_A['unmod'])
        df_A['deep']=df_A['mod']+df_A['unmod']

    elif mode==2:
        df_A = pd.DataFrame(data, columns=['chr', 'pos', 'level', 'deep'])

    else :
        df_A = pd.DataFrame(data, columns=['chr', 'pos', 'level'])
        df_A['deep'] = 100


    if  df_A['level'].max() > 1:
        df_A.loc[:, 'level'] = df_A['level'] / 100


    return df_A





#   python3 cor.py -bin 10000 -1 f1.bed -2 f2.bed -m1 1 -c1 0,1,4,5  -m2 1 -c2 0,1,4,5
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-1",
        "--f1",
        help="Input filename for f1.",
    )
    parser.add_argument(
        "-2",
        "--f2",
        help="Input filename for f2.",
    )
    parser.add_argument(
        "-c1",
        "--col1",
        default="0,1,4,5",
        help="columns to read (0-based index)"
    )
    parser.add_argument(
        "-c2",
        "--col2",
        default="0,1,4,5",
        help="columns to read (0-based index)"
    )


    parser.add_argument(
        "-m1",
        "--mode1",
        help="甲基化数据格式file1",
        default=1,
        type=int
    )

    parser.add_argument(
        "-m2",
        "--mode2",
        help="甲基化数据格式file2",
        default=1,
        type=int
    )



    parser.add_argument(
        "-bin",
        "--bin",
        help="区间大小",
        default=100000,
        type=int
    )
    args = parser.parse_args()

    df_A = get_input(args.f1,args.mode1,args.col1)
    df_B = get_input(args.f2, args.mode2, args.col2)


    print("bin大小："+str(args.bin))
    df_intersection = pd.merge(df_A, df_B, on=['chr', 'pos'])

    final_list=[]


    for cov1 in range(1,10):
        for cov2 in range(1,10):
            filtered_df = df_intersection[(df_intersection['deep_x'] >= cov1) & (df_intersection['deep_y'] >= cov2)].copy()

            len1 = len(filtered_df)
            if len1<100:
                continue
            filtered_df.loc[:, 'bin'] = filtered_df['pos'] // args.bin
            df_sum = filtered_df.groupby(['chr', 'bin']).agg({'level_x': 'mean', 'level_y': 'mean'})
            len2 = len(df_sum)
            r, p_value = stats.pearsonr(df_sum['level_x'], df_sum['level_y'])
            final_list.append(f"{r:.2f}")

            print(f"coverage1:{cov1},coverage2:{cov2},r值: {r:.2f}, p值: {p_value:.2e},位点数:{len1},{len2}")





    print(" ".join(final_list))




if __name__ == '__main__':
    main()
