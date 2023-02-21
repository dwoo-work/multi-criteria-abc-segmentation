
############################
### PART 1 - PREPARATION ###
############################

required_libraries <- c("tidyverse", "inventorize", "dplyr", "ggplot2")
lapply(required_libraries, require, character.only = TRUE)

sales <- read.csv('C:\\Users\\danie\\OneDrive\\Desktop\\archive\\sales_data_sample_utf8.csv')
sales <- unique(sales)
sales_clean <- sales

grouped <- sales_clean %>%
  group_by(PRODUCTCODE) %>%
  summarize(total_sales = sum(QUANTITYORDERED),
            total_revenue = sum(SALES)) %>%
  ungroup()

by_store <- sales_clean %>%
  group_by(COUNTRY, PRODUCTCODE) %>%
  summarize(total_sales = sum(QUANTITYORDERED),
            total_revenue = sum(SALES)) %>%
  ungroup()

#############################
### PART 2 - ABC ANALYSIS ###
#############################

abc <- grouped %>%
  arrange(desc(total_sales)) %>%
  mutate(cum_pct_sales = cumsum(total_sales) / sum(total_sales))

abc <- abc %>%
  mutate(Category = ifelse(cum_pct_sales <= 0.8, "A",
                           ifelse(cum_pct_sales <= 0.95, "B", "C")))

abc_countplot <- ggplot(abc, aes(x = Category)) +
  geom_bar() +
  ggtitle("Number of A, B, and C Category SKUs") +
  xlab("ABC Product Category Type") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))

abc_barplot <- ggplot(abc, aes(x = Category, y = total_sales)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Average Quantity Ordered of A, B, and C Category Product Code") +
  xlab("ABC Product Category Type") +
  ylab("Average Quantity Ordered for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

############################################
### PART 3 - MULTI-CRITERIA ABC ANALYSIS ###
############################################

mc_abc <- productmix(grouped$PRODUCTCODE, grouped$total_sales, grouped$total_revenue)
str(mc_abc)
table(mc_abc$product_mix)

mc_abc_countplot <- ggplot(mc_abc, aes(x = product_mix)) +
  geom_bar() +
  ggtitle("Number of A_A to C_C Category SKUs") +
  xlab("ABC Product Mix") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))

mc_abc_barplot1 <- ggplot(mc_abc, aes(x = product_mix, y = sales)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Average Quantity Ordered of A_A to C_C Category Product Code") +
  xlab("ABC Product Mix") +
  ylab("Average Quantity Ordered for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

mc_abc_barplot2 <- ggplot(mc_abc, aes(x = product_mix, y = revenue)) +
  geom_bar(stat = "summary", fun = "mean") +
  ggtitle("Total Revenue of A_A to C_C Category Product Code") +
  xlab("ABC Product Mix") + ylab("Average Revenue for each Product Code") +
  theme(plot.title = element_text(hjust = 0.5))

#############################################################
### PART 4 - MULTI-CRITERIA ABC ANALYSIS ON A STORE-LEVEL ###
#############################################################

mix_country <- inventorize::productmix_storelevel(by_store$PRODUCTCODE, by_store$total_sales, by_store$total_revenue, by_store$COUNTRY)
product_mix <- mix_country %>%
  dplyr::group_by(storeofsku, product_mix) %>%
  dplyr::summarise(SKU_count = n()) %>%
  dplyr::ungroup() %>%
  dplyr::select(storeofsku, product_mix, SKU_count)

australia <- subset(product_mix, storeofsku == "Australia")
str(australia)

aus_countplot <- ggplot(australia, aes(x = product_mix, y = SKU_count)) +
  geom_bar(stat = "identity") +
  ggtitle("Number of A_A to C_C Category SKUs for Australia") +
  xlab("ABC Product Mix") + ylab("Number of SKUs") +
  theme(plot.title = element_text(hjust = 0.5))
