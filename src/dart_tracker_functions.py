import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from numba import jit
from numba import njit, prange
import math

def generate_position_array():

    '''used to generate a 2D array to determine the poisition of each section of a standard dart board. The array is 400x450 with the center of the board being located at [200, 200]. 
    The extra space is used to generate boxes to visualize if a dart is thrown out of bounds of bounces off the board. The values that represent each section are listed in the function.
    The original array contains all zeros which are then replaced by values representing each different section of a dart board.
    
    There are no inputs for this function. The user only needs to run it and everything is self contained
    
    outputs:
        score_position_array: 400x450 array representing different sections of a dart board'''


    score_position_array = np.zeros((400, 450))

    #cm distances that darts rings are found
    radius_distance_list = [178, 170, 107, 99, 19, 7.5]

    #giving each distance ring a specific value
    #0=boarder, 0.2=x2, 0.8=outside, 0.3=x3, 0.1=inside, 0.25=outer_ring, 0.5=bullseye
    radius_value_list = [0.2, 0.8, 0.3, 0.1, 0.25, 0.5]

    #filling the array with distances values based on radii from the center 
    for k in range(len(radius_distance_list)):
        distance = radius_distance_list[k]
        for i in range(len(score_position_array[0, :])):
            for j in range(len(score_position_array[:, 0])):
                y_dis = i-200
                x_dis = j-200
                radius = np.sqrt(y_dis**2 + x_dis**2)
                if radius<distance:
                        score_position_array[i, j] = radius_value_list[k]
                        
    #making boxes for out of bounds and bounce
    #ofb = 0.7, bouce = 0.99
    score_position_array[20:70, 380:430] = 0.7
    score_position_array[330:380, 380:430] = 0.99


    return score_position_array

def generate_number_array():

    '''used to generate a 2D array to determine the number score of each section of a standard dart board. The array is 400x450 with the center of the board being located at [200, 200]. 
    The values that represent each numbered section is the normal value found on the dart board except for the bullseye, outter bullseye, out of bounds, or a bounce, which are represented by zero.
    The original array contains all zeros which are then replaced by values representing each different section of a dart board.
    
    There are no inputs for this function. The user only needs to run it and everything is self contained
    
    outputs:
        score_number_array: 400x450 array representing different numbered sections of a dart board'''

    score_number_array = np.zeros((400, 450))

    #creating the second layer of the array to represent positional value
    #each section is 18 degrees
    #goes through four quadrants counterclockwise
    #eaach section assigned its own number corresponding to dart board numbers

    for i in range(len(score_number_array[:, 0])):
        for j in range(len(score_number_array[:, 0])):

            #going through quadrant 1
            if j>=200 and i<=199:
                opposite = 200 - i
                adjacent = j - 199
                iso_angle = math.degrees(math.atan(opposite/adjacent))
                if iso_angle>=0 and iso_angle<9:
                    score_number_array[i, j] = 6
                if iso_angle>=9 and iso_angle<27:
                    score_number_array[i, j] = 13
                if iso_angle>=27 and iso_angle<45:
                    score_number_array[i, j] = 4
                if iso_angle>=45 and iso_angle<63:
                    score_number_array[i, j] = 18
                if iso_angle>=63 and iso_angle<81:
                    score_number_array[i, j] = 1
                if iso_angle>=81 and iso_angle<90:
                    score_number_array[i, j] = 20
                
            #going through quadrant 2
            if j<200 and i<=199:
                opposite = 200 - i
                adjacent = 200 - j 
                iso_angle = math.degrees(math.atan(opposite/adjacent))
                if iso_angle>=81 and iso_angle<90:
                    score_number_array[i, j] = 20
                if iso_angle>=63 and iso_angle<81:
                    score_number_array[i, j] = 5
                if iso_angle>=45 and iso_angle<63:
                    score_number_array[i, j] = 12
                if iso_angle>=27 and iso_angle<45:
                    score_number_array[i, j] = 9
                if iso_angle>=9 and iso_angle<27:
                    score_number_array[i, j] = 14
                if iso_angle>=0 and iso_angle<9:
                    score_number_array[i, j] = 11

            #going through quadrant 3           
            if j<200 and i>199:
                opposite = i - 200
                adjacent = 200 - j 
                iso_angle = math.degrees(math.atan(opposite/adjacent))
                if iso_angle>=0 and iso_angle<9:
                    score_number_array[i, j] = 11
                if iso_angle>=9 and iso_angle<27:
                    score_number_array[i, j] = 8
                if iso_angle>=27 and iso_angle<45:
                    score_number_array[i, j] = 16
                if iso_angle>=45 and iso_angle<63:
                    score_number_array[i, j] = 7
                if iso_angle>=63 and iso_angle<81:
                    score_number_array[i, j] = 19
                if iso_angle>=81 and iso_angle<90:
                    score_number_array[i, j] = 3         
                
                
            #going through quadrant 4    
            if j>=200 and i>199:
                opposite = i - 200
                adjacent = j - 199
                iso_angle = math.degrees(math.atan(opposite/adjacent))
                if iso_angle>=81 and iso_angle<90:
                    score_number_array[i, j] = 3
                if iso_angle>=63 and iso_angle<81:
                    score_number_array[i, j] = 17
                if iso_angle>=45 and iso_angle<63:
                    score_number_array[i, j] = 2
                if iso_angle>=27 and iso_angle<45:
                    score_number_array[i, j] = 15
                if iso_angle>=9 and iso_angle<27:
                    score_number_array[i, j] = 10
                if iso_angle>=0 and iso_angle<9:
                    score_number_array[i, j] = 6

    return score_number_array

