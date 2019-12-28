SMM.py & MFE.py, Anthony Androulakis, 2019
# Sung Melody Assessment
Sung Melody Assessment in Python. Includes sung melody transcription (SMM/Sung Melody to Matrix) and melody assessment (MFE/Melodic Fidelity Evaluator). This is an improved version of my [EncodingAndAssessingSungMelodies](https://github.com/AnthonyAndroulakis/EncodingAndAssessingSungMelodies) algorithm. Improvements include increased efficiency and accuracy.
![flowchart](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/examples/SungMelodyAssessment_flowchart.png)

## Requirements:
1) .wav file of a sung melody, any length
2) python3 (tested successfully in python3)
3) python modules:
    - parselmouth (https://github.com/AnthonyAndroulakis/parselmouthForPython3)
    - numpy
    - scipy
    - itertools
    - more_itertools

## How to run SMM (Sung Melody to Matrix):
`import SMM`       
`Phz = SMM.SMM(filename)`     
`notePitches = PHz[0]`     
`noteLengths = PHz[1]`     
will also output a txt file in this format:         
PHz=notePitches,noteLengths      

## How to run MFE (Melodic Fidelity Evaluator):
`import MFE`     
`MFE.MFE('melody.txt', 'sung.txt')`      
returns noteIntervalError, rhythmError, noteNumDifference

##### example txt file: https://github.com/AnthonyAndroulakis/TuneTaskApps/blob/master/the%20tunes/matricies/tune1.txt

---------------------------------
# How these algorithms work: \*
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
          
- __function 1__: for the simple case of the participant singing the same # of notes as the melody (case 1), the steps below are followed:
  1) scale participant sung note durations by the projection of (participant durations) onto (melody durations)
  2) find the Rhythm Error by finding the Euclidean Distance between the scaled participant durations and the melody durations
  3) convert both the participant sung note frequencies and melody frequencies into whole numbers      
(-∞ <-- A4=0 --> +∞)
  4) find the note intervals of the participant sung notes and melody notes by calculating the difference between note pairs for each
  5) find the Note Interval Error by finding the Euclidean Distance between the note intervals of the participant sung notes and melody notes
  6) Number of notes added or deleted by the participant = # of participant notes - # of notes in melody

The algorithm described in function 1 is show here:
![MFE Case 1](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/examples/MFEcase1.png)

- __function 2__: for the other case (participant singing the different # of notes as the melody (case 2)), the steps below are first followed:
  1) Number of notes added of deleted by participant = # of participant notes - # of notes in melody
  2) find which has fewer notes (sung melody of participant OR melody) (shorter matrix) and which has more notes (sung melody of participant OR melody) (longer matrix)
  3) now the smaller matrix will be filled with specially chosen notes to guess the participant's intentions:
      * find all permutations of added notes into the smaller matrix. The notes of the smaller matrix cannot change order, but the added notes can be placed anywhere. The number of added notes is the absolute value of the Number of notes added of deleted by the participant
      * within each permutation, fill in pitches such that they are dependent on the value before and after. For example, if the pitches of the shortest matrix are 3,[extra note],[extra note],5, the only configurations available are 3,3,3,5 3,3,5,5 and 3,5,5,5. The configuration that leads to the smallest Euclidean Distance for note intervals between the shortest matrix and the longest matrix is chosen for each permutation.
      * find the permutation that has the smallest Euclidean Distance for note intervals between the shortest matrix and the longest matrix is found. 
  4) The matrix found above (previously shortest matrix) and the longest matrix are then placed as inputs into function 1 (described above) to calculate the Note Interval Error and Rhythm Error

The algorithm described in function 2 is shown here in 2 parts:     
if sung melody # of notes < standard melody # of notes:
![MFE Case 2](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/examples/MFEcase2.png)

if sung melody # of notes < standard melody # of notes:
![MFE Case 3](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/examples/MFEcase3.png)

### \* Further code explanations can be found in the comment lines in [SMM.py](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/SMM.py) and [MFE.py](https://github.com/AnthonyAndroulakis/SungMelodyAssessment/blob/master/MFE.py)
---------------------------------
# How to generate random 3-second melodies (along with corresponding txt files):
https://github.com/AnthonyAndroulakis/RaCoTuGe

---------------------------------
## Works Cited:
- Jadoul, Y., Thompson, B., & de Boer, B. (2018). Introducing Parselmouth: A Python interface to Praat. Journal of Phonetics, 71, 1-15. https://doi.org/10.1016/j.wocn.2018.07.001     
- Boersma, P., & Weenink, D. (2018). Praat: doing phonetics by computer [Computer program]. Version 6.0.43, retrieved 8 September 2018 from http://www.praat.org/     
- https://github.com/pybind/pybind11
- https://github.com/AnthonyAndroulakis/EncodingAndAssessingSungMelodies
- Androulakis, A. (2019). Encoding and Assessing Sung Melodies in Stroke Patients with Aphasia J Neurol Disord 7: 404. [doi:10.4172/2329-6895.1000404](https://www.omicsonline.org/open-access/encoding-and-assessing-sung-melodies-in-stroke-patients-with-aphasia-2329-6895-1000404-108296.html)
