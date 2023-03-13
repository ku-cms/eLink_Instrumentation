# bitmap_creator_processes.py

from PIL import Image
import numpy as np
import os
import random as rand
import time
import concurrent.futures

# WARNING (based on testing the current script):
# This script took a long time to run (approx. 1 hour).
# Eventually (after approx 1 hour), the script crashed with this error:

# RuntimeError:
#         An attempt has been made to start a new process before the
#         current process has finished its bootstrapping phase.
#
#         This probably means that you are not using fork to start your
#         child processes and you have forgotten to use the proper idiom
#         in the main module:
#
#             if __name__ == '__main__':
#                 freeze_support()
#                 ...
#
#         The "freeze_support()" line can be omitted if the program
#         is not going to be frozen to produce an executable.

# The full script should not be run... it takes too long.

pixel_size = 2 # in micro meter

gnd_layer_height0 = int(4 / pixel_size) # in micro meter
layer_height0 = int(13 / pixel_size) # in micro meter
trace_width0 = int(75 / pixel_size) # in micro meter
gap0 = int(63 / pixel_size) # in micro meter
spacer_height0 = int(45 / pixel_size) # in micro meter

gnd_box_thickness = int(2 / pixel_size)
vacuum_box = 2
image_width0 = int(1600 / pixel_size) - 2*vacuum_box
image_height0 = int(800 / pixel_size) - 2*vacuum_box

pos_alu = (224,  31,  31)
neg_alu = ( 31,  31, 224)
neu_alu = ( 31, 224,  31)
epoxy   = (188, 127,  96)

def parametercreation(samplesize, gnd_layer_height, layer_height, pixel_size, directory):
    parameterlist = []
    filelist = []

    for i in range(samplesize):
        rand_trace_width = rand.randrange(63,150,7)//pixel_size
        rand_gap = rand.randrange(63,150,7)//pixel_size
        rand_spacer_height = rand.randrange(5,70,5)//pixel_size
        parameterlist.append((rand_trace_width, rand_gap, rand_spacer_height))

        filename = 'Usermap Microstrip'
        newfilename = filename + str(gnd_layer_height) + '-' + str(layer_height) + '-' + str(rand_trace_width) + '-' + str(rand_gap) + '-' + str(rand_spacer_height) + ' (.00' + str(pixel_size) + 'mm).bmp'
        filelist.append(newfilename)
    runlist_path = directory + '/runlist.txt'
    with open(runlist_path, 'w') as f:
        for item in filelist:
            f.write("%s\n" % item)

    return (parameterlist, filelist) # return tuple and in parameterlist there are lists with structure (rand_trace_width, rand_gap, rand_spacer_height)

def draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory):
    image_width = image_width0 + 2*vacuum_box
    image_height = image_height0 + 2*vacuum_box
    h_border_size = int((image_width - 2*trace_width - gap)/2)

    img = Image.new( 'RGB', (image_width, image_height), "black") # Create a new black image
    pixels = img.load() # Create the pixel map
    for i in range(img.size[0]):    # For every pixel:
        for j in range(img.size[1]):
            if (j in range(image_height - vacuum_box - gnd_layer_height - spacer_height - layer_height, image_height - vacuum_box - gnd_layer_height - spacer_height)):
                # left conductor:
                if i in range(h_border_size, h_border_size + trace_width):
                    pixels[i,j] = neg_metal
                # right conductor:
                elif i in range(h_border_size + trace_width + gap, h_border_size + 2 * trace_width + gap):
                    pixels[i,j] = pos_metal
            # dielectric spacer
            elif (j in range(image_height - vacuum_box - gnd_layer_height - spacer_height, image_height - vacuum_box - gnd_layer_height)) & (i in range(vacuum_box, image_width - vacuum_box)):
                pixels[i,j] = dielectric
            # ground plane
            elif (j in range(image_height - vacuum_box - gnd_layer_height, image_height - vacuum_box)) & (i in range(vacuum_box, image_width - vacuum_box)):
                pixels[i,j] = neu_metal
            else: pixels[i,j] = (0, 0, 0)

            # ground box
            # horizontal
            if ((j in range(vacuum_box, gnd_box_thickness + vacuum_box)) | (j in range(image_height - gnd_box_thickness - vacuum_box, image_height - vacuum_box))) & (i in range(vacuum_box, image_width - vacuum_box)):
                pixels[i,j] = neu_metal
            # vertical
            if (j in range(vacuum_box, image_height - vacuum_box)) & ((i in range(vacuum_box, gnd_box_thickness + vacuum_box)) | (i in range(image_width - gnd_box_thickness - vacuum_box, image_width - vacuum_box))):
                pixels[i,j] = neu_metal
    # save the bitmap
    filename = directory + '/Usermap Microstrip'
    newfilename = filename + str(gnd_layer_height) + '-' + str(layer_height) + '-' + str(trace_width) + '-' + str(gap) + '-' + str(spacer_height) + ' (.00' + str(pixel_size) + 'mm).bmp'
    img.save(newfilename)
    print(newfilename)

