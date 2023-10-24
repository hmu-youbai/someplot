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
        "-cov1",
        "--coverage1",
        help="甲基化数据格式file1",
        default=1,
        type=int
    )

    parser.add_argument(
        "-cov2",
        "--coverage2",
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

    filtered_df = df_intersection[(df_intersection['deep_x'] >= args.coverage1) & (df_intersection['deep_y'] >= args.coverage2)].copy()

    filtered_df.loc[:, 'bin'] = filtered_df['pos'] // args.bin
    df_sum = filtered_df.groupby(['chr', 'bin']).agg({'level_x': 'mean', 'level_y': 'mean'})

    output=args.f1+"_and_"+args.f2
    output=output.replace(".","_") + ".csv"

    df_sum[['level_x', 'level_y']].to_csv(output, sep='\t', index=False)









if __name__ == '__main__':
    main()
