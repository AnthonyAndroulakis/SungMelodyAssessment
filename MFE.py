#looks at each patient individually, input is 2 txt files
import math
import numpy as np
import itertools
import more_itertools

#KEY: Omat=Tune matrix; Pmat=Participant matrix
#########################Assessments############################
###Case 1: same num notes###
def sameNumNotes(OmatPitches, OmatLengths, PmatPitches, PmatLengths):
    #noteNumDifference = 0 #document it

    #scale using the projection of PmatLengths onto OmatLengths
    scaleLength = sum([PmatLengths[i]*OmatLengths[i] for i in range(len(PmatLengths))])/sum([PmatLengths[j]**2 for j in range(len(PmatLengths))]) #magnitude of projection of OmatLengths onto PmatLengths
    PmatLengths = [scaleLength*k for k in PmatLengths] #scale PmatLengths accordingly
    
    #Rhythm Error
    rhythmError = math.sqrt(sum([(OmatLengths[l]-PmatLengths[l])**2 for l in range(len(OmatLengths))])) #Euclidean distance
    
    #Note Interval Error
    OmatNoteIntervals = [m - n for n, m in zip(OmatPitches, OmatPitches[1:])] #find note intervals in (original) tune
    PmatNoteIntervals = [o - p for p, o in zip(PmatPitches, PmatPitches[1:])] #find note intervals in participant sung melody
    noteIntervalError = math.sqrt(sum([(OmatNoteIntervals[q]-PmatNoteIntervals[q])**2 for q in range(len(OmatNoteIntervals))])) #Euclidean distance

    print('Note Interval Error (semitones): '+str(noteIntervalError)+', Rhythm Error (seconds): '+str(rhythmError))
    #print('Number of notes added/deleted: 0')
    #return noteIntervalError, rhythmError, noteNumDifference
    return noteIntervalError, rhythmError

###Case 2: participant num notes not equal to original tune num notes###
#if len(OmatPitches) != len(PmatPitches): #change this to a function, move if statement down to main function

def diffNumNotes(LmatPitches, LmatLengths, SmatPitches, SmatLengths): #longer mat and shorter mat
    noteNumDifference = abs(len(LmatPitches)-len(SmatPitches)) #this is here for setting the firstExpansionRepresentation variable
    
    #find LmatNoteIntervals
    LmatNoteIntervals = [x - y for y, x in zip(LmatPitches, LmatPitches[1:])]

    #find unique expansions of (shorter mat notes) that match length of (longer mat notes)
    firstExpansionRepresentation = [np.nan]*len(SmatPitches)+[(r+1)/100 for r in list(range(noteNumDifference))] #notes are whole numbers, so this is fine
    allPerms = list(itertools.permutations(firstExpansionRepresentation))
    uniquePerms = [np.array(s) for s in list(set(allPerms))]
    #replace nan values with SmatPitches values
    for t in range(len(uniquePerms)):
        uniquePerms[t][np.isnan(uniquePerms[t])] = SmatPitches #replace nan elements with SmatPitches
        uniquePerms[t][np.array([cc%1 != 0 for cc in uniquePerms[t]])] = np.nan #replace non-whole number elements with nans
    uniquePerms = [tuple(u) for u in uniquePerms]

    #replace nans with all nearest-possibilities based on outer elements, minizing Euclidean distance
    allPossibilities = {dd: [] for dd in uniquePerms} #dictionary to keep track of possibility changes
    for ee in range(len(uniquePerms)): #go thru each outer possibility
        nanPositions = list(np.argwhere(np.isnan(list(uniquePerms[ee]))).flatten()) #different for each key
        nanPositions = [list(ff) for ff in more_itertools.consecutive_groups(nanPositions)] #group together consecutive positions
        bestNoteChangePositions = [] #in interval units, changes
        for gg in nanPositions: #remember: nanPositions is a nested list, so this selects each group; nanPositions contains indices
            if 0 in gg: #if includes beginning
                bestNoteChangePositions.append(gg) #append beginning range
            if 0 not in gg and len(uniquePerms[0])-1 not in gg: #if not at beginning or end
                LIntervalSub = LmatNoteIntervals[gg[0]-1:gg[-1]] #a group, g[-1] refers to lengths units, g[-1]+1 refers to intervals units
                if (uniquePerms[ee][gg[-1]+1])-(uniquePerms[ee][gg[0]-1]) == 0:
                    bestNoteChangePositions.append([gg[0]]) #append first cause it doesn't matter which one you choose
                if (uniquePerms[ee][gg[-1]+1])-(uniquePerms[ee][gg[0]-1]) > 0:
                    bestNoteChangePositions.append([gg[LIntervalSub.index(max(LIntervalSub))]])
                if (uniquePerms[ee][gg[-1]+1])-(uniquePerms[ee][gg[0]-1]) < 0:
                    bestNoteChangePositions.append([gg[LIntervalSub.index(max(LIntervalSub))]])
            if len(uniquePerms[0])-1 in gg: #append ending range
                bestNoteChangePositions.append(gg)
        allPossibilities[uniquePerms[ee]] = bestNoteChangePositions

    #print(allPossibilities) #for debugging, example: {(nan, nan, -3, nan, nan, -10): [[0, 1], [4]]}

    #convert note changes into dict of (value) lists
    allLists = {jj: list(jj) for jj in uniquePerms}
    for hh in range(len(uniquePerms)):
        nanPositions = list(np.argwhere(np.isnan(list(uniquePerms[hh]))).flatten()) #different for each key
        nanPositions = [list(kk) for kk in more_itertools.consecutive_groups(nanPositions)] #group together consecutive positions
        for ii in allPossibilities[uniquePerms[hh]]: #going through each value in allPossibilities
            if 0 in ii:
                allLists[uniquePerms[hh]][0:ii[-1]+1] = (ii[-1]+1)*[allLists[uniquePerms[hh]][ii[-1]+1]]
            elif len(uniquePerms[0])-1 in ii:
                allLists[uniquePerms[hh]][ii[0]:len(uniquePerms[0])] = (len(uniquePerms[0])-ii[0])*[allLists[uniquePerms[hh]][ii[0]-1]]
            else: #if group is in the middle
                whichMiddle = [ii[0] in nanPositions[ll] for ll in range(len(nanPositions))].index(True) #find which group in nanPositions contains the note change index
                replacementList = ((ii[0]+1)-nanPositions[whichMiddle][0])*[allLists[uniquePerms[hh]][nanPositions[whichMiddle][0]-1]] + (nanPositions[whichMiddle][-1]-(ii[0]))*[allLists[uniquePerms[hh]][nanPositions[whichMiddle][-1]+1]]
                allLists[uniquePerms[hh]][nanPositions[whichMiddle][0]:nanPositions[whichMiddle][-1]+1] = replacementList

    #find which value of dict allLists minimizes the Euclidean distance
    EuclideanDistances = []
    for mm in uniquePerms:
        currentList = allLists[mm]
        testNoteIntervals = [nn - oo for oo, nn in zip(currentList, currentList[1:])]
        EuclideanDistances.append(math.sqrt(sum([(LmatNoteIntervals[pp]-testNoteIntervals[pp])**2 for pp in range(len(LmatNoteIntervals))])))

    #get list with the smallest note interval Euclidean Distance and set to SmatPitches
    SmatPitches = allLists[uniquePerms[EuclideanDistances.index(min(EuclideanDistances))]]

    #change time matrix
    tempSmatLengths = np.array([np.nan]*len(LmatLengths))
    keyConfiguration = list(uniquePerms[EuclideanDistances.index(min(EuclideanDistances))])
    tempSmatLengths[~np.isnan(keyConfiguration)] = SmatLengths #replace numbers in expanded matrix by SmatLengths
    tempSmatLengths[np.isnan(keyConfiguration)] = 0
    SmatLengths = list(tempSmatLengths)

    return LmatPitches, LmatLengths, SmatPitches, SmatLengths

