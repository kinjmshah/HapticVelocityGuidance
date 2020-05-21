import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times New Roman"

def getFileNames(dataFolderName):
    cwd = os.getcwd()
    dirData = cwd + '/' + dataFolderName
    fileNames = os.listdir(dirData)

    return fileNames,dirData

def readData(fileNamesAll,dirData,identifier):
    for name in fileNamesAll:
        if identifier in name:
            fileName = name

    filePath = dirData + '/' + fileName
    dataStr = open(filePath,'r')
    dataRaw = np.loadtxt(filePath,delimiter = ',')
    stopYes = dataRaw[:,9]
    time = dataRaw[:,0]

    numPoints = len(time)

    sub0 = time[0]
    for i in range(numPoints):
        time[i] = time[i] - sub0

    count1 = 0
    for i in range(1,numPoints):
        if stopYes[i] == 1:
            count1 += 1
            print(count1)
            if count1 == 2:
               trimVal = i+1
            subtractTime = time[i+1] - time[i]
            for j in range(i+1,numPoints):
                time[j] = time[j] - subtractTime

    targetVel = dataRaw[trimVal:,2]
    freqBOT = dataRaw[trimVal:,4]
    avgVel = dataRaw[trimVal:,1]
    freqTOP = dataRaw[trimVal:,5]

    tNew= time[trimVal:]
    tN1 = tNew[0]
    tFinal = tNew - tN1

    for i in range(len(targetVel)):
        avgVel[i] = avgVel[i]*180./np.pi
        targetVel[i] = targetVel[i]*180./np.pi


    return tFinal, avgVel, targetVel,freqBOT,freqTOP

dataFolderName = 'data'

fileNames,dirData = getFileNames(dataFolderName)


# CONSTANT TARGET VELOCITY

t1, avgV1, targetV1,freqB1,freqT1 = readData(fileNames,dirData,'001')

thresh1 = targetV1 * 0.25;

fig1, axs1 = plt.subplots(2, sharex=True, sharey=False)
# plot "true" velocity
axs1[0].plot(t1, avgV1,'-',color = 'purple',linewidth=2)
# plot target
axs1[0].plot(t1,targetV1,'k--',linewidth=0.75)
# plot target - threshold
axs1[0].fill_between(t1, targetV1 + thresh1, targetV1 - thresh1,  color = 'palegoldenrod')
axs1[0].plot(t1,-targetV1,'k--',linewidth=0.75)
axs1[0].fill_between(t1, -targetV1 + thresh1, -targetV1 - thresh1,  color = 'palegoldenrod')

axs1[0].plot(t1,[0]*t1,'k',linewidth = 0.5)
# plot pwm
axs1[1].plot(t1,freqB1, 'r-',linewidth=1)
axs1[1].plot(t1,freqT1,'b--',linewidth=1)
axs1[1].set_ylim([0,510])
axs1[1].set_xlim([0,t1[-1]])
axs1[0].set_xlim([0,t1[-1]])

plt.tight_layout()

count = 0
for ax in axs1:
    count += 1
    if count == 1:
        ax.set(ylabel = 'Velocity (degrees/sec)')
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(right="off", top="off",bottom="off",left = "off")
    elif count == 2:
        ax.set(xlabel = 'Time (sec)',ylabel = 'Vibration Freq (Hz)')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(right="off", top="off",bottom="off",left="off")

# Hide x labels and tick labels for all but bottom plot.
for ax in axs1:
    ax.label_outer()

plt.tight_layout()
fig1.savefig('ConstantVel.png')


# VARYING TARGET VELOCITY

t2, avgV2, targetV2,freqB2,freqT2 = readData(fileNames,dirData,'002')

thresh2 = targetV2 * 0.25;

fig2, axs2 = plt.subplots(2, sharex=True, sharey=False)
# plot "true" velocity
axs2[0].plot(t2, avgV2,'-',color = 'purple',linewidth=2)
# plot target + threshold
# plot target
axs2[0].plot(t2,targetV2,'k--',linewidth=0.75)
# plot target - threshold
#axs1[0].plot(t1,targetV1 - thresh1, 'gray',linewidth=1)
axs2[0].fill_between(t2, targetV2 + thresh2, targetV2 - thresh2,  color = 'palegoldenrod')
#axs1[0].plot(t1,-targetV1 + thresh1,'gray',linewidth=1)
axs2[0].plot(t2,-targetV2,'k--',linewidth=0.5)
axs2[0].plot(t2,[0]*t2,'k',linewidth = 0.5)
#axs1[0].plot(t1,-targetV1 - thresh1,'gray',linewidth=1)
axs2[0].fill_between(t2, -targetV2 + thresh2, -targetV2 - thresh2,  color = 'palegoldenrod')

# plot pwm
axs2[1].plot(t2,freqB2, 'r',linewidth=1)
axs2[1].plot(t2,freqT2,'b--',linewidth=1)
axs2[1].set_ylim([0,510])
axs2[1].set_xlim([0,t2[-1]])
axs2[0].set_xlim([0,t2[-1]])

plt.tight_layout()

count = 0
for ax in axs2:
    count += 1
    if count == 1:
        ax.set(ylabel = 'Velocity (degrees/sec)')
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(right="off", top="off",bottom="off",left="off")
    elif count == 2:
        ax.set(xlabel = 'Time (sec)',ylabel = 'Vibration Freq (Hz)')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.tick_params(right="off", top="off",bottom="off",left="off")

# Hide x labels and tick labels for all but bottom plot.
for ax in axs1:
    ax.label_outer()

plt.tight_layout()
fig2.savefig('VaryingVel.png')