def generate_outline_array(score_position_array, score_number_array):

    '''Uses the score_position_array and score_number_array to generate an outline of the dartboard for visualization purposes. First, two zero arrays of the same size as the score_position_array
    and score_number_array are generated. This function then goes through both arrays, one number at a time.  If that number is the same as the numbers directly below, above, to the left, 
    and to the right, the zero in the same position on the new array stays zero. If htis is not the case, this signifies that that number sits in a transition position between sections or numbers and 
    therefore the zero in the same position on the new array becomes 1. These two arrays are then combined and a combined_array is made, coordinates are pulled, and these can be used to 
    plot the dart board boarders in later functions.
    
    Inputs:
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board
    
    outputs:
        y_coords: first dimension coodrinates for where dart board sections are located. Used to visually show dart board sections when generating a heatmap.
        x_coords: second dimension coodrinates for where dart board sections are located. Used to visually show dart board sections when generating a heatmap.'''

    
    position_outline_array = np.zeros((400, 450))
    for i in range(len(score_position_array[10:440, 0])-1):
        for j in range(len(score_position_array[0, 10:440])-1):
            position = score_position_array[i+10, j+10]
            
            up = score_position_array[i+9, j+10]
            down = score_position_array[i+11, j+10]
            left = score_position_array[i+10, j+9]
            right = score_position_array[i+10, j+11]

            if up != position:
                position_outline_array[i+10, j+10] = 1
            if down != position:
                position_outline_array[i+10, j+10] = 1
            if left != position:
                position_outline_array[i+10, j+10] = 1
            if right != position:
                position_outline_array[i+10, j+10] = 1
                        
                        

    score_outline_array = np.zeros((400, 450))
    for i in range(len(score_number_array[10:390, 0])):
        for j in range(len(score_number_array[0, 10:390])):
            position = score_number_array[i+10, j+10]
            
            up = score_number_array[i+9, j+10]
            down = score_number_array[i+11, j+10]
            left = score_number_array[i+10, j+9]
            right = score_number_array[i+10, j+11]
            if up != position:
                score_outline_array[i+10, j+10] = 1
            if down != position:
                score_outline_array[i+10, j+10] = 1
            if left != position:
                score_outline_array[i+10, j+10] = 1
            if right != position:
                score_outline_array[i+10, j+10] = 1
    centerpoint = 199
    for i in range(len(score_outline_array[:, 0])):
        for j in range(len(score_outline_array[0, :])):
            radius = np.sqrt((i - centerpoint)**2 + (j - centerpoint)**2)
            if radius > 178 or radius < 19:
                score_outline_array[i, j] = 0
            
    combined_array = score_outline_array + position_outline_array

    melded_array = np.zeros((400, 450))
    for i in range(len(score_outline_array[:, 0])):
        for j in range(len(score_outline_array[0, :])):
            if combined_array[i, j] > 0:
                melded_array[i, j] = 1

    y_coords, x_coords = np.where(melded_array == 1)
    return y_coords, x_coords


@jit(nopython=True)
def determine_position_score(prev_freq, score_position_array, score_number_array, score, position):

    '''Used in the update_first_dart and update_one_dart function. Used to go through each "throw" represented in the csv file containing dart throw data.
    Determines what position and what number value section each dart belongs to.
    
    Inputs:
        prev_freq: array that is used to start the heatmap. Since this is the first dart throw, the array is unaltered and all zeros.
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board
        score: value from the csv dart data file that represents what section number wise the dart landed in.
        position: value from the csv dart data file that represents what section position wise the dart landed in.
    
    outputs:
        prev_freq: 2D array that has the dartboard updated with what section the first dart was thrown into.'''

    for i in range(len(prev_freq[:, 0])):
        for j in range(len(prev_freq[0, :])):
            if position == 0.25 or position == 0.5:
                if score_position_array[i, j] == position:
                    prev_freq[i, j] +=1 

            if position == 0.7 or position == 0.99:
                if score_position_array[i, j] == position:
                    prev_freq[i, j] +=1 
            else:
                if score_position_array[i, j] == position:
                    if score_number_array[i, j] == score:
                        prev_freq[i, j] +=1
    return prev_freq
    
