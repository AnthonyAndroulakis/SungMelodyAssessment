SMM.py, Anthony Androulakis, 2019
# Sung Melody Transcription
Sung Melody Transcription in Python, this is a vastly-more-efficient version of my SMM.m

## Requirements:
1) .wav file of a sung melody, any length
2) python3
3) python modules:
    - scipy
    - more_itertools
    - parselmouth
    - numpy

## How to run:
`import SMM`       
`notePitches,noteLengths = SMM.SMM(filename)`

## License:
As long as you cite me (Anthony Androulakis) and this repo as well as https://github.com/AnthonyAndroulakis/EncodingAndAssessingSungMelodies, you may use the code.

## Works Cited:
Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics, 71, 1-15. https://doi.org/10.1016/j.wocn.2018.07.001     
Boersma, P., & Weenink, D. (2018). Praat: doing phonetics by computer [Computer program]. Version 6.0.43, retrieved 8 September 2018 from http://www.praat.org/     
https://github.com/pybind/pybind11
