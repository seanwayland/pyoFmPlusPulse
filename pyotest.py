from pyo import *
pm_list_devices()
import math
import sys
import random
random.seed(a=None, version=2)


attacksetting = 0.015

decaysetting = 0.3

sustainsetting = 0.9

releasesetting = 0.05

polyphony = 8

bendrange = 2

samplerate = 96000

buffsize = 512
s = Server(sr=samplerate, buffersize=buffsize)
s.setMidiInputDevice(2)

s.boot()

n = Notein(poly=polyphony, scale=1)  # transpo
bend = Bendin(brange=bendrange, scale=1)
env = MidiAdsr(n['velocity'], attack=attacksetting, decay=decaysetting, sustain=sustainsetting, release=releasesetting)
t = HarmTable([1, 0.1])
pit = n["pitch"]
vel = n["velocity"]






#f = FM(carrier=[400,400], ratio=[.2498, .2503], index = [4.8, 3.8],  mul=0.2 ).out()

freq = pit*bend
# LFO applied to the `sharp` attribute
# band limited saw wave
#osc = LFO(freq=freq, type = 1 , sharp=0.7, mul=env)
#f = FM(carrier=[pit,pit], ratio=[.2498, .2503], index = [4.8, 3.8],  mul=env)
f = FM(carrier=pit*bend, ratio=.5 , index = 4 + vel*3,  mul=env)
butlp = ButLP(f, 3000)
mm = Mixer(outs=3, chnls=2, time=.025)
fx2 = STRev(mm[0], inpos=0.25, revtime=0.1, cutoff=5000*vel - pit/10, mul=env, bal=0.06, roomSize=1).out(0)

lfo = Sine(.1).range(0.78, 0.82)
ph = Phasor(pit*bend)
sqr = ph < lfo
bisqr = Sig(sqr, mul=2, add=-1)
filt = IRWinSinc(bisqr, freq=0, order=16)
output = Sig(filt, mul=env)
fx2 = STRev(mm[1], inpos=0.25, revtime=2, cutoff=5000, mul=env/2, bal=0.01, roomSize=1).out(1)


mm.addInput(0, f)
mm.addInput(1, output)
mm.setAmp(0,0,.5)
mm.setAmp(0,1,.5)
mm.setAmp(1,1,.5)



s.gui(locals())