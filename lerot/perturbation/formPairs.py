"""
This function forms pairs of indices according to 
the raman et al. 2013 paper for 3PR

@Params: length
@returns: paired indices list 
"""
import random as rnd

def formPairs(length):
    # Init flag for single item that needs addition to paired_indeces
    has_one = True
    if length % 2 == 0:
         has_one = False

    # p=0.5 for not using singular starter
    if rnd.randint(0,1):
        paired_indices = []
    
    # Else, assign singular starter, swap flag
    else:
        paired_indices = [(0,)]
        has_one = not has_one

    # Gather all pairs of 2 that have no item in indices yet    
    for i in xrange(len(paired_indices),length-1,2):
        paired_indices.append((i, i+1))
    
    # Add last index if it hasn't been added yet
    if has_one:
        paired_indices.append((length-1,))

    return paired_indices