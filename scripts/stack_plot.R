args <- commandArgs(trailingOnly=TRUE)
data_file <- args[1]
image_width <- as.numeric(args[2])
image_height <- as.numeric(args[3])

library(ggplot2)

# Read the data
data <- read.table(data_file, header=TRUE, sep="\t")

# Pivot the data for plotting
library(tidyr)
data_pivot <- pivot_wider(data, names_from = Gene, values_from = Expr)

# Convert the data to long format for ggplot
data_long <- pivot_longer(data_pivot, cols = -ID, names_to = "Gene", values_to = "Expr")

# Create the stacked bar plot
p <- ggplot(data_long, aes(x = ID, y = Expr, fill = Gene)) +
    geom_bar(stat = "identity") +
    labs(x = "ID", y = "Expression Level", title = "Stacked Bar Plot") + 
    theme_minimal() +
    theme(
        panel.grid = element_blank(),  # 去掉背景格子
        axis.line = element_line(colour = "black"),  # 显示坐标轴
        axis.ticks = element_line(colour = "black"),  # 显示刻度线
        axis.text.x = element_text(angle = 45, hjust = 1, size = 5, face = "bold")
        )
    

# Save the plot to a file
ggsave("static/plot.png", plot = p, width = image_width, height = image_height, units = "cm")