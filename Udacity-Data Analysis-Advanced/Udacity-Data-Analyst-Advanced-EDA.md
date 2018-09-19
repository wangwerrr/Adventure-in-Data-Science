---
title: '[Udacity/DA] 2 EDA'
date: 2018-07-04 09:34:32
categories: Data Science
tags:
- Udacity
- R
---
How to explore data both quantitatively and visually. Implementations with R.
<!-- more -->

## EDA
### Definition

### Goal

## R
### Basic Commands
- Command+Enter: run selected r script lines
- remove variables: rm(variable)
- Directory: getwd(), setwd('path/file')
- Read data: stateInfo <- read.csv('filename'), read.delim('pseudo_facebook.tsv')
- query:
    - get column: subset(dataSet, COLUMNS)   --  subset(statesInfo, state.region == 1)
    - dataSet[dataSet\$ROWS, dataSet\$COLUMS]   --  statesInfo[statesInfo$state.region == 1,  ]
    - delete variables: subset(dataSet, select = -COLUMNS)

     - number of rows: nrow()
     - number of columns: length()
- and/or: & / |
- if else
```r
mtcars$wt
cond <- mtcars$wt < 3
cond
mtcars$weight_class <- ifelse(cond, 'light', 'average')
mtcars$weight_class
cond <- mtcars$wt > 3.5
mtcars$weight_class <- ifelse(cond, 'heavy', mtcars$weight_class)
mtcars$weight_class
```
-  ordered factor variables
```r
reddit$age.range <- ordered(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"))
#or
reddit$age.range <- factor(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"), ordered=T)
```
### Exploring Single Variable
library:ggplot
dataset: pseudo_facebook.tsv
`library(ggplot2)
pf <- read.csv('pseudo_facebook.tsv', sep='\t')`

#### Call plot function
`ggplot(aes(x = dob_day), data = pf)`
- handle missing values (using subset)
 `ggplot(aes(x = friend_count), data = subset(pf, !is.na(gender)))`
- count -> proportion
    `ggplot(aes(x = friend_count, y = ..count../sum(..count..)), data = pf)`
    Note: sum(..count..) 将跨颜色进行总计，因此，显示的百分比是总用户数的百分比。要在每个组内绘制百分比，应使用y = ..density...

#### Add layers
Plots:
- Histogram
    bin width, color(outline), fill:
    `geom_histogram(binwidth = 1, color = 'black', fill = '#099DD9'))`
- Frequency Polygon
    `geom_freqpoly(aes(color = gender), binwidth=10)`
- Box Plot
`ggplot(aes(x = gender, y = friend_count), data = subset(pf, !is.na(gender))) +
geom_boxplot() ` -- notice we add parameter y to ggplot()

Features:
- axis range &  breaks
    adjust axis to smaller range (since there might be outliers: bad/good, extreme/non-extreme)
    `xlim(low, high)`
    `scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50))` -- delete data points (or `scale_x_discrete`)
    `coord_cartesian(ylim=c(0,1000)` -- does not delete data points, different when using box_plot
- Split up data by variable(s)
    `facet_wrap(~variable, scales = 'free_y')`
    `facet_grid(vertical_variable~horizontal_variable)`
- axis transformation
    `scale_x_log10()
    scale_x_sqrt()`
- coordinate transformation
    `coord_trans(x = "log10", y = "log10")`
- Multiple plots
`library(gridExtra)
p1 <- ggplot(aes(x = friend_count), data = pf) + geom_histogram()
p2 <- p1 + scale_x_log10()
p3 <- p1 + scale_x_sqrt()
grid.arrange(p1, p2, p3, ncol=1)`

- labeles
`xlab('Num of Friends')
ylab('Percentage of users with that friend count')`

Statistics:
`by(variable, split_by, output_statistic)`   output_statistic=summary, sum, etc.

`summary(variable/condition)`
`sum(variable)`
`length(variable)`
`table(variable)`

- value counts
    `table(pf$gender)`
    `by(pf$friend_count, pf$gender, sum)`
