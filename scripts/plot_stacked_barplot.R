args <- commandArgs(trailingOnly = TRUE)
data_file <- args[1]
image_width <- as.numeric(args[2])
image_height <- as.numeric(args[3])
title <- args[4]
x_label <- args[5]
y_label <- args[6]
show_legend <- as.logical(args[7])
x_rotation <- as.numeric(args[8])

library(ggplot2)

data <- read.table(data_file, header = TRUE, sep = "\t")

# Pivot the data for plotting
library(tidyr)
data_pivot <- pivot_wider(data, names_from = Gene, values_from = Expr)

# Convert the data to long format for ggplot
data_long <- pivot_longer(data_pivot, cols = -ID, names_to = "Gene", values_to = "Expr")


p <- ggplot(data_long, aes(x = ID, y = Expr, fill = Gene)) +
    geom_bar(stat = "identity") +
    labs(title = title, x = x_label, y = y_label) +
    theme(axis.text.x = element_text(angle = x_rotation, hjust = 1))

if (!show_legend) {
    p <- p + theme(legend.position = "none")
}

ggsave("static/plot.png", plot = p, width = image_width / 2.54, height = image_height / 2.54)