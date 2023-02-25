import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from numba import jit
from numba import njit, prange
import math

def generate_position_array():
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
    prev_freq = frequency_array[0, :, :]
    updated_array = determine_position_score(prev_freq, score_position_array, score_number_array, score, position)
    
    return updated_array
   
def update_one_dart(prev_freq, determine_position_score, score_position_array, score_number_array, score, position):
    updated_array = determine_position_score(prev_freq, score_position_array, score_number_array, score, position)
    
    return updated_array

def generate_frequency_array(df, score_position_array, score_number_array):
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
