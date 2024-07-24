library(ggplot2)
library(jsonlite)

args <- commandArgs(trailingOnly = TRUE)
input_json <- fromJSON(file("stdin"))

data <- input_json$data
image_width <- as.numeric(input_json$image_width)
image_height <- as.numeric(input_json$image_height)
title <- input_json$title
x_label <- input_json$x_label
y_label <- input_json$y_label
show_legend <- as.logical(input_json$show_legend)
x_rotation <- as.numeric(input_json$x_rotation)

# Read data into a data frame
df <- read.table(text = data, header = TRUE, sep = "\t")

# Create the stacked bar plot
p <- ggplot(df, aes(x = ID, y = Expr, fill = Gene)) +
  geom_bar(stat = "identity") +
  labs(title = title, x = x_label, y = y_label, fill = if (show_legend) "Gene" else NULL) +
  theme(axis.text.x = element_text(angle = x_rotation, hjust = 1))

# Save the plot to a file
ggsave("static/plot.png", plot = p, width = image_width, height = image_height, units = "cm")