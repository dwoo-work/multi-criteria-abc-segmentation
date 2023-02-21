
############################
### PART 1 - PREPARATION ###
############################

# Ensure that all the necessary libraries are loaded and available for use in this project.

required_libraries <- c("tidyverse", "inventorize", "dplyr", "ggplot2")
lapply(required_libraries, require, character.only = TRUE)

# Import and clean the CSV dataframe. Use the cleaned data to create a new CSV dataframe.

sales <- read.csv('C:\\Users\\danie\\OneDrive\\Desktop\\archive\\sales_data_sample_utf8.csv')
sales <- unique(sales)
sales_clean <- sales

# Create a new CSV dataframe that will be used for both ABC Analysis and Multi-Criteria ABC Analysis.

grouped <- sales_clean %>%
  group_by(PRODUCTCODE) %>%
  summarize(total_sales = sum(QUANTITYORDERED),
            total_revenue = sum(SALES)) %>%
  ungroup()

# Create a new CSV dataframe that will be used for Multi-Criteria ABC Analysis on a Store-Level (classification in this case is 'Country').

by_store <- sales_clean %>%
  group_by(COUNTRY, PRODUCTCODE) %>%
  summarize(total_sales = sum(QUANTITYORDERED),
            total_revenue = sum(SALES)) %>%
  ungroup()

#############################
### PART 2 - ABC ANALYSIS ###
#############################

# Create a new dataframe (abc) to perform ABC Analysis.
# Calculate the cumulative percentage of total sales.

abc <- grouped %>%
  arrange(desc(total_sales)) %>%
  mutate(cum_pct_sales = cumsum(total_sales) / sum(total_sales))

# Assign ABC categories based on cumulative percentage of total sales.

abc <- abc %>%
  mutate(Category = ifelse(cum_pct_sales <= 0.8, "A",
                           ifelse(cum_pct_sales <= 0.95, "B", "C")))

# Plot the Countplot using ggplot2, which shows the number of A, B, and C category SKUs.

abc_countplot <- ggplot(abc, aes(x = Category)) +
  geom_bar() +
  ggtitle("Number of A, B, and C Category SKUs") +
  xlab("ABC Product Category Type") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))

# Plot the Barplot using ggplot2, which shows the average quantity ordered for each product code belonging to the A, B, C category types.

abc_barplot <- ggplot(abc, aes(x = Category, y = total_sales)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Average Quantity Ordered of A, B, and C Category Product Code") +
  xlab("ABC Product Category Type") +
  ylab("Average Quantity Ordered for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

############################################
### PART 3 - MULTI-CRITERIA ABC ANALYSIS ###
############################################

# Create a new dataframe (mc_abc) to perform Multi-Criteria ABC Analysis.

mc_abc <- productmix(grouped$PRODUCTCODE, grouped$total_sales, grouped$total_revenue)
str(mc_abc)
table(mc_abc$product_mix)

# Plot the Countplot using ggplot2, which shows the number of SKUs belong to each of the 9 Product Mix.

mc_abc_countplot <- ggplot(mc_abc, aes(x = product_mix)) +
  geom_bar() +
  ggtitle("Number of A_A to C_C Category SKUs") +
  xlab("ABC Product Mix") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))

# Plot the Barplot using ggplot2, which shows the average quantity ordered for each product code belong to each of the 9 Product Mix.

mc_abc_barplot1 <- ggplot(mc_abc, aes(x = product_mix, y = sales)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Average Quantity Ordered of A_A to C_C Category Product Code") +
  xlab("ABC Product Mix") +
  ylab("Average Quantity Ordered for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

# Plot the Barplot using ggplot2, which shows the average revenue for each product code belong to each of the 9 Product Mix.

mc_abc_barplot2 <- ggplot(mc_abc, aes(x = product_mix, y = revenue)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Total Revenue of A_A to C_C Category Product Code") +
  xlab("ABC Product Mix") + ylab("Average Revenue for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

#############################################################
### PART 4 - MULTI-CRITERIA ABC ANALYSIS ON A STORE-LEVEL ###
#############################################################

# Create a new dataframe (mix_country) to perform Multi-Criteria ABC Analysis on a store-level.

mix_country <- inventorize::productmix_storelevel(by_store$PRODUCTCODE, by_store$total_sales, by_store$total_revenue, by_store$COUNTRY)
product_mix <- mix_country %>%
  dplyr::group_by(storeofsku, product_mix) %>%
  dplyr::summarise(SKU_count = n()) %>%
  dplyr::ungroup() %>%
  dplyr::select(storeofsku, product_mix, SKU_count)

# Create a variable for Australia's product mix for analysis.

australia <- subset(product_mix, storeofsku == "Australia")
str(australia)

# Plot the Countplot using ggplot2, which shows the number of SKUs belong to each of the 9 Product Mix (for Australia).

aus_countplot <- ggplot(australia, aes(x = product_mix, y = SKU_count)) +
  geom_bar(stat = "identity") +
  ggtitle("Number of A_A to C_C Category SKUs for Australia") +
  xlab("ABC Product Mix") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))
