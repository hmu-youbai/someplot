import sys
import os

def merge_and_process(file1, file2):
    filename1 = os.path.basename(file1).split('.')[0]
    filename2 = os.path.basename(file2).split('.')[0]

    merged_filename = f"{filename1}_{filename2}.bed"
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines = f1.readlines() + f2.readlines()

    data = {}
    for line in lines:
        fields = line.strip().split()
        key = (fields[0], int(fields[1]), int(fields[2]))


        if key not in data:
            data[key] = [0, 0, 0, 0]

        data[key][0] += float(fields[3])
        data[key][1] += int(fields[4])
        data[key][2] += int(fields[5])
        data[key][3] += 1




    with open(merged_filename, 'w') as out:
        for key in sorted(data.keys(), key=lambda x: (x[0], x[1], x[2])):
            out.write(f"{key[0]}\t{key[1]}\t{key[2]}\t{((data[key][0])/data[key][3]):.4f}\t{data[key][1]}\t{data[key][2]}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <file1> <file2>")
        sys.exit(1)
    merge_and_process(sys.argv[1], sys.argv[2])
