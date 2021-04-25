from threading import Thread
import RPi.GPIO as GPIO
from spidev import SpiDev
import threading

import time



buzzer = 13;
class MCP3008:
    def __init__(self, bus=0, device=0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000  # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000  # 1MHz

    def read(self, channel=0):
        cmd1 = 4 | 2 | ((channel & 4) >> 2)
        cmd2 = (channel & 3) << 6

        adc = self.spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data

    def close(self):
        self.spi.close()

class Pulsesensor:
    def __init__(self, channel=0, bus=0, device=0):
        self.channel = channel
        self.BPM = 0
        self.adc = MCP3008(bus, device)

    def getBPMLoop(self):
        # init variables
        rate = [0] * 10  # array to hold last 10 IBI values
        sampleCounter = 0  # used to determine pulse timing
        lastBeatTime = 0  # used to find IBI
        P = 512  # used to find peak in pulse wave, seeded
        T = 512  # used to find trough in pulse wave, seeded
        thresh = 525  # used to find instant moment of heart beat, seeded
        amp = 100  # used to hold amplitude of pulse waveform, seeded
        firstBeat = True  # used to seed rate array so we startup with reasonable BPM
        secondBeat = False  # used to seed rate array so we startup with reasonable BPM

        IBI = 600  # int that holds the time interval between beats! Must be seeded!
        Pulse = False  # "True" when User's live heartbeat is detected. "False" when not a "live beat".
        lastTime = int(time.time() * 1000)

        while not self.thread.stopped:
            Signal = self.adc.read(self.channel)
            currentTime = int(time.time() * 1000)

            sampleCounter += currentTime - lastTime
            lastTime = currentTime

            N = sampleCounter - lastBeatTime

            # find the peak and trough of the pulse wave
            if Signal < thresh and N > (IBI / 5.0) * 3:  # avoid dichrotic noise by waiting 3/5 of last IBI
                if Signal < T:  # T is the trough
                    T = Signal  # keep track of lowest point in pulse wave

            if Signal > thresh and Signal > P:
                P = Signal

            # signal surges up in value every time there is a pulse
            if N > 250:  # avoid high frequency noise
                if Signal > thresh and Pulse == False and N > (IBI / 5.0) * 3:
                    Pulse = True  # set the Pulse flag when we think there is a pulse
                    IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
                    lastBeatTime = sampleCounter  # keep track of time for next pulse

                    if secondBeat:  # if this is the second beat, if secondBeat == TRUE
                        secondBeat = False;  # clear secondBeat flag
                        for i in range(len(rate)):  # seed the running total to get a realisitic BPM at startup
                            rate[i] = IBI

                    if firstBeat:  # if it's the first time we found a beat, if firstBeat == TRUE
                        firstBeat = False;  # clear firstBeat flag
                        secondBeat = True;  # set the second beat flag
                        continue

                    # keep a running total of the last 10 IBI values
                    rate[:-1] = rate[1:]  # shift data in the rate array
                    rate[-1] = IBI  # add the latest IBI to the rate array
                    runningTotal = sum(rate)  # add upp oldest IBI values

                    runningTotal /= len(rate)  # average the IBI values
                    self.BPM = 60000 / runningTotal  # how many beats can fit into a minute? that's BPM!

            if Signal < thresh and Pulse == True:  # when the values are going down, the beat is over
                Pulse = False  # reset the Pulse flag so we can do it again
                amp = P - T  # get amplitude of the pulse wave
                thresh = amp / 2 + T  # set thresh at 50% of the amplitude
                P = thresh  # reset these for next time
                T = thresh

            if N > 2500:  # if 2.5 seconds go by without a beat
                thresh = 512  # set thresh default
                P = 512  # set P default
                T = 512  # set T default
                lastBeatTime = sampleCounter  # bring the lastBeatTime up to date
                firstBeat = True  # set these to avoid noise
                secondBeat = False  # when we get the heartbeat back
                self.BPM = 0

            time.sleep(0.005)

    # Start getBPMLoop routine which saves the BPM in its variable
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.stopped = False
        self.thread.start()
        return

    # Stop the routine
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return


class PulseSensorTest(Thread):

    def __init__(self, client, value):
        super().__init__()
        self.p = Pulsesensor()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
        self.value = ""
        self.data = "basic"

        self.client = client

    def clarkon(self):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(buzzer, GPIO.LOW)

    def clarkoff(self):
        GPIO.output(buzzer, GPIO.LOW)

    def run(self):
        self.p.startAsyncBPM()
        try:
            while True:
                self.bpm = self.p.BPM
                if self.bpm > 0:
                    self.value = 'pulse_on'
                    print("BPM: %d" % self.bpm)
                    if self.bpm<80:
                        self.clarkon()
                    else:
                        self.clarkoff()

                else:
                    self.value = 'pulse_error'
                    print("No Heartbeat found")
                time.sleep(1)
                self.client.publish("iot/pulse", "pulse,%d" % self.value)
                if self.data == "stop":
                    print("stop")
                    break
        except:
            self.p.stopAsyncBPM()
