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
#  Dividend adjusted!                                                                                                           # 
Use_Dividend_Adjusted = False

if ( Use_Dividend_Adjusted ):
    readinIndex = 6
else:
    readinIndex = 4

# CCI parameters!!!                                                                                                              
CCI_period = 20

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

for i in range(1, dmax + 1):
    date200.append(a[i].split(',')[0])
    a200.append(a[i].split(',')[readinIndex])
#    HighP = float(a[i].split(',')[2]) / float(a[i].split(',')[4]) * float(a[i].split(',')[6])
    HighP = float(a[i].split(',')[2])
#    LowP = float(a[i].split(',')[3]) / float(a[i].split(',')[4]) * float(a[i].split(',')[6])
    LowP = float(a[i].split(',')[3])
    CloseP = float(a[i].split(',')[readinIndex]) 
    TP.append( (HighP + LowP + CloseP) / 3.0 )
#    print HighP, LowP, CloseP
a200.reverse()
date200.reverse()
TP.reverse()

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
subplot(5,1,1)
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
title(name.upper() + '  Price and MACD in the past ' + str(time_range) + ' ' + periodText, fontsize = 18 ) 

subplot(5,1,5)
plot(x[dmax-time_range-1:]-(dmax-time_range-1), CCI_array[dmax - time_range:], 'k')
grid(True)
xticks(xindex, xdate)
ylabel('CCI_20', fontsize=16)

subplot(5,1,2)
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
    cash = 100000
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

        if ( DIF_slope > 0 and DIF_array[i-1] < DEA_array[i-1] and DIF_array[i] > DEA_array[i] ):
#        if ( DIF_array[i-1] < DEA_array[i-1] and DIF_array[i] > DEA_array[i] ):
            iabove = iabove + 1
            buy = True

        if ( DIF_slope < 0 and DIF_array[i-1] > DEA_array[i-1] and DIF_array[i] < DEA_array[i] ):
            ibelow = ibelow + 1
            sell = True

        if ( DIF_array[i-1] < DEA_array[i-1] and DIF_array[i] > DEA_array[i] ):
            if ( iabove > 1 ):
                istart_above = i
                iprevmax = imax
                prevmax = maxd
                iprevmaxprice = imaxprice
                prevmaxprice = maxprice
                top = [DIF_array[i]]
                itop = [i]
            imax = i
            maxd = DIF_array[i]
            imaxprice = i+1
            maxprice = a200[i+1]
            above_active = True

        if ( DIF_array[i-1] > DEA_array[i-1] and DIF_array[i] < DEA_array[i] ):
            if ( ibelow > 1 ):
                istart_below = i
                iprevmin = imin
                prevmin = mind
                iprevminprice = iminprice
                prevminprice = minprice
                bottom = [DIF_array[i]]
                ibottom = [i]
            imin = i
            mind = DIF_array[i]
            iminprice = i+1
            minprice = a200[i+1]
            below_active = True

        if ( DIF_array[i] > DEA_array[i] or ( len( top ) == 1 and DIF_array[i-1] > DEA_array[i-1] ) ):
            if ( DIF_array[i] > maxd ):
                imax = i
                maxd = DIF_array[i]
            if ( a200[i+1] > maxprice ):
                imaxprice = i+1
                maxprice = a200[i+1]
            if ( iabove > 1 and above_active ):
                if ( len( top ) == 0 ):
                    top = [DIF_array[i]]
                    itop = [i]
                elif ( len( top ) == 1 ):
                    if ( DIF_array[i] >= top[0] ):
                        top[0] = DIF_array[i]
                        itop[0] = i
                    else:
                        if ( top[0] < prevmax ):
                            current_maxprice = max(a200[istart_above+1:i+1+1])
                            icurrent_maxprice = numpy.argmax(a200[istart_above+1:i+1+1])
                            if ( current_maxprice > prevmaxprice ):
                                buy = False
                                sell = True
                                itop_plot = [iprevmax - (dmax - 1 - time_range - 1), itop[0] - (dmax - 1 - time_range - 1)]
                                top_plot = [prevmax, top[0]]
                                subplot(5,1,2)
