#!/bin/bash

# 检查是否传入了两个文件名
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file1> <file2>"
    exit 1
fi

# 获取文件名，但是不带扩展名
filename1=$(basename "$1" | cut -d. -f1)
filename2=$(basename "$2" | cut -d. -f1)

# 合并文件名
merged_filename="${filename1}_${filename2}.txt"

# 使用cat合并文件并保存到新文件
cat "$1" "$2" > "${merged_filename}.temp"




sort -k1,1 -k2,2n -k3,3n  "${merged_filename}.temp" | \
awk '
BEGIN {OFS="\t"} 
{
  key=$1"_"$2"_"$3; 
  chr[key]=$1;
  start[key]=$2; 
  end[key]=$3; 
  value5[key]+=$5; 
  value6[key]+=$6;
} 
END {
  for (i in start) {
    split(i, arr, "_");
    print arr[1], arr[2], arr[3], "0.00", value5[i], value6[i], "CpG";
  }
}' | sort -k1,1 -k2,2n -k3,3n > "$merged_filename"

rm "${merged_filename}.temp"
