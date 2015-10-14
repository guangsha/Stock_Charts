#!/usr/bin/python
#
#  Dividend!
#

import os
import sys
import urllib2
import math
import numpy
from pylab import *

#                                                                                                                              
#  Dividend adjusted!                                                                                                           
#
 
Use_Dividend_Adjusted = True

if ( Use_Dividend_Adjusted ):
    readinIndex = 6
else:
    readinIndex = 4

# Subplots in total
nsubplots = 5
iprice = 1
imacd = 2
#icci = 4
idmi = 3
ibalance = 4
igain = 5


# CCI parameters!!!                                                                                                              
CCI_period = 20

# DMI parameters!!!
DMI_period = 14

name = str(sys.argv[1])
period = str(sys.argv[2])
time_range = int(sys.argv[3]) 
predict = bool(int(sys.argv[4]))

if (period == 'd'):
    periodText = "days"
if (period == 'w'):
    periodText = "weeks"
if (period == 'm'):
    periodText = "months"

def Average(list):
    r=0.0
    for i in list:
        r+=float(i)
    return  r/len(list)

def EMA(list):
    r = 0.0
    f = 0
    for i in range(1, len(list) + 1): 
        r = r + float(list[i-1]) * ( len(list) + 1 - i )
        f = f + i
    return  r / f

response = urllib2.urlopen('http://table.finance.yahoo.com/table.csv?s='+name+'&d=12&e=29&f=3014&g='+period+'&a=3&b=23&c=1000&ignore=.csv')

if not os.path.exists( 'figures' ):
    os.makedirs( 'figures' )

html = response.read()
#print html
a = html.split('\n')

dmax = len(a) - 2  #Be careful here! One header line and One empty line in the end
if ( dmax < time_range ):
    time_range = dmax - 1
a200 = []
date200 = []
avg12 = []
avg26 = []
dif = []
TP = []
TR = []
TR14 = []
HighP = []
LowP = []

DM_positive = []
DM_negative = []
DM14_positive = []
DM14_negative = []

DI14_positive = []
DI14_negative = []

DX = []
ADX = []

for i in range(dmax, 0, -1):
    date200.append(a[i].split(',')[0])
    a200.append(float(a[i].split(',')[readinIndex]))
#    HighP.append( float(a[i].split(',')[2]) )
    HighP.append( float(a[i].split(',')[2]) / float(a[i].split(',')[4]) * float(a[i].split(',')[6]) )
#    LowP.append( float(a[i].split(',')[3]) )
    LowP.append( float(a[i].split(',')[3]) / float(a[i].split(',')[4]) * float(a[i].split(',')[6]) )
    CloseP = float(a[i].split(',')[readinIndex]) 
    TP.append( (HighP[dmax - i] + LowP[dmax - i] + CloseP) / 3.0 )
    if ( i < dmax ):
        TR.append( max(HighP[dmax - i], a200[dmax - i - 1]) - min(LowP[dmax - i], a200[dmax - i - 1]) )
        TR14.append( TR14[dmax - i - 1] * float(DMI_period - 1) / float(DMI_period) + TR[dmax - i] / float(DMI_period) ) 
        DM_positive.append( max(0, HighP[dmax - i] - HighP[dmax - i - 1]) )
        DM_negative.append(  max(0, LowP[dmax - i - 1] - LowP[dmax - i]) )
        DM14_positive.append( DM14_positive[dmax - i - 1] * float(DMI_period - 1) / float(DMI_period) + DM_positive[dmax - i] / float(DMI_period) )
        DM14_negative.append( DM14_negative[dmax - i - 1] * float(DMI_period - 1) / float(DMI_period) + DM_negative[dmax - i] / float(DMI_period) )
        if ( TR14[dmax - i] == 0 ):
            DI14_positive.append(0)
            DI14_negative.append(0)
        else:
            DI14_positive.append( DM14_positive[dmax - i] / TR14[dmax - i] * 100 )
            DI14_negative.append( DM14_negative[dmax - i] / TR14[dmax - i] * 100 )
        if ( DI14_positive[dmax - i] + DI14_negative[dmax - i] == 0 ):
            DX.append(0)
        else:
            DX.append( abs( DI14_positive[dmax - i] - DI14_negative[dmax - i] ) / ( DI14_positive[dmax - i] + DI14_negative[dmax - i] ) * 100 )
        ADX.append(  ADX[dmax - i - 1] * float(DMI_period - 1) / float(DMI_period) + DX[dmax - i] / float(DMI_period) )
    else:
        TR.append( HighP[dmax - i] - LowP[dmax - i] )
        TR14.append( TR[dmax - i] )
        DM_positive.append(0)
        DM_negative.append(0)
        DM14_positive.append( DM_positive[dmax - i] )
        DM14_negative.append( DM_negative[dmax - i] )
        if ( TR14[dmax - i] == 0 ):
            DI14_positive.append(0)
            DI14_negative.append(0)
        else:
            DI14_positive.append( DM14_positive[dmax - i] / TR14[dmax - i] * 100 )
            DI14_negative.append( DM14_negative[dmax - i] / TR14[dmax - i] * 100 )
        if ( DI14_positive[dmax - i] + DI14_negative[dmax - i] == 0 ):
            DX.append(0)
        else:
            DX.append( abs( DI14_positive[dmax - i] - DI14_negative[dmax - i] ) / ( DI14_positive[dmax - i] + DI14_negative[dmax - i] ) * 100 )
        ADX.append( DX[dmax - i] )

