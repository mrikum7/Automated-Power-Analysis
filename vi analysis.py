#!/usr/bin/python3

import usbtmc as u
import pandas as pd
from time import sleep, time
from scipy import integrate

file = open('power-pH.csv', 'a')

N = input('HNO3:')
P = input('H3PO4:')
K = input('KOH:')

dev1 = u.Instrument(u.list_devices()[0])
dev2 = u.Instrument(u.list_devices()[1])
volt = []
curr = []
dev1.write(':outp ch1, on')
for i in range(351):
	dev1.write(':volt {}'.format(0.01*i))
	#sleep(0.1)
	volt.append(0.01*i)
	#c = dev2.ask(':meas:curr:dc? 4?').lstrip('#9000000016  ')
	c = dev2.ask(':meas:curr:dc?')[11:]
	print(c)
	curr.append(float(c))
	#sleep(0.1)
	
df = pd.DataFrame({'volt':volt, 'curr':curr})
df.to_csv('{}-{}-{}.csv'.format(N,P,K), index=None)
power = integrate.simps(curr, volt)

file.write(str(power) + ',' + N + ',' + P + ',' + K + '\n')
file.close()
print(power)
dev1.write(':outp ch1, off')
