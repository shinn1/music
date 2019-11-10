# import data
setwd('~/Google Drive/music_project/data_processed')

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

# pair traits
foo <- ddply(max, .(pair), function(x) data.frame(
     prof_sum = sum(x$prof),
     prof_diff = abs(diff(x$prof)),
     others_sum = sum(x$others),
     others_diff = abs(diff(x$others)),
     jam_sum = sum(x$jam),
     jam_diff = abs(diff(x$jam)),
     duration_sum = sum(x$duration),
     duration_diff = abs(diff(x$duration))))

pair_traits <- foo
pair_traits$MI_s1 <- diag(rec_pair[1, 2, 1:30, 31:60])
pair_traits$MI_s2 <- diag(rec_pair[2, 2, 1:30, 31:60])
pair_traits$MI <- (pair_traits$MI_s1 + pair_traits$MI_s2)/2

pair_traits$others_sum <- as.factor(pair_traits$others_sum )
pair_traits$others_diff <- as.factor(pair_traits$others_diff)
pair_traits$prof_sum <- as.factor(pair_traits$prof_sum)
pair_traits$prof_diff <- as.factor(pair_traits$prof_diff)
pair_traits$jam_sum <- as.factor(pair_traits$jam_sum)
pair_traits$jam_diff <- as.factor(pair_traits$jam_diff)

# model
model_s1 <- glm(MI_s1 ~  others_sum * others_diff + duration_sum * duration_diff,
     data = pair_traits, family = Gamma('log'))
summary(model_s1)
library(car)
Anova(model_s1)
# anova(model_s1, test = 'Chisq')

# model p-value
phi <- summary(model_s1)$dispersion
chisq <- (model_s1$null.deviance - model_s1$deviance)/phi
df <- model_s1$df.null - model_s1$df.resid
phi; chisq; 1 - pchisq(chisq, df)


model_s2 <- glm(MI_s2 ~  others_sum * others_diff + duration_sum * duration_diff,
     data = pair_traits, family = Gamma('log'))
#anova(model_s2, test = 'Chisq')
Anova(model_s2)
summary(model_s2)

# model p-value
phi <- summary(model_s2)$dispersion
chisq <- (model_s2$null.deviance - model_s2$deviance)/phi
df <- model_s2$df.null - model_s2$df.resid
1 - pchisq(chisq, df)


#________________________
# plot

library(ggplot2)
library(colorRamps)

## prediction of others (session 1)
## set duration = 0
pdf('~/Google Drive/music_project/figures/traits/MI_others_s1.pdf', height = 4, width = 4)
foo <- data.frame(others_sum = as.factor(rep(0:7, 5)),
     others_diff = as.factor(rep(0:4, each = 8)),
     duration_sum = 0, duration_diff = 0)

foo$TE_pred <- predict(model_s1, newdata = foo)

ggplot(foo, aes(others_sum, others_diff)) +
     geom_tile(aes(fill = TE_pred)) +
     coord_fixed(ratio = 8/5) +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'Sum of the experience of playing with others',
     y = 'Difference of the experience of playing with others')
dev.off()

## prediction of others (session 2)
## set duration = 0
pdf('~/Google Drive/music_project/figures/traits/MI_others_s2.pdf', height = 4, width = 4)
foo <- data.frame(others_sum = as.factor(rep(0:7, 5)),
     others_diff = as.factor(rep(0:4, each = 8)),
     duration_sum = 0, duration_diff = 0)

foo$TE_pred <- predict(model_s2, newdata = foo)

ggplot(foo, aes(others_sum, others_diff)) +
     geom_tile(aes(fill = TE_pred)) +
     coord_fixed(ratio = 8/5) +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'Sum of the experience of playing with others',
     y = 'Difference of the experience of playing with others')
dev.off()

## prediction of duation (session 1)
pdf('~/Google Drive/music_project/figures/traits/MI_duration_s1.pdf', height = 4, width = 4)

seq_sum <- seq(0, 30, 0.1)
seq_diff <- seq(0, 15, 0.1)

foo <- data.frame(duration_sum = rep(seq_sum, length(seq_diff)),
     duration_diff = rep(seq_diff, each = length(seq_sum)))

coef_sum <- model_s1$coefficients[13]
coef_diff <- model_s1$coefficients[14]
coef_interaction <- model_s1$coefficients[43]

foo$TE_effect <- coef_sum * foo$duration_sum + coef_diff * foo$duration_diff +
     coef_interaction * foo$duration_sum * foo$duration_diff

ggplot(foo, aes(duration_sum, duration_diff)) +
     geom_raster(aes(fill = TE_effect)) +
     coord_fixed(21/15) +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'Sum of the duration of practice (years)',
     y = 'Difference of the duration of practice (years)')
dev.off()

## prediction of duation (session 2)
pdf('~/Google Drive/music_project/figures/traits/MI_duration_s2.pdf', height = 4, width = 4)

seq_sum <- seq(0, 30, 0.1)
seq_diff <- seq(0, 15, 0.1)

foo <- data.frame(duration_sum = rep(seq_sum, length(seq_diff)),
     duration_diff = rep(seq_diff, each = length(seq_sum)))

coef_sum <- model_s2$coefficients[13]
coef_diff <- model_s2$coefficients[14]
coef_interaction <- model_s2$coefficients[43]

foo$TE_effect <- coef_sum * foo$duration_sum + coef_diff * foo$duration_diff +
     coef_interaction * foo$duration_sum * foo$duration_diff

ggplot(foo, aes(duration_sum, duration_diff)) +
     geom_raster(aes(fill = TE_effect)) +
     coord_fixed(21/15) +
     scale_fill_gradientn(colours = matlab.like(10), limit = c(-5.38, 2.59)) +
     labs(fill = 'TE (received)', x = 'Sum of the duration of practice (years)',
     y = 'Difference of the duration of practice (years)')
dev.off()
