"""
This function forms pairs of indices according to 
the raman et al. 2013 paper for 3PR

Takes length
returns paired indices list 
"""

def formPairs(length):
	paired_indices = []
	# If even, go from the start and form pairs
	if length % 2 == 0:
		for i in xrange(0,length-1,2):
			paired_indices.append([i, i+1])
    # Uneven, take the first number on it's own pair the rest
	else:
		paired_indices = [[1]]
		for i in xrange(1,length-1,2):
			paired_indices.append([i, i+1]) 
	return paired_indices