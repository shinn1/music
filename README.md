## Data
- `amplitude.csv` contains sound amplitudes of music at a 150-ms interval
- `survey.csv` contains survey data

## Recurrence analysis
- `recurrence_together.py` computes recurrence metrics for music created by pairs
- `shuffle_rec_together.py` performs permutation test on the observed recurrence metrics
- `recurrence_pair.py` computes mutual information and transfer entropy
- `shuffle_rec_pair.py` performs permutation test on the observed mutual information and transfer entropy

## Relationship with individual attributes
- `analysis_MI_traits.r` runs GLM on mutual information
- `analysis_TE_traits.r` runs GLM on transfer entropy

## sample music
- `sample/pair20session1.wav`: music with lowest mutual information (0.008) 
- `sample/pair15session2.wav`: music with highest mutual information (0.637)
- `sample/pair02session2.wav`: music with lowest symbolic recurrence rate (0.117) 
- `sample/pair26session1.wav`: music with highest symbolic recurrence rate (0.321)
