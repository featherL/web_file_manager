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

df <- read.table(data_file, header = TRUE, sep = "\t")

p <- ggplot(df, aes(x = Gene, y = Expr, fill = Group)) +
    geom_boxplot() +
    labs(title = title, x = x_label, y = y_label) +
    theme(axis.text.x = element_text(angle = x_rotation, hjust = 1))

if (!show_legend) {
    p <- p + theme(legend.position = "none")
}

ggsave("static/plot.png", plot = p, width = image_width / 2.54, height = image_height / 2.54)