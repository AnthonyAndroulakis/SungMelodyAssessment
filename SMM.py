#Anthony Androulakis, SMM.py, 2019
#How to run: import SMM; notePitches,noteLengths = SMM.SMM(filename)
#note: to convert between .mp3 and .wav, do: ffmpeg -i filename.mp3 newfilename.wav
#assuming 0.1 seconds to be the fastest note anyone is going to sing
#the below code needs .wav files to function
from scipy.io import wavfile #needed for getting audio data (duration)
import more_itertools #helps in finding gaps of Nan for voice gaps
import parselmouth #praat in python
import numpy as np #arrays
import scipy.ndimage #gaussian moving average, for smoothing curve, assuming noise is random

#filename = 'voicetest2.wav'

def SMM(filename):
    snd = parselmouth.Sound(filename)
    Fs, data = wavfile.read(filename)
    duration = data.size/Fs

    #pitch tests#########################################

    pitch = snd.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan

    #####
    whereVoice = list(map(list, np.where(~np.isnan(pitch_values))))[0] #where non nan values exist
    consecutiveVoice = [list(group) for group in more_itertools.consecutive_groups(whereVoice)] #clump non nan consecutive indices together
    #duration/len(pitch_values) #find units of range(len(pitch_values)) in seconds
    beginnings = [r[0] for r in consecutiveVoice]
    endings = [t[-1] for t in consecutiveVoice]
    utteranceRanges = sorted(beginnings+endings)
    shortestnote = 0.1 #seconds
    findGreenFlags = [(duration/len(pitch_values))*len(e) >= shortestnote for e in consecutiveVoice] #also needed for final pitch detection, find utterances greater than or equal to 0.1 seconds
    updatedBeginnings = [beginnings[p] for p in range(len(consecutiveVoice)) if findGreenFlags[p]]
    updatedEndings = [endings[a] for a in range(len(consecutiveVoice)) if findGreenFlags[a]]
    pitchUtterancesB = [(duration/len(pitch_values))*u for u in updatedBeginnings] #find where pitch predicts note beginnings (units = seconds)
    pitchUtterancesE = [(duration/len(pitch_values))*s for s in updatedEndings] #find where pitch predicts note endings (units = seconds)
    pitchUtterances = sorted(pitchUtterancesB+pitchUtterancesE)

    #####intensity tests
    intensity = snd.to_intensity()
    envelope = [0 if i < 0 else i for i in list(intensity.values.T.flatten())] #took intensity and converted all negatives to 0s
    while envelope: #delete beginning 0s
        if envelope[0] != 0:
            break
        del envelope[0]
    while envelope: #delete trailing 0s
        if envelope[-1] != 0:
            break
        del envelope[-1]
    smooth_envelope = scipy.ndimage.gaussian_filter1d(envelope,round(len(envelope)/100)) #gaussian filter intensity with sigma len(envelope)/100, works well for 16th notes
    seconds_se = [duration/len(smooth_envelope)*f for f in range(len(smooth_envelope))] #smooth_envelope units conversion
    #####################
    
    ###finding beginnings and endings of utterances, final
    noteChanges = []
    for o in range(len(pitchUtterancesE)-1): #now working with seconds as units
        beginningIndex = min(seconds_se, key=lambda x:abs(x-pitchUtterancesE[o]))
        endingIndex = min(seconds_se, key=lambda x:abs(x-pitchUtterancesB[o+1]))
        minIntensity = min(list(smooth_envelope[seconds_se.index(beginningIndex):seconds_se.index(endingIndex)]))
        noteChanges.append((duration/len(smooth_envelope))*list(smooth_envelope).index(minIntensity))
    
    noteChanges.insert(0, pitchUtterancesB[0])
    noteChanges.append(pitchUtterancesE[-1])
    
    ###finding pitches of notes (based on middle mean of greenFlag areas)
    notePitches=[]
    for q in range(len(updatedEndings)): #now working with pitch list length units
        pitchIntervalBeginningIndex = int(updatedBeginnings[q] + round((updatedEndings[q]-updatedBeginnings[q])/4))
        pitchIntervalEndingIndex = int(updatedEndings[q] - round((updatedEndings[q]-updatedBeginnings[q])/4))
        averagePitch = sum(pitch_values[pitchIntervalBeginningIndex:pitchIntervalEndingIndex])/(pitchIntervalEndingIndex-pitchIntervalBeginningIndex+1)
        notePitches.append(averagePitch)
    
    #########################
    noteLengths = [t - s for s, t in zip(noteChanges, noteChanges[1:])]
    
    #########################
    return([notePitches,noteLengths])

#example run: notePitches,noteLengths = SMM.SMM(filename)