- min, max, med, etc.
    `by(pf$friend_count, pf$gender, summary)`
    
    `summary(pf$friend_count)`
    transformations:
    `summary(log10(pf$friend_count+1))`   -- add 1 to avoid -INF
    `summary(sqrt(pf$friend_count))`
- IQR
    `IQR(subset(diamonds, price <1000)$price) `

save image:
`ggsave('priceHistogram.png')`

### Exploring Two Variables
**Scatter Plot**
`ggplot(aes(x = age, y = friend_count), data = pf) + geom_point()`
- aes: aesthetic wrapper
- transparency: `geom_point(alpha=1/20)` -- 20 data points = 1 point in the plot, to reduce over plottings
- jitter: `geom_jitter(alpha=1/20, position=position_jitter(h=0))` -- add noise, discrete->continuous; position_jitter set the min height
- represent another feature of the point by size:`geom_point(aes(size = feature))`

**Summaries**
- connect the dots: `+ geom_line(color='orange', linetype=2)`
    - mean: `geom_line(stat = 'summary', fun.y = mean)`
    - quantile:  `geom_line(stat = 'summary', fun.y = quantile, probs=.9)`
- horizontal line: `geom_hline(yintercept=1, alpha=0.3)`
- smoother: `geom_smooth(method='lm', color='red')`, lm for linear model

- create derived dataframe
using `library(dplyr)`
```r
pf.fc_by_age <- pf %.%
    filter(!is.na(age)) %.%
    group_by(age)  %.%
    summarise(friend_count_mean = mean(friend_count),
              friend_count_median = median(friend_count),
              n = n()) %.%
    arrange(age)

head(pf.fc_by_age,20)
```
or
```r
age_groups <- group_by(pf, age)

pf.fc_by_age <- summarise(age_groups,
friend_count_mean = mean(friend_count),
friend_count_median = median(friend_count),
n = n()) # count values

pf.fc_by_age <- arrange(pf.fc_by_age, age)

head(pf.fc_by_age,20)
```
- correlation coefficient (linear): `cor.test(df$x, df$y, method='pearson')` or `with(df, cor.test(x, y, method='pearson))`, spearman

### Exploring 3+ Variables
**Scatter Plot by Gender**
eg. x = age, y = friend_count, color = gender
```r
ggplot(aes(x = age, y = friend_count),
     data = subset(pf, !is.na(gender))) +
     geom_line(aes(color = gender), stat = 'summary', fun.y = median)
```

**Reshape Data**
```r
library(reshape2)

pf.fc_by_age_gender.wide <- dcast(pf.fc_by_age_gender,
                            age ~ gender,
                            value.var = 'median_friend_count')
```

**Cut a Variable**: from continuous to discrete
`cut(pf$year_joined, breaks = int or seq)`

**Transform**
- addition of columns: `yo <- transform(yo, all.purchases = strawberry + blueberry + plain)`

`x %in% y` 返回一个长度与 x 相同的逻辑（布尔）向量，该向量指出 x 中的每一个条目是否都出现在 y 中。也就是说，对于 x 中的每一个条目，该向量都会检查这一条目是否也出现在 y 中。

**Plot Matrices**
`library(GGally)`
`ggpairs(data)`

**Heat Map**
`ggplot(aes(y,x,fill), data)
    geom_tile() +
    scale_fill_gradientn(colours=colorRampPalette(c('blue', 'red'))(100))`

### Linear Model


## Reference
[1. Quick R](https://www.statmethods.net)
[2. Loading Data and Basic Formatting in R](http://flowingdata.com/2015/02/18/loading-data-and-basic-formatting-in-r/)
[3. Cookbook for R](http://www.cookbook-r.com)
[4. Transformed Cartesian coordinate system](https://ggplot2.tidyverse.org/reference/coord_trans.html)
[5. Introducing dplyr](https://blog.rstudio.com/2014/01/17/introducing-dplyr/)
[6. ggplot2](https://ggplot2.tidyverse.org)
