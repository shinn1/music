# data preparation
library(tuneR)
library(seewave)

file_name_p1s1 <- file_name_p1s2 <- c()
file_name_p2s1 <- file_name_p2s2 <- c()
for(i in 1:30) {

	file_name_p1s1[i] <- paste('Trial00', sprintf("%02d",i), '/Trial00', sprintf("%02d",i), 'p01s1.wav', sep='')
	file_name_p2s1[i] <- paste('Trial00', sprintf("%02d",i), '/Trial00', sprintf("%02d",i), 'p02s1.wav', sep='')
	file_name_p1s2[i] <- paste('Trial00', sprintf("%02d",i), '/Trial00', sprintf("%02d",i), 'p01s2.wav', sep='')
	file_name_p2s2[i] <- paste('Trial00', sprintf("%02d",i), '/Trial00', sprintf("%02d",i), 'p02s2.wav', sep='')
}

for(i in 1:30) {

	# session 1
	# extract amplitude from signal
	setwd('C:/Users/User/Google Drive/Music Project/Trial Data/')
	wav1 <- readWave(file_name_p1s1[i])
	amp1 <- env(wav1, plot=F)/(2^(wav1@bit -1))
	time1 <- 0:(length(amp1))/wav1@samp.rate

	wav2 <- readWave(file_name_p2s1[i])
	amp2 <- env(wav2, plot=F)/(2^(wav2@bit -1))
	time2 <- 0:(length(amp2))/wav2@samp.rate

	# subsampling at every tau second
	tau <- 0.15

	amp1sub <- amp1[seq(1, length(amp1), wav1@samp.rate*tau)]
	time1sub <- time1[seq(1, length(time1), wav1@samp.rate*tau)]
	amp2sub <- amp2[seq(1, length(amp2), wav2@samp.rate*tau)]
	time2sub <- time2[seq(1, length(time2), wav2@samp.rate*tau)]

	# cut the sound at first 15 s (backing track) and over 120 s
	max <- min(max(time1sub), max(time2sub), 120)
	amp1sub <- amp1sub[time1sub >= 15 & time1sub <= max]
	amp2sub <- amp2sub[time2sub >= 15 & time2sub <= max]
	time1sub <- time1sub[time1sub >= 15 & time1sub <= max]
	time2sub <- time2sub[time2sub >= 15 & time2sub <= max]

	# write
	setwd('C:/Users/User/Google Drive/music_project/data_processed/wav data (0.15 s)')
	p1s1 <- data.frame(second=time1sub, amplitude=amp1sub)
	p2s1 <- data.frame(second=time2sub, amplitude=amp2sub)
	f1 <- paste('Trial', sprintf("%02d",i), 'p1s1.csv', sep='')
	f2 <- paste('Trial', sprintf("%02d",i), 'p2s1.csv', sep='')
	write.csv(p1s1, file=f1, row.names=F)
	write.csv(p2s1, file=f2, row.names=F)


	# session 2
	# extract amplitude from signal
	setwd('C:/Users/User/Google Drive/Music Project/Trial Data/')
	wav1 <- readWave(file_name_p1s2[i])
	amp1 <- env(wav1, plot=F)/(2^(wav1@bit -1))
	time1 <- 0:(length(amp1))/wav1@samp.rate

	wav2 <- readWave(file_name_p2s2[i])
	amp2 <- env(wav2, plot=F)/(2^(wav2@bit -1))
	time2 <- 0:(length(amp2))/wav2@samp.rate

	amp1sub <- amp1[seq(1, length(amp1), wav1@samp.rate*tau)]
	time1sub <- time1[seq(1, length(time1), wav1@samp.rate*tau)]
	amp2sub <- amp2[seq(1, length(amp2), wav2@samp.rate*tau)]
	time2sub <- time2[seq(1, length(time2), wav2@samp.rate*tau)]

	# cut the sound at first 15 s (backing track) and over 120 s
	max <- min(max(time1sub), max(time2sub), 120)
	amp1sub <- amp1sub[time1sub >= 15 & time1sub <= max]
	amp2sub <- amp2sub[time2sub >= 15 & time2sub <= max]
	time1sub <- time1sub[time1sub >= 15 & time1sub <= max]
	time2sub <- time2sub[time2sub >= 15 & time2sub <= max]

	# write
	setwd('C:/Users/User/Google Drive/music_project/data_processed/wav data (0.15 s)')
	p1s2 <- data.frame(second=time1sub, amplitude=amp1sub)
	p2s2 <- data.frame(second=time2sub, amplitude=amp2sub)
	f1 <- paste('Trial', sprintf("%02d",i), 'p1s2.csv', sep='')
	f2 <- paste('Trial', sprintf("%02d",i), 'p2s2.csv', sep='')
	write.csv(p1s2, file=f1, row.names=F)
	write.csv(p2s2, file=f2, row.names=F)

	gc()
	cat(i, 'done.\n')
}