##### MAIN #####
rel_path = 'Sampledir'

if not os.path.exists(rel_path):
    os.makedirs(rel_path)

num_samples = 100
x, y = parametercreation(num_samples, gnd_layer_height0, layer_height0, pixel_size, rel_path)

for i in range(num_samples):
    print("i = {0}, ({1}, {2}, {3})".format(i, x[i][0], x[i][1], x[i][2]))
    # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
    draw_microstrip(gnd_layer_height0, layer_height0, x[i][0], x[i][1], x[i][2], pos_alu, neg_alu, neu_alu, epoxy, rel_path)

# create the bitmaps with a parameter loop
for g in range(63,150,7):
    # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
    draw_microstrip(gnd_layer_height0, layer_height0, trace_width0, int(g / pixel_size), spacer_height0, pos_alu, neg_alu, neu_alu, epoxy, rel_path)

# iterations: gap, spacer_height, trace_width
for iter_trace_width in range(63,150,7):
    for iter_gap in range(63,150,7):
        for iter_spacer_height in range(5,70,5):
            # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
            single_image = draw_microstrip(gnd_layer_height0, layer_height0, int(iter_trace_width / pixel_size), int(iter_gap / pixel_size), int(iter_spacer_height / pixel_size), pos_alu, neg_alu, neu_alu, epoxy, rel_path)

#img.show()

missing_list = [[31, 59], [35, 70], [38, 63], [42, 73], [45, 35], [52, 45], [52, 59], [59, 38], [66, 38], [70, 45], [73, 31], [73, 38], [73, 45]]
rel_path = 'Missingdir'

if not os.path.exists(rel_path):
    os.makedirs(rel_path)

for missing in missing_list:
    # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
    draw_microstrip(gnd_layer_height0, layer_height0, missing[0], missing[1], 22, pos_alu, neg_alu, neu_alu, epoxy, rel_path)

start = time.perf_counter()
rel_path = 'Testingdir'

trace_width_list = range(63,150,7)
gap_list = range(63,150,7)
spacer_height_list = range(5,70,5)

if not os.path.exists(rel_path):
    os.makedirs(rel_path)

#for trace_width in trace_width_list:
#    for gap in gap_list:
#        # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
#        draw_microstrip(gnd_layer_height0, layer_height0, trace_width//pixel_size, gap//pixel_size, 22, pos_alu, neg_alu, neu_alu, epoxy, rel_path)

def threaded_drawer(trace_width):
    for gap in gap_list:
        # draw_microstrip(gnd_layer_height, layer_height, trace_width, gap, spacer_height, pos_metal, neg_metal, neu_metal, dielectric, directory)
        draw_microstrip(gnd_layer_height0, layer_height0, trace_width//pixel_size, gap//pixel_size, 22, pos_alu, neg_alu, neu_alu, epoxy, rel_path)

## this works in linux without jupyther just fine
with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(threaded_drawer, trace_width_list)


finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} second(s)')
