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
library(reshape2)

df <- read.table(data_file, header = TRUE, sep = "\t")
df_pivot <- dcast(df, ID ~ Gene, value.var = "Expr")

df_melt <- melt(df_pivot, id.vars = "ID")

p <- ggplot(df_melt, aes(x = variable, y = ID, fill = value)) +
    geom_tile() +
    scale_fill_gradient(low = "white", high = "red") +
    labs(title = title, x = x_label, y = y_label) +
    theme(axis.text.x = element_text(angle = x_rotation, hjust = 1))

if (!show_legend) {
    p <- p + theme(legend.position = "none")
}

ggsave("static/plot.png", plot = p, width = image_width / 2.54, height = image_height / 2.54)