#    print HighP, LowP, CloseP
#a200.reverse()
#date200.reverse()
#TP.reverse()

a300 = []
for i in range(0, len(a200) ):
    a200[i] = float(a200[i])
#print max(a200)
EMA12 = a200[0]
EMA26 = a200[0]
DIF = 0.0
DEA_old = 0.0
DEA_new = 0.0
DIF_array = []
DEA_array = []
#print html

MA_array = []
CCI_array = []

figure(1,(12,15)) 

    # CCI Part
for i in range(0, dmax):
    if ( i < CCI_period - 1 ):
        MA = Average( TP[:i+1] )
        MA_array.append(MA)
#        MD = Average( [abs(x - y) for x, y in zip(MA_array[:i+1], TP[:i+1])] )
        MD = Average( [abs(x - MA) for x in TP[:i+1]] )
    else:
        MA = Average( TP[i-19:i+1] )
        MA_array.append(MA)
#        MD = Average( [abs(x - y) for x, y in zip(MA_array[i-19:i+1], TP[i-19:i+1])]  )
        MD = Average( [abs(x - MA) for x in TP[i-19:i+1]] )
    if ( i < CCI_period - 1 ):
        CCI_array.append(0)
    else:
        CCI_array.append ( ( TP[i] - MA ) / MD / 0.015 )
#    print TP[i], MA

    # MACD Part
for i in range(1, dmax):
    EMA12 = ( 2 * float(a200[i]) + 11 * EMA12 ) / 13
    EMA26 = ( 2 * float(a200[i]) + 25 * EMA26 ) / 27
    DIF = EMA12 - EMA26
    DEA_new = DEA_old * 8 / 10 + DIF * 2 / 10
    DIF_array.append(DIF)
    DEA_array.append(DEA_new)
    DEA_old = DEA_new

x = arange(1, dmax, 1)
#print len(x)
#DIF_array = x
#plot(x[400:], DIF_array[400:], x[400:], DEA_array[400:])
subplot(nsubplots,1,iprice)
plot(x[dmax-time_range-1:]-(dmax-time_range-1), a200[dmax - time_range:], 'k')
grid(True)
xindex = []
xdate = []
xinterval = 5
for i in range( 0, xinterval ):
    xindex.append( int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1 )
    xdate.append( str( date200[dmax - 1 - time_range + int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1] ) )
xindex.append( time_range )
xdate.append( str( date200[dmax - 1] ) )
xticks(xindex, xdate)
ylabel('PRICE     (USD)', fontsize=16)
title(name.upper() + '  Price and Indices in the past ' + str(time_range) + ' ' + periodText, fontsize = 18 ) 

# Plot CCI
#subplot(nsubplots,1,icci)
#plot(x[dmax-time_range-1:]-(dmax-time_range-1), CCI_array[dmax - time_range:], 'k')
#grid(True)
#xticks(xindex, xdate)
#ylabel('CCI_20', fontsize=16)

# Plot DMI
subplot(nsubplots,1,idmi)
plot(x[dmax-time_range-1:]-(dmax-time_range-1), DI14_positive[dmax - time_range:], 'b',linestyle=':')
plot(x[dmax-time_range-1:]-(dmax-time_range-1), DI14_negative[dmax - time_range:], 'm', linestyle='--')
#plot(x[dmax-time_range-1:]-(dmax-time_range-1), DX[dmax - time_range:], 'g')
plot(x[dmax-time_range-1:]-(dmax-time_range-1), ADX[dmax - time_range:], 'k', linestyle='-')
grid(True)
xticks(xindex, xdate)
ylabel('DMI_14', fontsize=16)
lg = legend(['DI+', 'DI-', 'ADX'], loc='upper center', bbox_to_anchor=(1.049, 1.05))

