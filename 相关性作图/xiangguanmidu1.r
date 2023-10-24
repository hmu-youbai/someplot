# 加载所需的库
library(graphics)

# 读取数据
df <- read.table("GSM4708554_caps_mm9_mESC_CpG_bed_and_0820_0822_txt.csv", header = TRUE, sep = "\t")
x <- df$level_x
y <- df$level_y

# 计算相关性
correlation <- cor(x, y, method = "pearson")
title <- paste("Correlation:", round(correlation, 2))

# 保存图形到PDF文件
pdf("smoothScatter_example.pdf")

# 绘制平滑散点图
smoothScatter(x, y, xlab="level_x", ylab="level_y", main=title, bandwidth = 0.01)

# 关闭PDF设备
dev.off()
