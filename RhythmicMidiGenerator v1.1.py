# -*- coding: utf-8 -*-
"""

@author: prod_emdub

Version 1.1


This program will generate a 4 chord progression in all major keys with 
a random rhythmic sequence

BEFORE USING YOU MUST INSTALL MIDI UTIL >> pip install MIDIUtil

Info about this package can be found at: https://pypi.org/project/MIDIUtil/

Output directory must be edited on line 218
"""

from midiutil import MIDIFile
import random


#######################################################################             

def rand_dur():
    
    """ 
    Duration Default: Quarter Note
    
    Here a random list will be created with 4 elements. Each of the elements
    will have a sub list containing randomly generated rhythmic sequences.
    Only 2 of the 4 elemets are generated, then they are repeated to create
    some sort of rhythmic repition
    
    Example: A list will look like this: 
            [[0.5, 2.5], [2, 1, 1, 0.5, 0.5], [0.5, 2.5], [2, 1, 1, 0.5, 0.5]]
            
    
    Within the first subunit, the chord will play for 0.5 notes then again
    for 2.5 notes, totaling to 3. Within the 2nd subunit, that chord will play
    for 2 notes, then 1 note, then 1 note, then 0.5 notes, then 0.5 notes, totaling 
    to 5. Each set of 2 subunits will add to 8, and the list total will be
    16, representing the 16 notes in a 4 bar loop    
    """
    
    #initialize blank duration list for the 4 chords, each will be made up of 
    #rhythmic subunits
    dur = []
    
    #define possible chord durations
    possible_chord_durs = [3, 4, 5]
    
    #define possible rhythmic subunit durations
    possible_rhy_durs = [0.5,1,1.5,2,2.5,3]
    
    #for 2 sublists in dur list, add chords + rhythm
    for i in range(2):
        
        #assignn x to random chord duration        
        #for 2nd and 4th chords, make sure chord dur adds to 8
        if (i == 1):
            x = 8 - sum(dur[0])
        
        #for the 1st chords
        else:
            x = random.choice(possible_chord_durs)

        #initilize sublist outside of while loop so it clears each for loop 
        rhy_sublist = []
        
        #while loop to add each rhythmic subset dur to dur list
        while (x > 0):
            
            #randomly select rhy dur
            z = random.choice(possible_rhy_durs)
            
            #if the selected rhy dur does not add up to the selected chord dur, retry
            if (x - z < 0):
                continue
            
            #add the rhy dur to the sublist if accepted
            else:
                rhy_sublist.append(z)
                
                #subtract selected rhy dur from chord dur to eventually get to 0
                #to stop while loop
                x = x - z
                
        #add the sublist to the dur list so that the 2 bars are repeated
        dur.append(rhy_sublist)
    
    #copy the 2 rhythms 
    dur.append(dur[0])
    dur.append(dur[1])

    return dur
            
#######################################################################
    
def major_chord_prog():
    
    """
    This method is responsible for generating a random progression in a major
    key (c maj by default, the notes are changed in the file_writer() method)
    The 3 notes of every chord in c maj are given in a list, and 4 are chosen
    at random to be added to a list and returned as the chord progression
    """
    
    #define each numbered chord based on note location number
    #C maj is default
    default_chords = [[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72], [67, 71, 74], [69, 72, 76], [71, 74, 77]]
                   
    #initialize list of random progression
    rand_progression = []
    rand_progression_fin = []
        
    #while the list has less than 4 elements in it, keep running to add elements
    while (len(rand_progression_fin) < 4):
    
        #send x to a random index from the list
        x = random.choice(range(0,7))
                
        #add to the list from the index of c maj chords
        rand_progression.append(default_chords[x])
                
        #iterate through each element of the created list. Try and add element to new list
        #if element already in new list, do not add, while loop will add another
        for i in rand_progression:
            if i not in rand_progression_fin:
                rand_progression_fin.append(i)
    return rand_progression_fin
                        
###########################################################################


def file_writer():
    
    """
    This method will write the files for the midis. 
    
    For each midi file that is created, it needs to be created as a MidiFile(),
    and given track, channel, pitch, time, duration, and volume parameters. Notes
    are added with the (midi).addNote function.
    
    File name will change based on what iteration of loop it is on. 1st iteration:
    c_maj, 4th iteration: d#_maj, etc. 
    
    The note adding section will take the first element of the chord list and add those
    notes to the midi file, with length of that chord defined by the duration
    sub lists.
    """
        
    list_of_chords = ["c_maj", "c#_maj","d_maj", "d#_maj","e_maj", "f_maj","f#_maj", "g_maj","g#_maj", "a_maj","a#_maj", "b_maj"]
   
    for chord in range(len(list_of_chords)):
  
        # get unique chord progression from method
        maj_ch_pr = major_chord_prog()
        
        #change note number based on progression (C# maj + 1, d maj +2, etc)
        for q in range(len(maj_ch_pr)):
            for k in range(len(maj_ch_pr[q])):
            
                #here is where notes are changed
                maj_ch_pr[q][k] += chord
        
        #initialize to keep track of total time, needs to add to 16
        tot_duration_time = 0
        
        #note chord name
        chord_name = list_of_chords[chord]
            
        #create the midi file      
        MyMIDI = MIDIFile(1)
                        
            #returns a list of 4 note durations from method with rhy sublists
        note_durations = rand_dur()
        
        #for each item in the chord list for the 4 created chords
        for k in range(4):
            degrees = maj_ch_pr[k] #what notes will be played in the chord
            track = 0 #likely arbitrary 
            channel  = 0 #color in fl
            time     = 0    # In beats (Where it starts)
            volume   = 100  # 0-127, as per the MIDI standard
            
            #for loop below this, keep track of if it is the first time or not
            if k == 0:
                first_chord = True
            else:
                first_chord = False
            
            #starting with the length of the first rhy subunit, add each one to midi
            for s in range(len(note_durations[k])):
                
                #note duration will be the s element of the k subunit
                duration = note_durations[k][s]
                
                          
                #for the first time through, disreagard adding time
                if (first_chord and s == 0):
                    for j, pitch in enumerate(degrees):
                        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                        
                #for subsequent times, add sum of previous durations to time
                else:
                    for j, pitch in enumerate(degrees):
                        MyMIDI.addNote(track, channel, pitch, time + tot_duration_time, duration, volume)
    
                #to keep track of what time to add, sum the duration
                #this sums each note time of the sublist, summing to 16
                tot_duration_time += duration
         
        """
        EDIT DIRECTORY HERE \/
        """       
        #write the midi file
        with open("dir/dir/dir"+chord_name+"_prog.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
                
###########################################################################

def main():
    file_writer()  

###########################################################################

if __name__ == "__main__":
    main()
    print("Midis successfully created. Check directory")
        
            
 