subplot(nsubplots,1,imacd)
plot(x[dmax-time_range-1:]-(dmax-time_range-1), DIF_array[dmax-time_range-1:], 'b')
plot(x[dmax-time_range-1:]-(dmax-time_range-1), DEA_array[dmax-time_range-1:], 'r')
#xlabel('Date', fontsize=16)
ylabel('MACD     (USD)', fontsize=16)
globalmin = min([min(DIF_array[dmax-time_range-1:]), min(DEA_array[dmax-time_range-1:])])
globalmax = max([max(DIF_array[dmax-time_range-1:]), max(DEA_array[dmax-time_range-1:])])
#for j in range( 0, 5):
#    text(time_range - j * xinterval - float(time_range) / 40.0, globalmin - (globalmax - globalmin) * 0.2, date200[dmax-1-j * xinterval],color='blue')
lg = legend(['DIF', 'MACD'], loc='upper center')
lg.draw_frame(False)
grid(True)
xticks(xindex, xdate)
#xticks([i * 5 for i in range(1, time_range / 5)])
#title('[12, 26, 9] MACD Curves for ' + name.upper() + ' in the recent ' + str(time_range) + ' ' + periodText )
if ( predict == True):
    cash = 1.0
    ns = 0
    nborrow = 0
    ntrade = 0
    ngain = 0
    nloss = 0
    total_gain = 0.0
    total_loss = 0.0
    top = []
    itop = []
    bottom = []
    ibottom = []
    iabove = 1
    ibelow = 1
    imax = 1
    maxd = -99999.0
    imin = 1
    mind = 99999.0
    imaxprice = 1
    maxprice = -99999.0
    iminprice = 1
    minprice = 99999.0
    above_active = False
    below_active = False

    found_low_MACD = False
    found_low_ADX = False
    last_low_MACD = 0
    last_low_ADX = 0

    real_high = False

    total_vector = []
    gain_result_vector = []

    for i in range( dmax - 1 - time_range, dmax - 1):
        total = cash + ns * float(a200[i+1]) - nborrow * float(a200[i+1])
        total_vector.append( total )
        gain_result = 0.0
#        print i, "    ", a200[i+1], "   ", total, date200[i+1]
        correct = False
        buy = False
        sell = False
        DIF_slope = DIF_array[i] - DIF_array[i-1]
        DEA_slope = DEA_array[i] - DEA_array[i-1]

        if ( DIF_array[i-1] < DEA_array[i-1] and DIF_array[i-2] > DIF_array[i-1] and DIF_array[i] > DIF_array[i-1] ):
            found_low_MACD = True
            last_low_MACD = i
            
        if ( DIF_slope < 0 and DIF_array[i-1] > DEA_array[i-1] and DIF_array[i] < DEA_array[i] ):
            sell = True
            subplot(nsubplots,1,imacd)
            axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')

        # Make decision based on CCI
#        if ( CCI_array[i] < 100 and CCI_array[i+1] >= 100 ):
#            buy = True
#            subplot(nsubplots,1,icci)
#            axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')

#        if ( CCI_array[i] > -100 and CCI_array[i+1] <= -100 ):
#            sell = True
#            subplot(nsubplots,1,icci)                                                                             
#            axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed') 

        # Make decision based on DMI
        if ( ADX[i+1] < ADX[i] and ADX[i-1] < ADX[i] ):
            found_low_ADX = True
            if ( i - last_low_MACD <= 3 ):
                buy = True
                subplot(nsubplots,1,imacd)
                axvline(x = last_low_MACD - (dmax-time_range-1) + 1, linewidth=1, color='g')
                subplot(nsubplots,1,idmi)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')

#        if ( DI14_positive[i] > DI14_negative[i] and DI14_positive[i+1] < DI14_negative[i+1] and ADX[i+1] >= 25 ):
#            sell = True
#            subplot(nsubplots,1,idmi)
#            axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')

        if ( buy ):
            if ( nborrow > 0 ):
                subplot(nsubplots,1,iprice)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                ntrade = ntrade + 1
                cash = cash - nborrow * float(a200[i+1])
                if ( float(a200[i+1]) < borrow_price ):
                    ngain = ngain + 1
                    gain = nborrow * (borrow_price - float(a200[i+1]))
                    gain_result = gain
                    total_gain = total_gain + gain
#                    file.write(str(ntrade) + '     ' + str(gain) + '\n')
                else:
                    nloss = nloss + 1
                    loss = nborrow * (borrow_price - float(a200[i+1]))
                    gain_result = loss
                    total_loss = total_loss + loss
#                    file.write(str(ntrade) + '     ' + str(loss) + '\n')
                nborrow = 0
            if ( ns == 0 ):
                subplot(nsubplots,1,iprice)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