#                                plot(itop_plot, top_plot, 'g--')
                                plot(itop_plot, top_plot, 'g', linewidth=2.0)
                                itopprice_plot = [iprevmaxprice - (dmax - 1 - time_range - 1) - 1, icurrent_maxprice + istart_above - (dmax - 1 - time_range - 1)]                                
                                topprice_plot = [prevmaxprice, current_maxprice]
                                subplot(5,1,1)
#                                plot(itopprice_plot, topprice_plot, 'r--')
                                plot(itopprice_plot, topprice_plot, 'r', linewidth=2.0)
                        above_active = False

        if ( DIF_array[i] < DEA_array[i] or ( len( bottom ) == 1 and DIF_array[i-1] < DEA_array[i-1] ) ):                    
            if ( DIF_array[i] < mind ):
                imin = i
                mind = DIF_array[i]
            if ( a200[i+1] < minprice ):
                iminprice = i+1
                minprice = a200[i+1]
            if ( ibelow > 1 and below_active ):
                if ( len( bottom ) == 0 ):
                    bottom = [DIF_array[i]]
                    ibottom = [i]
                elif ( len( bottom ) == 1 ):
                    if ( DIF_array[i] <= bottom[0] ):
                        bottom[0] = DIF_array[i]
                        ibottom[0] = i
                    else:
                        if ( bottom[0] > prevmin ):
                            current_minprice = min(a200[istart_below+1:i+1+1])
                            icurrent_minprice = numpy.argmin(a200[istart_below+1:i+1+1])
                            if ( current_minprice < prevminprice ):
                                buy = True
                                sell = False
                                ibottom_plot = [iprevmin - (dmax - 1 - time_range - 1), ibottom[0] - (dmax - 1 - time_range - 1)]
                                bottom_plot = [prevmin, bottom[0]]
                                subplot(5,1,2)
                                plot(ibottom_plot, bottom_plot, 'b', linewidth=2.0)
                                ibottomprice_plot = [iprevminprice - (dmax - 1 - time_range - 1) - 1, icurrent_minprice + istart_below - (dmax - 1 - time_range - 1)]
                                bottomprice_plot = [prevminprice, current_minprice]
                                subplot(5,1,1)
                                plot(ibottomprice_plot, bottomprice_plot, 'r', linewidth=2.0)
                        below_active = False

        if ( buy ):
            if ( nborrow > 0 ):
                subplot(5,1,1)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                subplot(5,1,2)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                #                print i - (dmax-time_range-1)
#                print 'Borrow on ', date200[(dmax-time_range-1) + borrow_date], ' @ ', borrow_price, '; Return on ', date200[i+1], ' @ ', a200[i+1]
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
                subplot(5,1,1)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                subplot(5,1,2)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='g')
                ns = int(cash / float(a200[i+1]))
                if ( ns > 0 ):
                    cash = cash - ns * float(a200[i+1])
                    buy_price = float(a200[i+1])
                    buy_date = i - (dmax-time_range-1) + 1
        if ( sell ):    
            if ( ns > 0 ):
                subplot(5,1,1)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
                subplot(5,1,2)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
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
                subplot(5,1,1)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
                subplot(5,1,2)
                axvline(x = i - (dmax-time_range-1) + 1, linewidth=1, color='r',linestyle='dashed')
                nborrow = int(cash / float(a200[i+1]))
                if ( nborrow > 0 ):
                    cash = cash + nborrow * float(a200[i+1])
                    borrow_price = float(a200[i+1])
                    borrow_date = i - (dmax-time_range-1) + 1
        gain_result_vector.append( gain_result )
#    file.close()
    ref_total = int(100000 / float(a200[dmax - 1 - time_range + 1])) * (-float(a200[dmax - 1 - time_range + 1]) + float(a200[dmax - 1]) ) + 100000
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
subplot(5,1,3)
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
subplot(5,1,4)
xlim([1,time_range])
vlines( x, [0], gain_result_vector, lw=4 )
axhline(0, color='black')
xticks(xindex, xdate, fontsize=12)
xlabel('Date', fontsize=16)
ylabel('Gain     (USD)', fontsize=16)
grid(True)
if not os.path.exists( name.upper() ):
    os.makedirs( name.upper() )
savefig( './' + name.upper() + '/' + name.upper() + '_' + periodText + '.pdf' )
