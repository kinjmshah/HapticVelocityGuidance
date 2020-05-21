import numpy as np
import time
import csv
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO


def motorLEDActivation(topL,botL,topM,botM,velDiff,thresh,state,processTime,\
        prevVelDiff,prevFreq,pwm,changeFreq):
    ''' this function walks through motor and LED advication algorithm for upward and downward motion'''
    pwmON = 100
    pwmOFF = 0

    freq150 = 150
    freq250 = 250

    pwmDiffThreshPos = 0
    pwmDiffThreshNeg = 0

    # WEBERS LAW
    pwmDiff = velDiff - prevVelDiff
    # if velDiff > prevVelDiff - will be positive value
    k_weber = 0.3 # webers law fraction for vibrotactile stimulation

    # if the motors were off and now they should be on set the frequency to 150
    # if the difference in velocity for current time > previous time velocity diff
        ## increase frequency to (1.03)*prevFreq
    # if the difference in velocity is < previous time difference then
        ## decrease frequency to (0.7)*prevFrequency

    pwmLED = 100-(1/(1+abs(velDiff)))*100
    # LED PWM will be proportional to velDiff still

    #print('PWM: ', pwm)

    # UPWARD MOTION
    if state == 2:
        # arm is moving upward

        if velDiff > thresh:

            # moving up too quickly, top should activate

            botL.ChangeDutyCycle(pwmOFF)
            botM.ChangeDutyCycle(pwmOFF)

            # top should turn on
            topL.ChangeDutyCycle(pwmLED)

            if pwm == 0: # if the motor was off
                freq = freq250
                #print('frequency', freq) # value should be 150
                pwm = pwmON # turn the motor on

                topM.ChangeFrequency(freq150)
                topM.ChangeDutyCycle(pwm)

            elif ((pwmDiff > pwmDiffThreshPos) and changeFreq == True): # the velDiff is increasing (moving away from target)
                freq = (1+k_weber)*prevFreq
                if freq > 500:
                    freq = 500

                topM.ChangeFrequency(freq150)
                #topM.ChangeDutyCycle(pwmON) #shouldnt need this code - if the motor is on it should stay on just frequency change

            elif ((pwmDiff < pwmDiffThreshNeg) and changeFreq == True): # the velDiff is decreasing (moving closer to target)
                freq = (1-k_weber)*prevFreq
                if freq < 150:
                    freq = 150

                topM.ChangeFrequency(freq150)

                #topM.ChangeDutyCycle(pwmON)
            else:
                freq = prevFreq
                # motor does not change
                #print('FREQ DOES NOT CHANGE')

            freqBOT = pwmOFF
            freqTOP = freq

            print('STATE 2: ARM UP TOO FAST - TOP SHOULD BE ON: ',freqTOP)
            print('bot',freqBOT)

            #print('TOP UP')
            actuateTime = time.time()-processTime
            #prevPWM = pwmON # set the status for the next iteration

        elif velDiff < -thresh:
            # moving upward too slowly, bottom should activate
            topL.ChangeDutyCycle(pwmOFF)
            topM.ChangeDutyCycle(pwmOFF)

            # bottom should turn on
            botL.ChangeDutyCycle(pwmLED)

            if pwm == 0:
                freq = freq250
                pwm = pwmON
                botM.ChangeFrequency(freq150)
                botM.ChangeDutyCycle(pwm)

            elif ((pwmDiff > pwmDiffThreshPos) and changeFreq == True): # the velDiff is increasing (moving away from target)
                freq = (1+k_weber)*prevFreq
                if freq > 500:
                    freq = 500
                botM.ChangeFrequency(freq150)
                #botM.ChangeDutyCycle(pwmON)
            elif ((pwmDiff < pwmDiffThreshNeg) and changeFreq == True): # the velDiff is decreasing (moving closer to target)
                freq = (1-k_weber)*prevFreq
                if freq < 150:
                    freq = 150
                botM.ChangeFrequency(freq150)
                #topM.ChangeDutyCycle(pwmON)
            else:
                freq = prevFreq
                #print('FREQ DOES NOT CHANGE')

            #print('BOT UP')
            freqBOT = freq
            freqTOP = pwmOFF
            print('STATE 2: ARM UP TOO SLOW - BOT SHOULD BE ON: ', freqBOT)
            print('top',freqTOP)

            actuateTime = time.time()-processTime

        else: # moving within the range

            pwmLED = pwmOFF
            pwm = pwmOFF
            topL.ChangeDutyCycle(pwmLED)
            botL.ChangeDutyCycle(pwmLED)
            botM.ChangeDutyCycle(pwm)
            topM.ChangeDutyCycle(pwm)
            actuateTime = time.time()-processTime

            freq = pwmOFF
            freqBOT = pwmOFF
            freqTOP = pwmOFF

            print('JUST RIGHT - NONE ON: ')
            print('top',freqTOP)
            print('bot',freqBOT)

    # DOWNWARD MOTION
    elif state == 3:
        # arm is moving downward

        if velDiff > thresh:
            # user is moving down too quickly bottom should activate
            topL.ChangeDutyCycle(pwmOFF)
            topM.ChangeDutyCycle(pwmOFF)

            # bottom should turn on
            botL.ChangeDutyCycle(pwmLED)

            if pwm == 0:
                freq = freq250
                pwm = pwmON
                botM.ChangeFrequency(freq150)
                botM.ChangeDutyCycle(pwmON)

            elif pwmDiff > 0: # the velDiff is increasing (moving away from target)
                freq = (1+k_weber)*prevFreq
                if freq > 500:
                    freq = 500
                botM.ChangeFrequency(freq150)
                #botM.ChangeDutyCycle(pwmON)
            elif pwmDiff < 0: # the velDiff is decreasing (moving closer to target)
                freq = (1-k_weber)*prevFreq
                if freq < 150:
                    freq = 150
                botM.ChangeFrequency(freq150)
                #topM.ChangeDutyCycle(pwmON)
            else:
                freq = prevFreq
                #print('FREQ DOES NOT CHANGE')

            #print('BOT DOWN')
            freqTOP = pwmOFF
            freqBOT = freq
            print('STATE 3: ARM DOWN TOO FAST - BOT SHOULD BE ON: ',freqBOT)
            print('top',freqTOP)


            actuateTime = time.time()-processTime

        elif velDiff < -thresh:
            # moving down too slowly, top should activate
            botL.ChangeDutyCycle(pwmOFF)
            botM.ChangeDutyCycle(pwmOFF)

            # top should turn on
            topL.ChangeDutyCycle(pwmLED)

            if pwm == 0: # if the motor was off
                freq = freq250
                pwm = pwmON

                topM.ChangeFrequency(freq150)
                topM.ChangeDutyCycle(pwm)

            elif pwmDiff > 0: # the velDiff is increasing (moving away from target)
                freq = (1+k_weber)*prevFreq
                if freq > 500:
                    freq = 500
                topM.ChangeFrequency(freq150)
                #topM.ChangeDutyCycle(pwmON) #shouldnt need this code - if the motor is on it should stay on just frequency change

            elif pwmDiff < 0: # the velDiff is decreasing (moving closer to target)
                freq = (1-k_weber)*prevFreq
                if freq < 150:
                    freq = 150
                topM.ChangeFrequency(freq150)

                #topM.ChangeDutyCycle(pwmON)
            else:
                freq = prevFreq
                # motor does not change
                #print('FREQ DOES NOT CHANGE')

            #print('TOP DOWN')

            freqTOP = freq
            freqBOT = pwmOFF
            print('STATE 3: ARM DOWN TOO SLOW - TOP SHOULD BE ON: ',freqTOP)
            print('bot',freqBOT)
            actuateTime = time.time()-processTime


        else:

            pwmLED = pwmOFF
            pwm = pwmOFF
            topL.ChangeDutyCycle(pwmLED)
            botL.ChangeDutyCycle(pwmLED)
            botM.ChangeDutyCycle(pwm)
            topM.ChangeDutyCycle(pwm)
            actuateTime = time.time()-processTime

            freqBOT = pwmOFF
            freqTOP = pwmOFF
            freq = pwmOFF
            actuateTime = time.time()-processTime

            print('JUST RIGHT - NONE ON: ')
            print('top',freqTOP)
            print('bot',freqBOT)

    return actuateTime, freqBOT, freqTOP, freq, pwm