def MFE(tuneFilename, participantFilename):
    #######load data##############
    #tune data
    print('Original tune filename: '+tuneFilename)
    Omatfilename = tuneFilename
    OmatString = open(Omatfilename,"r").read()
    preProcessedOmatString = [a.strip().split(' ') for a in OmatString[5:-1].split(';')]
    OmatPitches = [float(preProcessedOmatString[0][b]) for b in range(len(preProcessedOmatString[0]))]
    OmatLengths = [float(preProcessedOmatString[1][c]) for c in range(len(preProcessedOmatString[1]))]

    #participant data
    print('Participant filename: '+participantFilename)
    Pmatfilename = participantFilename
    PmatString = open(Pmatfilename,"r").read()
    preProcessedPmatString = [d.strip().split(' ') for d in PmatString[5:-1].split(';')]
    PmatPitches = [float(preProcessedPmatString[0][e]) for e in range(len(preProcessedPmatString[0]))]
    PmatLengths = [float(preProcessedPmatString[1][f]) for f in range(len(preProcessedPmatString[1]))]

    #######preprocess pitch data########
    #tune
    OmatPitches = [math.floor((24*(math.log(g/440)/math.log(2))+1)/2) for g in OmatPitches]

    #patient
    PmatPitches = [math.floor((24*(math.log(h/440)/math.log(2))+1)/2) for h in PmatPitches]

    #######Assessments##################
    if len(OmatPitches) == len(PmatPitches):
        noteNumDifference = 0
        noteIntervalError, rhythmError = sameNumNotes(OmatPitches, OmatLengths, PmatPitches, PmatLengths)
        print('Number of notes added/deleted: 0')
    elif len(OmatPitches) > len(PmatPitches):
        noteNumDifference = len(PmatPitches)-len(OmatPitches)
        OmatPitches, OmatLengths, PmatPitches, PmatLengths = diffNumNotes(OmatPitches, OmatLengths, PmatPitches, PmatLengths) #get minimized Euclidean Distance variables, setting Omat to Lmat
        noteIntervalError, rhythmError = sameNumNotes(OmatPitches, OmatLengths, PmatPitches, PmatLengths)
        print('Number of notes added/deleted: '+str(noteNumDifference))
    elif len(OmatPitches) < len(PmatPitches):
        noteNumDifference = len(PmatPitches)-len(OmatPitches)
        PmatPitches, PmatLengths, OmatPitches, OmatLengths = diffNumNotes(PmatPitches, PmatLengths, OmatPitches, OmatLengths) #setting Pmat to Lmat
        noteIntervalError, rhythmError = sameNumNotes(PmatPitches, PmatLengths, OmatPitches, OmatLengths)
        print('Number of notes added/deleted: '+str(noteNumDifference))

    return noteIntervalError, rhythmError, noteNumDifference