#                subplot(nsubplots,1,iprice)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
#                subplot(nsubplots,1,icci)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                ns = cash / float(a200[i+1])
                if ( ns > 0 ):
                    cash = cash - ns * float(a200[i+1])
                    buy_price = float(a200[i+1])
                    buy_date = i - (dmax-time_range-1) + 1

        if ( sell ):    
            if ( ns > 0 ):
                subplot(nsubplots,1,iprice)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
#                subplot(nsubplots,1,iprice)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
#                subplot(nsubplots,1,icci)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
#                print 'Bought on ', date200[(dmax-time_range-1) + buy_date], ' @ ', buy_price, '; Sell on ', date200[i+1], ' @ ', a200[i+1]
                ntrade = ntrade + 1
                cash = cash + ns * float(a200[i+1])
                if ( float(a200[i+1]) > buy_price ):
                    ngain = ngain + 1
                    gain = ns * (float(a200[i+1]) - buy_price)
                    gain_result = gain
                    total_gain = total_gain + gain
#                    file.write(str(ntrade) + '     ' + str(gain) + '\n')
                else:
                    nloss = nloss + 1
                    loss = ns * (float(a200[i+1]) - buy_price)
                    gain_result = loss
                    total_loss = total_loss + loss
#                    file.write(str(ntrade) + '     ' + str(loss) + '\n')
                ns = 0
            if ( nborrow == 0 ):
                subplot(nsubplots,1,iprice)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
#                subplot(nsubplots,1,iprice)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
#                subplot(nsubplots,1,icci)
#                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
                nborrow = cash / float(a200[i+1])
                if ( nborrow > 0 ):
                    cash = cash + nborrow * float(a200[i+1])
                    borrow_price = float(a200[i+1])
                    borrow_date = i - (dmax-time_range-1) + 1
        gain_result_vector.append( gain_result )
#    file.close()
    ref_total = 1.0 / float(a200[dmax - 1 - time_range + 1]) * (-float(a200[dmax - 1 - time_range + 1]) + float(a200[dmax - 1])) + 1.0
    if ( ngain == 0 ):
        avg_gain = 'NA'
    else:
        avg_gain = total_gain / ngain
    if ( nloss == 0 ):
        avg_loss = 'NA'
    else:
        avg_loss = total_loss / nloss
    print ntrade, ' ', ngain, ' ', nloss, ' ', avg_gain, ' ', avg_loss, total, ref_total, (total-ref_total)/ref_total*100

#figure()
x = arange(1, time_range + 1, 1)
subplot(nsubplots,1,ibalance)
xlim([1,time_range])
plot( x, total_vector )
#title(name.upper() + '  Balance and Gain/Loss in the past ' + str(time_range) + ' ' + periodText, fontsize = 18 )
xindex = []
xdate = []
xinterval = 5
for i in range( 0, xinterval ):
    xindex.append( int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1 )
#    print int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) )
    xdate.append( str( date200[dmax - 1 - time_range + int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1] ) )
xindex.append( time_range )
xdate.append( str( date200[dmax - 1] ) )
xticks(xindex, xdate, fontsize=12)
ylabel('Balance     (USD)', fontsize=16)
grid(True)
subplot(nsubplots,1,igain)
xlim([1,time_range])
vlines( x, [0], gain_result_vector, lw=4 )
axhline(0, color='black')
xticks(xindex, xdate, fontsize=12)
xlabel('Date', fontsize=16)
ylabel('Gain     (USD)', fontsize=16)
grid(True)

#figure()
#x = arange(1, time_range + 1, 1)
#subplot(nsubplots,1,3)
#xlim([1,time_range])
#plot( x, total_vector )
#title(name.upper() + '  Balance and Gain/Loss in the past ' + str(time_range) + ' ' + periodText, fontsize = 18 )
#xindex = []
#xdate = []
#xinterval = 5
#for i in range( 0, xinterval ):
#    xindex.append( int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1 )
#    print int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) )
#    xdate.append( str( date200[dmax - 1 - time_range + int ( math.ceil( float(i) * ( time_range - 1 ) / xinterval ) ) + 1] ) )
#xindex.append( time_range )
#xdate.append( str( date200[dmax - 1] ) )
#xticks(xindex, xdate, fontsize=12)
#ylabel('Balance     (USD)', fontsize=16)
#grid(True)
#subplot(nsubplots,1,4)
#xlim([1,time_range])
#vlines( x, [0], gain_result_vector, lw=4 )
#axhline(0, color='black')
#xticks(xindex, xdate, fontsize=12)
#xlabel('Date', fontsize=16)
#ylabel('Gain     (USD)', fontsize=16)
#grid(True)
savefig( './figures/' + name.upper() + '_' + periodText + '.pdf' )
