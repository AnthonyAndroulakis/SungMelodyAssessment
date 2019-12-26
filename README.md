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
- input: .wav file of a sung melody
- output: txt file containing frequency and duration information       
(format: `[3 letter identifier]=[frequencies;durations]`)
- Praat (Parselmouth) is used to find the sung pitches and intensity curves.     
- Praat only includes human voice in the pitch curve, thus creating a discontinuous pitch curve (NaN values inbetween voiced notes).      
- Pitch segments that occur for less than 0.1 seconds are excluded.       
- To find the specific location in between 2 voiced notes that indicates a note change, the point of lowest intensity between each pair of voiced notes is picked (the intensity curve is smoothed with a gaussian filter with sigma length(envelope)/100).     
     
This is shown in the graph below:     
![Graph Example](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/examples/graphexample.png)

## Melodic Fidelity Evaluator (MFE):
- input: 2 txt files (a melody and a sung melody) each containing frequency and duration information.    
(format: `[3 letter identifier]=[frequencies;durations]`)
- output: measured error (using Euclidean distances): Note Interval Error, Rhythm Error, Number of notes added or deleted by participant
- 2 cases: (1) participant sings the same # of notes as melody (2) participant sings a different # of notes as melody
- for the simple case of the participant singing the same # of notes as the melody (case 1), the steps below are followed:
1) scale participant sung note durations by the projection of (participant durations) onto (melody durations)
2) find the Rhythm Error by finding the Euclidean Distance between the scaled participant durations and the melody durations
3) convert both the participant sung note frequencies and melody frequencies into whole numbers (-∞ <-- A4=0 --> +∞)

---------------------------------

## Works Cited:
- Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics, 71, 1-15. https://doi.org/10.1016/j.wocn.2018.07.001     
- Boersma, P., & Weenink, D. (2018). Praat: doing phonetics by computer [Computer program]. Version 6.0.43, retrieved 8 September 2018 from http://www.praat.org/     
- https://github.com/pybind/pybind11