def callGuidanceSystem(topL,botL,topM,botM,initialState,filename,targetVel,velProf):

    start = time.time()
    t = time.time() - start
    # initialize state
    state = initialState

    # Variables
    targetVel = float(targetVel)
    velProf = int(velProf)

    threshold = 0.25 # target vel +/- threshold the motors will not be active
    angPosTol = 2. # for angle initialization (e.g. if the angle is -2 to 2 the state will change)
    processTimeStart = 0
    actuateTime = 0
    timeLoopEnd = 0
    timeLoop = 0
    freqBOT = 0
    freqTOP = 0

    elrStore = [] # angle position store
    velStore = [] # angular velocity store
    iteration = 0
    diffPrev = 0
    pwmPrev = 0
    prevFreq = 0
    count5 = 0
    changeFreq = False

    # initialize CSV
    csv.register_dialect('myDialect',delimiter = ',', \
            quoting = csv.QUOTE_NONE,skipinitialspace=True,escapechar='\\')

    # Intialize IMU
    print('Trying to initilize IMU')
    bno = BNO055.BNO055(serial_port='/dev/serial0',rst=18)

    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055')

    print('Please have the user move to zero position.\n')

    try:
        while True:
            count5 +=1
            if count5 == 5:
                changeFreq = True
                count5 = 0

            t = time.time() - start

            if velProf == 1:
                targetVel = np.sin(5*t)

            timeLoopPrev = timeLoopEnd - timeLoop

            timeLoop = time.time()

            pauseCheck = 0

            # begin collecting values
            heading,roll,pitch = bno.read_euler() # euler angles
            roll = -roll
            gx,gy,gz = bno.read_gyroscope() # angular velocity
            readTime = time.time()-start

            # Store values
            elrStore.append(roll)
            velStore.append(gy)

            # skip to next iteration of loop if not long enough
            if len(elrStore)<3:
                continue

            # calculate moving average
            avgPos = np.mean(elrStore)
            avgVel = np.mean(velStore)

            # trim first entry
            elrStore = elrStore[1:]
            velStore = velStore[1:]

            # calculate difference between measured and target velocity
            diff = abs(avgVel) - abs(targetVel)

            if state == 0:

                # if the user gets to the 0 angle position change the state
                if abs(avgPos) < angPosTol:
                    state = 1 # have the user move to the negative most value before they begin the true experiment

                    input('You have reached 0,Press Enter To Continue.\n')
                    pauseCheck = 1
                    print('Please have the user move to minimum position degrees\n')

            elif state == 1:
                # once the user gets to minimum degree position change the state
                if abs(90 + avgPos) < 10:
                    minAngle = avgPos
                    state = 1.5 # state 2 = upward motion
                    input('STATE 1.5 START: Please press enter to continue.\n')
                    pauseCheck = 1
                    print('-----------------------Begin upward motion to max\n')

            elif state == 1.5:
                if abs(90-avgPos) < 10:
                    maxAngle = avgPos
                    state = 3 #state 3 = upward motion
                    # input('STATE 3 START: press enter to continue.\n')
                    pauseCheck = 1
                    print('-------------------------Begin downward motion to min\n')

            elif state == 2:
                processTimeStart = time.time() - readTime
                # if moving upward activate motors/led as needed
                actuateTime,freqBOT,freqTOP,freq,pwm = motorLEDActivation(topL,botL,\
                        topM,botM,diff,threshold,state,processTimeStart,diffPrev,\
                        prevFreq,pwmPrev,changeFreq)

                prevFreq = freq
                pwmPrev = pwm

                if abs(avgPos-maxAngle) < angPosTol: # 45 - 45
                    state = 3 # downward motion
                    freq = 150
                    freqBOT = freq
                    freqTOP = freq
                    topL.ChangeDutyCycle(80)
                    botL.ChangeDutyCycle(80)
                    topM.ChangeFrequency(freq)
                    botM.ChangeFrequency(freq)
                    topM.ChangeDutyCycle(100)
                    botM.ChangeDutyCycle(100)
                    # input('STATE3 START: Press Enter to Continue. \n')
                    #pauseCheck = 1
                    #prevFreq = 0
                    print('---------------Please have the user now move down to min.\n')

            elif state == 3:
                processTimeStart = time.time() - readTime
                # if moving doward activate motots/LED as needed
                actuateTime,freqBOT,freqTOP,freq,pwm = motorLEDActivation(topL,botL,\
                        topM,botM,diff,threshold,state,processTimeStart,diffPrev,\
                        prevFreq,pwmPrev,changeFreq)

                prevFreq = freq
                pwmPrev = pwm

                if abs(minAngle - avgPos) < angPosTol:
                    state = 2 # upward motion
                    freq = 150
                    freqBOT = freq
                    freqTOP = freq
                    topL.ChangeDutyCycle(80)
                    botL.ChangeDutyCycle(80)
                    topM.ChangeFrequency(freq)
                    botM.ChangeFrequency(freq)
                    topM.ChangeDutyCycle(100)
                    botM.ChangeDutyCycle(100)
                    # input('Press Enter to Continue. \n')
                    #pauseCheck = 1
                    #prevFreq = 0
                    print('------------------------Please have the user now move ip to max. \n')

            data = np.array([t, avgVel, targetVel,diff,freqBOT,freqTOP,state,actuateTime - readTime,timeLoopPrev,pauseCheck]).ravel()

            with open(filename,'a') as f:
                writer = csv.writer(f,dialect = 'myDialect')
                writer.writerow(data)
                f.close

            timeLoopEnd = time.time()

            #print(targetVel,avgPos,state)

            iteration += 1
            changeFreq = False

    except KeyboardInterrupt:

        topM.stop()
        botM.stop()
        topL.stop()
        botL.stop()
        GPIO.cleanup()
        print('Complete.')
