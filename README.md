SMM.py & MFE.py, Anthony Androulakis, 2019
# Sung Melody Assessment
Sung Melody Assessment in Python, more efficient and simple that my codes 2 years ago

## Requirements:
1) .wav file of a sung melody, any length
2) python3 (tested successfully in python3)
3) python modules:
    - scipy
    - itertools
    - more_itertools
    - parselmouth (https://github.com/AnthonyAndroulakis/parselmouthForPython3)
    - numpy

## How to run SMM:
`import SMM`       
`Phz = SMM.SMM(filename)`     
`notePitches = PHz[0]`     
`noteLengths = PHz[1]`     
will also output a txt file in this format:         
PHz=notePitches,noteLengths      

## How to run MFE:
`import MFE`     
`MFE.MFE('tune.txt', 'participant.txt')`      
returns noteIntervalError, rhythmError, noteNumDifference

---------------------------------
# How these algorithms work:

## Sung Melody to Matrix (SMM):
Praat (Parselmouth) is used to find the sung pitches and intensity curves.     
Praat only includes human voice in the pitch curve, thus creating a discontinuous pitch curve (NaN values inbetween voiced notes).      
Pitch segments that occur for less than 0.1 seconds are excluded.       
To find the specific location in between 2 voiced notes that indicates a note change, the point of lowest intensity between each pair of voiced notes is picked.     
     
This is shown in the picture below:     
[Graph Example](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/graphexample.png)

## Melodic Fidelity Evaluator (MFE):

---------------------------------

## Works Cited:
- Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics, 71, 1-15. https://doi.org/10.1016/j.wocn.2018.07.001     
- Boersma, P., & Weenink, D. (2018). Praat: doing phonetics by computer [Computer program]. Version 6.0.43, retrieved 8 September 2018 from http://www.praat.org/     
- https://github.com/pybind/pybind11
