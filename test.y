category C n t s r k l m d j p h ʔ b g w ŋ ʃ
# category names can be anything with no spaces in it, same with phonemes

category V a i e o u
# by default phonemes are listed from most frequent to least
# to make a categroy with equally frequent phonemes use "uniform" instead of "category"

category N n m ŋ

syllable I C?75 V N?25
# ? after a category makes it optional, putting a number from 0-100 after it gives it that percent chance of appearing

syllable S C V N?25

word I S? S?
# only 1 word shape, it doesn't take a name
# default random probability is 50%

reject [mnŋ][mnŋʔhrljw] ^ʔ ji wu
# regexes can be used to reject words that match a certain pattern

filter [nŋ]([pb])>m\1 [mŋ]([tsdʃ])>n\1 [mn]([kg])>ŋ\1 j>y ʔ>' ŋ>ng ʃ>sh
# pattern>substitution
