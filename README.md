## Data
- `...` contains the wave files of music
- `...` contains survey data

## Sound amplitude
- `extract_amplitude.r` extracts sound amplitude from wave files

## Pairwise behavior
- `recurrence_pair.py` computes joint symbolic recurrence rate, mutual information, and transfer entropy (all combinations of players)
- `shuffle_rec_pair.py` performs permutation to test whether observed MI are different from random

## Joint behavior
- `recurrence_together.py` computes recurrence metrics for pairs (real and shuffled pairs)
- `shuffle_rec_together.py` performs permutation to test whether observed joint recurrence metrics are different from random

## Relationship with individual attributes
- `analysis_MI_traits.r` runs GLM on mutual information
- `analysis_TE_traits.r` runs GLM on transfer entropy

