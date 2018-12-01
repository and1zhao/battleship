from matplotlib.pyplot import *
from numpy import *

#################### Data ######################
# data for each value shoud be seprated by commas, each tombstone's data should be in its own line - look at seriation_data.txt for an example
filename = 'seriation_data.txt'
file = open(filename, mode='r')
data = file.read()
file.close()
data = data.split('\n')
data = [graveyard.split(',') for graveyard in data]

start_year = 1840
year_increment = 20
num_intervals = 0
while start_year + year_increment * num_intervals < 2018:
    num_intervals += 1

labels1 = ['small', 'medium', 'large', 'xlarge']
labels2 = ['standard', 'tower', 'flat', 'rectangular', 'cross']
labels3 = ['limestone', 'granite', 'marble', 'metal']

freqs1, freqs2, freqs3 = [], [], []

for _ in labels1:
    freqs1.append([0] * num_intervals)
for _ in labels2:
    freqs2.append([0] * num_intervals)
for _ in labels3:
    freqs3.append([0] * num_intervals)

for elem in data:
    timeperiod_index = (int(elem[1]) - start_year)//20
    var1_index = labels1.index(elem[4])
    var2_index = labels2.index(elem[5])
    var3_index = labels3.index(elem[6])
    freqs1[var1_index][timeperiod_index] += 1
    freqs2[var2_index][timeperiod_index] += 1
    freqs3[var3_index][timeperiod_index] += 1

# change the filename here - make sure it is .png
filename = 'var1.png'

################## Formatting ###################

percentage_markers = True
border_color = 'black'
fill_color = 'black'
height = .875
show_y_ticks = False
preview_only = False

################################################

n_sets = len(freqs1)
set_length  = len(freqs1[0])

years = arange(start_year, start_year+year_increment*set_length, year_increment)
year_labels = ["{}-{}".format(y, y+year_increment) for y in years]

#check for errors in the data
bad_sets = ""
for i in range(n_sets):
    if set_length != len(freqs1[i]):
        bad_sets += "data set #{}: {}\n".format(i+1, labels1[i])

assert not bad_sets, "\nwrong number of elements for the following data sets:\n{}".format(bad_sets)

def tot(n, i):
    sum = 0
    for j in n:
        sum += j[i]
    return sum

total = [tot(freqs1, i) for i in range(set_length)]
percentages = [[ns[i]*1.0/total[i] for i in range(set_length)] for ns in freqs1]

f, axs = subplots(1, n_sets, sharex=True, sharey=True)

for i in range(n_sets):
    ax = axs[i]

    axs[i].set_title(labels1[i])
    rects = ax.barh(arange(set_length), percentages[i],
                        height, [-x/2.0 for x in percentages[i]],
                        tick_label=year_labels, align='center', color=fill_color, edgecolor=border_color)
    if percentage_markers:
        for j in range(len(rects)):
            rect = rects[j]
            
            percent_string = "{:.0f}%".format(100.0*percentages[i][j])
            
            t = ax.text(0, 0, percent_string,
                        verticalalignment='center', weight='bold',
                        clip_on=True)
            
            bb = t.get_window_extent(renderer=f.canvas.get_renderer())
            bb_coords = bb.transformed(axs[i].transData.inverted())
        
            if (rect.get_width() > bb_coords.width+0.025):
                x = rect.get_x() + rect.get_width()/2.0
                clr = 'white'
                align = 'center'
            else:
                x = rect.get_x()+rect.get_width()+0.025
                clr = 'black'
                align = 'left'
            y = rect.get_y() + rect.get_height()/2.0
            
            t.set_color(clr)
            t._x = x
            t._y = y
            t._horizontalalignment = align

axs[0].tick_params(
    axis='y',
    which='both',
    right='off')

f.subplots_adjust(wspace=0)
setp([a.get_xticklabels() for a in f.axes], visible=False)

for ax in axs:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(
        axis='x',
        which='both',
        top='off',
        bottom='off')
    ax.spines['left'].set_visible(False)

for ax in axs[1 if show_y_ticks else 0:]:
    ax.tick_params(
        axis='y',
        which='both',
        left='off',
        right='off',
        labelbottom='off')

if preview_only:
    show()
else:
    savefig(filename)