library(reticulate)
np <- import('numpy')

# session, values (jointSRR, MI, TE12, TE21), player i, player j
rec_pair <- np$load('rec_pair_m3.npy')

# individual attributes
survey <- read.csv('survey.csv')
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

# model for session 1
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

# model for session 2
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