def update_first_dart(frequency_array, determine_position_score, score_position_array, score_number_array, score, position):

    '''Used to update the frequency array for the first dart throw. This function works closly with determine_position_score. 

    Inputs:
        frequency_array: 3D array. 1st dimension represents the entire dart board for one throw. Other two dimensions are the x,y coordinates for each dart board section.
        determine_position_score: function used to go through one 2D array (representing one dart throw) within the frequency_array and update that array.
        prev_freq: array that is used to start the heatmap. Since this is the first dart throw, the array is unaltered and all zeros.
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board
        score: value from the csv dart data file that represents what section number wise the dart landed in.
        position: value from the csv dart data file that represents what section position wise the dart landed in.
    
    outputs:
        updated_array: 3D array that has the dartboard updated with what section the first dart was thrown into.'''
    
    prev_freq = frequency_array[0, :, :]
    updated_array = determine_position_score(prev_freq, score_position_array, score_number_array, score, position)
    
    return updated_array
   
def update_one_dart(prev_freq, determine_position_score, score_position_array, score_number_array, score, position):

    '''Used to update the frequency array for the all darts thrown after the first dart. This function works closly with determine_position_score. 

    Inputs:
        frequency_array: 3D array. 1st dimension represents the entire dart board for one throw. Other two dimensions are the x,y coordinates for each dart board section.
        determine_position_score: function used to go through one 2D array (representing one dart throw) within the frequency_array and update that array.
        prev_freq: array that is used to start the heatmap. Since this is the first dart throw, the array is unaltered and all zeros.
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board
        score: value from the csv dart data file that represents what section number wise the dart landed in.
        position: value from the csv dart data file that represents what section position wise the dart landed in.
    
    outputs:
        updated_array: 3D array that has the dartboard updated with what section that each dart was thrown into.'''
    


    updated_array = determine_position_score(prev_freq, score_position_array, score_number_array, score, position)
    
    return updated_array

def generate_frequency_array(df, score_position_array, score_number_array):

    '''Used to generate and update a 3D frequency array based on the raw dart throwing data. The first dimension represents each thrown dart. The last two dimensions
    represent the x, y coordinates for each dart section represented by the score_poisition_array and score_number_array 

    Inputs:
        df: dataframe generated from the csv file containing the dart throwing data.
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board

    
    outputs:
        frequency_array: 3D array that has all dartboard data added. Each level of the first demension represents a subsequent dart being thrown and the array usdated to reflect that'''

    #go through each throw and update the array
    #each array (first dimension) reflects one throw
    frequency_array = np.zeros((len(df), 400, 450))
    for a in range(len(frequency_array[:, 0, 0])):
        position = df.iloc[a][3]
        score = df.iloc[a][4]

        #needs a separate step since there is no previous array to be updated
        if a == 0:
            one_dart_update = update_first_dart(frequency_array, determine_position_score, score_position_array, score_number_array, score, position)

        #uses the previous array (first dimension) and updates it with the next dart thrown
        else:
            one_dart_update = update_one_dart(frequency_array[a-1, :, :], determine_position_score, score_position_array, score_number_array, score, position)
        frequency_array[a, :, :] = one_dart_update
        
    return frequency_array


def generate_images(df, frequency_array, boarders_y_coords, boarders_x_coords, directory):

    '''Used to generate images that can be used to generate a movie showing a progressive heatmap. Each dart throw (first dimension of the frequency_array) has its 2D x,y coordinate array
    converted into an image that is then saved in a specificed directory.

    Inputs:
        df: dataframe generated from the csv file containing the dart throwing data.
        score_position_array: 400x450 array representing different sections of a dart board
        score_number_array: 400x450 array representing different numbered sections of a dart board
        boarders_y_coords: first dimension coodrinates for where dart board sections are located. Used to visually show dart board sections when generating a heatmap.
        boarders_x_coords: second dimension coodrinates for where dart board sections are located. Used to visually show dart board sections when generating a heatmap.
        directory: path and file name of where the images are to be saved'''
    
    mode_position = df['position'].value_counts()
    mode_number = df['score'].value_counts()

    #determining if the mode is a a score coded with 0.0
    #if it is, that value frequency becomes the ceiling
    if mode_position.index[0] in [0.25, 0.50, 0.70, 0.99]:
        ceiling_value = mode_position.iloc[0]

    #if the most often is one of the 1-20 scores, this is how the ceiling is determiend
    else:
        if mode_number.index[0] == 0.0:
            ceiling_value = mode_number.iloc[1] 
        else:
            ceiling_value = mode_number.iloc[0] 
    
    iteration = 0 #used to lable images in ascending order
    for i in range(len(frequency_array[:, 0, 0])):
        fig, ax = plt.subplots()
        im = ax.imshow(frequency_array[i, :, :], vmin=0, vmax=ceiling_value, cmap='jet')
        ax.scatter(boarders_x_coords, boarders_y_coords, s=0.1, color='white')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(str(directory)+str(iteration)+'.jpeg', dpi = 300,  bbox_inches="tight")
        iteration += 1
