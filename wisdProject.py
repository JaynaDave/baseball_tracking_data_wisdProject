import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
import sys

from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.axes3d import *
from matplotlib import cm



def plot_hits(name, hits, ss_hits):
    fig = plt.figure(name)
    ax = fig.add_subplot(projection='3d')

    #home plate origin reference point
    ax.scatter( 0, 0, 0, marker="D", label="Home Plate (origin)")

    for p in hits:
        ax.scatter(p[0], p[1], p[2], marker="o", color='g')

    for p in ss_hits:
        ax.scatter(p[0], p[1], p[2], marker="o", color='r')

    ax.scatter([], [], [],marker="o", color='g', label='Hit' )
    ax.scatter([], [], [],marker="o", color='r', label="'sweet spot' Hit" )
    ax.legend()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


  


def find_closest(lst, k):
    closest_num = lst[0].get('time')
    for ballData in lst:
        num = ballData.get('time')
        if abs(num - k) < abs(closest_num - k):
            closest_num = num
        if num > k:
            break
    #print("closest time  ", closest_num)
    return ballData.get('pos')

datalist = []
fastball = []
slider = []
sinker = []
changeup = []
curveball = []
other = []

fn = sys.argv[1]
if os.path.exists(fn):
    print (os.path.basename(fn))
else:
    print ("file path error")

path = fn
for filename in glob.glob(os.path.join(path, '*.jsonl')): #only process .JSON files in folder.      
    with open(filename, encoding='utf-8', mode='r') as json_file:
        bd = json.load(json_file)
        #print ("loading file...")
        datalist.append(bd)
        #bd.pop('samples_ball')
        #bd.pop('samples_bat')
        #print(bd.get('events'))
        #print(((bd.get('summary_acts')).get('pitch')).get('type'))
        
        pitchtype = ((bd.get('summary_acts')).get('pitch')).get('type')
        if pitchtype == 'FourSeamFastball':
            fastball.append(bd)
        elif pitchtype == 'Curveball':
            curveball.append(bd)
        elif pitchtype == 'Sinker':
            sinker.append(bd)
        elif pitchtype == 'Slider':
            slider.append(bd)
        elif pitchtype == 'Changeup':
            changeup.append(bd)
        else:
            other.append(bd)


fb_noswings = 0 
fb_swung = []
for fb in fastball:
  
    if ((fb.get('summary_acts')).get('pitch')).get('action') == 'Called':
        fb_noswings += 1 
    else:
        fb_swung.append(fb) 

fb_hits = 0
fb_ss_hit = 0
fb_hit_positions = []
fb_ss_positions = []
for swing in fb_swung:
    if swing.get('events'):
        fb_hits += 1

        ballPos = None 
        for item in (swing.get('samples_bat')):
                if item.get('event') == 'Hit':
                    hitTime = item.get('time')
                    ballPos = find_closest(swing.get('samples_ball'), hitTime)


        launch_angle = ((swing.get('events'))[0].get('start')).get('angle')[1]
        if (8 <= launch_angle <= 32):
            fb_ss_hit += 1
            if ballPos:
                fb_ss_positions.append(ballPos)
                    #find ball position at hit time
        else:
            if ballPos:
                fb_hit_positions.append(ballPos)

plot_hits('Fastball Hits', fb_hit_positions,fb_ss_positions)

print("FourSeamFastball\n")

print("hits   ", fb_hits)
print("'sweet spot' hits ", fb_ss_hit)
#print(fb_ss_positions)

if len(fastball) > 0: 
        
    print ("Percentage Swung: ",  1 - (fb_noswings/(len(fastball))))
    print ("Percentage hit out of swung: ", fb_hits/(len(fastball)-fb_noswings))
    print ("Percentage 'sweet spot' hits of hits: ",  fb_ss_hit/fb_hits)
    print ("Percentage hit overall: ", fb_hits/(len(fastball)))

print("\n")


sinker_noswings = 0 
sinker_swung = []
for sb in sinker:
    #print (((sb.get('summary_acts')).get('pitch')).get('action'))
    if ((sb.get('summary_acts')).get('pitch')).get('action') == 'Called':
        sinker_noswings += 1 
    else:
        sinker_swung.append(sb)


sinker_hits = 0
sinker_ss_hit = 0
sinker_hit_positions = []
sinker_ss_positions = []
for swing in sinker_swung:
    if swing.get('events'):
        sinker_hits += 1\

        ballPos = None
        for item in (swing.get('samples_bat')):
            if item.get('event') == 'Hit':
                hitTime = item.get('time')
                ballPos = find_closest(swing.get('samples_ball'), hitTime)   
                    
        launch_angle = ((swing.get('events'))[0].get('start')).get('angle')[1]
        if (8 <= launch_angle <= 32):
            sinker_ss_hit += 1
            if ballPos:
                sinker_ss_positions.append(ballPos)
        else:
            if ballPos:
                sinker_hit_positions.append(ballPos)
            
plot_hits('Sinker Hits', sinker_hit_positions,sinker_ss_positions)                 

print("Sinker\n")

print("hits   ", sinker_hits)
print("'sweet spot' hits ", sinker_ss_hit)
#print(fb_ss_positions)

