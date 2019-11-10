# import data
setwd('~/Google Drive/music_project/data_processed')
library(MASS)
library(glmnet)
library(reticulate)

np <- import('numpy')

# session, values (jointSRR, MI, TE12, TE21), player i, player j
rec_pair <- np$load('rec_pair_m3.npy')

# individual attributes
survey <- read.csv('~/Google Drive/music_project/survey/survey.csv')
survey$duration[survey$duration == '<1'] <- 0.5
survey$duration <- as.numeric(as.character(survey$duration))
survey <- round(survey)

# get max value for each player
library(plyr)
max <- ddply(survey, .(pair, player), function(x) data.frame(
     prof = max(x$proficiency),
     others = max(x$others),
     jam = max(x$jam),
     duration = max(x$duration)))

max$prof <- as.factor(max$prof)
max$others <- as.factor(max$others)
max$jam <- as.factor(max$jam)
# max$duration <- ihs(max$duration)   # transformation

foo <- max[order(max$player, max$pair),]
bar <- max[order(-max$player, max$pair),]

foo <- cbind(foo[,-(1:2)], bar[, 3:6])
colnames(foo) <- c('my_prof', 'my_others', 'my_jam', 'my_duration',
     'your_prof', 'your_others', 'your_jam', 'your_duration')

# Transfer entropy
TE12_s1 <- diag(rec_pair[1, 3, 1:30, 31:60])
TE21_s1 <- diag(rec_pair[1, 3, 31:60, 1:30])
TE12_s2 <- diag(rec_pair[2, 3, 1:30, 31:60])
TE21_s2 <- diag(rec_pair[2, 3, 31:60, 1:30])

ind_traits <- foo
ind_traits$TEreceive_s1 <- c(TE21_s1, TE12_s1)
ind_traits$TEreceive_s2 <- c(TE21_s2, TE12_s2)
ind_traits$TEreceive <- (ind_traits$TEreceive_s1 + ind_traits$TEreceive_s2)/2

model_s1 <- glm(TEreceive_s1 ~ my_others * your_others + my_duration * your_duration,
     data = ind_traits, family = Gamma('log'))
# anova(model_s1, test = 'Chisq')
library(car)
Anova(model_s1)

model_s2 <- glm(TEreceive_s2 ~ my_others * your_others + my_duration * your_duration,
     data = ind_traits, family = Gamma('log'))
#anova(model_s2, test = 'Chisq')
Anova(model_s2)

#_______________________________________________________
#
# plot
library(ggplot2)
library(colorRamps)

# plot prediction of others (session 1)
## set duration = 0
pdf('~/Google Drive/music_project/figures/traits/TE_others_s1.pdf', height = 4, width = 4)
seq <- seq(0, 4, 1)
foo <- data.frame(my_others = as.factor(rep(seq, length(seq))),
     your_others = as.factor(rep(seq, each = length(seq))),
     my_duration = 0, your_duration = 0)

foo$TE_pred <- predict(model_s1, newdata = foo)

# limit = c(-4, 2.32)

ggplot(foo, aes(my_others, your_others)) +
     geom_tile(aes(fill = TE_pred)) +
     coord_fixed() +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'My experience of playing with others',
     y = 'Your experience of playing with others')
dev.off()

# plot prediction of others (session 2)
pdf('~/Google Drive/music_project/figures/traits/TE_others_s2.pdf', height = 4, width = 4)
seq <- seq(0, 4, 1)
foo <- data.frame(my_others = as.factor(rep(seq, length(seq))),
     your_others = as.factor(rep(seq, each = length(seq))),
     my_duration = 0, your_duration = 0)

foo$TE_pred <- predict(model_s2, newdata = foo)

ggplot(foo, aes(my_others, your_others)) +
     geom_tile(aes(fill = TE_pred)) +
     coord_fixed() +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'My experience of playing with others',
     y = 'Your experience of playing with others')
dev.off()




# plot prediction of duration (session 1)
pdf('~/Google Drive/music_project/figures/traits/TE_duration_s1.pdf', height = 4, width = 4)
seq <- seq(0, 15, 0.1)
foo <- data.frame(my_duration = rep(seq, length(seq)),
     your_duration = rep(seq, each = length(seq)))

coef_my <- model_s1$coefficients[10]
coef_your <- model_s1$coefficients[11]
coef_interaction <- model_s1$coefficients[28]

foo$TE_effect <- coef_my * foo$my_duration + coef_your * foo$your_duration +
     coef_interaction * foo$my_duration * foo$your_duration


ggplot(foo, aes(my_duration, your_duration)) +
     geom_raster(aes(fill = TE_effect)) +
     coord_fixed() +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-4, 2.32)) +
     labs(fill = 'TE (received)', x = 'My duration of practice (years)',
     y = 'Your duration of practice (years)')
dev.off()

# plot prediction of duration (session 2)
## set others = '0'
pdf('~/Google Drive/music_project/figures/traits/TE_duration_s2.pdf', height = 4, width = 4)
seq <- seq(0, 15, 0.1)
foo <- data.frame(my_duration = rep(seq, length(seq)),
     your_duration = rep(seq, each = length(seq)))

coef_my <- model_s2$coefficients[10]
coef_your <- model_s2$coefficients[11]
coef_interaction <- model_s2$coefficients[28]

foo$TE_effect <- coef_my * foo$my_duration + coef_your * foo$your_duration +
     coef_interaction * foo$my_duration * foo$your_duration

ggplot(foo, aes(my_duration, your_duration)) +
     geom_raster(aes(fill = TE_effect)) +
     coord_fixed() +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'My duration of practice (years)',
     y = 'Your duration of practice (years)')
dev.off()
