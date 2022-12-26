C = n/t/k/m/s/l/r/ʔ/b/d/p/ŋ/j/w/h/g/z/ʀ
O = t/k/s/b/d/p/g/z
L = l/r/ʀ
V = a/i/u/ə
N = n/m/ŋ
I = (C:4/OL:1)%75 V (N)%25
S = [C:4/OL:1] V (N)%25
W = I(S(S))
reject = ji wu ^ʔ (.+)\1 [td]l N[Nʔh]

# C = n/t/k/m/s/l/r/ʔ/b/d/p/ŋ/j/w/h/ʃ/g/z/f/v/tʃ/ts/ʒ/dʒ/dz
# V = a/i/u/o/e
# N = n/m/ŋ
# I = (C)%75 V (N)%25
# S = C V (N)%25
# W = I(S(S))
# reject = ji wu ^ʔ (.+)\1 N[Nʔh]
# filter = [nŋ]([pbfv]) -> m\1, [mŋ]([tdszʃʒ]) -> n\1, [mn]([kg]) -> ŋ\1, ʔ -> ', ŋ -> ng, j -> y, tʃ -> c, ʃ -> sh, dʒ -> j, ʒ -> zh