if len(sinker) > 0: 
        
    print ("Percentage Swung: ",  1 - (sinker_noswings/(len(sinker))))
    print ("Percentage hit out of swung: ", sinker_hits/(len(sinker)-sinker_noswings))
    print ("Percentage 'sweet spot' hits of hits: ",  sinker_ss_hit/sinker_hits)
    print ("Percentage hit overall: ", sinker_hits/(len(sinker)))

print("\n")


slider_noswings = 0 
slider_swung = []
for sb in slider:
    #print (((sb.get('summary_acts')).get('pitch')).get('action'))
    if ((sb.get('summary_acts')).get('pitch')).get('action') == 'Called':
        slider_noswings += 1 
    else:
        slider_swung.append(sb)

slider_hits = 0
slider_ss_hit = 0
slider_hit_positions = []
slider_ss_positions = []
for swing in slider_swung:
    if swing.get('events'):
        slider_hits += 1\

        ballPos = None
        for item in (swing.get('samples_bat')):
            if item.get('event') == 'Hit':
                hitTime = item.get('time')
                ballPos = find_closest(swing.get('samples_ball'), hitTime)   
                    
        launch_angle = ((swing.get('events'))[0].get('start')).get('angle')[1]
        if (8 <= launch_angle <= 32):
            slider_ss_hit += 1
            if ballPos:
                slider_ss_positions.append(ballPos)
        else:
            if ballPos:
                slider_hit_positions.append(ballPos)
            
plot_hits('Slider Hits', slider_hit_positions,slider_ss_positions)                 

print("Slider\n")

print("hits   ", slider_hits)
print("'sweet spot' hits ", slider_ss_hit)
#print(fb_ss_positions)

if len(slider) > 0: 
        
    print ("Percentage Swung: ",  1 - (slider_noswings/(len(slider))))
    print ("Percentage hit out of swung: ", slider_hits/(len(slider)-slider_noswings))
    print ("Percentage 'sweet spot' hits of hits: ",  slider_ss_hit/slider_hits)
    print ("Percentage hit overall: ", slider_hits/(len(slider)))

print("\n")


changeup_noswings = 0 
changeup_swung = []
for sb in changeup:
    #print (((sb.get('summary_acts')).get('pitch')).get('action'))
    if ((sb.get('summary_acts')).get('pitch')).get('action') == 'Called':
        changeup_noswings += 1 
    else:
        changeup_swung.append(sb)

changeup_hits = 0
changeup_ss_hit = 0
changeup_hit_positions = []
changeup_ss_positions = []
for swing in changeup_swung:
    if swing.get('events'):
        changeup_hits += 1\

        ballPos = None
        for item in (swing.get('samples_bat')):
            if item.get('event') == 'Hit':
                hitTime = item.get('time')
                ballPos = find_closest(swing.get('samples_ball'), hitTime)   
                    
        launch_angle = ((swing.get('events'))[0].get('start')).get('angle')[1]
        if (8 <= launch_angle <= 32):
            changeup_ss_hit += 1
            if ballPos:
                changeup_ss_positions.append(ballPos)
        else:
            if ballPos:
                changeup_hit_positions.append(ballPos)
            
plot_hits('Changeup Hits', changeup_hit_positions,changeup_ss_positions)                 

print("Changeup\n")

print("hits   ", changeup_hits)
print("'sweet spot' hits ", changeup_ss_hit)
#print(fb_ss_positions)

if len(changeup) > 0: 
        
    print ("Percentage Swung: ",  1 - (changeup_noswings/(len(changeup))))
    print ("Percentage hit out of swung: ", changeup_hits/(len(changeup)-changeup_noswings))
    print ("Percentage 'sweet spot' hits of hits: ",  changeup_ss_hit/changeup_hits)
    print ("Percentage hit overall: ", changeup_hits/(len(changeup)))

print("\n")


curveball_noswings = 0 
curveball_swung = []
for sb in curveball:
    #print (((sb.get('summary_acts')).get('pitch')).get('action'))
    if ((sb.get('summary_acts')).get('pitch')).get('action') == 'Called':
        curveball_noswings += 1 
    else:
        curveball_swung.append(sb)

curveball_hits = 0
curveball_ss_hit = 0
curveball_hit_positions = []
curveball_ss_positions = []
for swing in curveball_swung:
    if swing.get('events'):
        curveball_hits += 1\

        ballPos = None
        for item in (swing.get('samples_bat')):
            if item.get('event') == 'Hit':
                hitTime = item.get('time')
                ballPos = find_closest(swing.get('samples_ball'), hitTime)   
                    
        launch_angle = ((swing.get('events'))[0].get('start')).get('angle')[1]
        if (8 <= launch_angle <= 32):
            curveball_ss_hit += 1
            if ballPos:
                curveball_ss_positions.append(ballPos)
        else:
            if ballPos:
                curveball_hit_positions.append(ballPos)
            
plot_hits('Curveball Hits', curveball_hit_positions,curveball_ss_positions)                 

print("Curveball\n")

print("hits   ", curveball_hits)
print("'sweet spot' hits ", curveball_ss_hit)
#print(fb_ss_positions)

if len(curveball) > 0: 
        
    print ("Percentage Swung: ",  1 - (curveball_noswings/(len(curveball))))
    print ("Percentage hit out of swung: ", curveball_hits/(len(curveball)-curveball_noswings))
    print ("Percentage 'sweet spot' hits of hits: ",  curveball_ss_hit/curveball_hits)
    print ("Percentage hit overall: ", curveball_hits/(len(curveball)))

print("\n")

#plot hits 

plt.show()

