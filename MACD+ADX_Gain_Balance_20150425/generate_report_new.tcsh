#!bin/tcsh

set time_range = 200 
set today = `date | awk '{print $2, $3, $6}'`
set nstock = `wc -l stocklist.dat | awk '{print $1}'`
set method = MACD

rm summary.dat.*

foreach stock(`cat stocklist.dat`)
echo $stock
./main.py $stock d ${time_range} 1 | awk '{printf "%10s%12s%12s%12s%15.2f%15.2f%16.2f%16.2f%10.2f\n", "'$stock'", $1, $2, $3, $4, $5, $6, $7, $8}' >> summary.dat.${time_range}.d
./main.py $stock w ${time_range} 1 | awk '{printf "%10s%12s%12s%12s%15.2f%15.2f%16.2f%16.2f%10.2f\n", "'$stock'", $1, $2, $3, $4, $5, $6, $7, $8}' >> summary.dat.${time_range}.w
./main.py $stock m ${time_range} 1 | awk '{printf "%10s%12s%12s%12s%15.2f%15.2f%16.2f%16.2f%10.2f\n", "'$stock'", $1, $2, $3, $4, $5, $6, $7, $8}' >> summary.dat.${time_range}.m
end

cat > summary.tex <<EOF
\documentclass{article} % For LaTeX2e
\usepackage{nips14submit_e,times}
\usepackage{hyperref}
\usepackage{url}
%\documentstyle[nips14submit_09,times,art10]{article} % For LaTeX 2.09

\usepackage{graphicx}

\usepackage{float}
%\usepackage{subfig}
%\usepackage[]{algorithm2e}
%\usepackage{algorithm}
    %\usepackage{algorithmic}
\usepackage{url}%refer to website
\usepackage{caption}
%\usepackage{subcaption}
%\usepackage{subfigure}
\usepackage{color}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{graphics}
\usepackage{epsfig}
\usepackage{subfigure}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{amsmath}


\newcommand{\argmin}{\arg\!\min}
\DeclareMathOperator{\Tr}{Tr}
\bibliographystyle{abbrv}


\title{Title}

\author{
Guangsha Shi, Weimin Wang\\\
Department of Materials Science and Engineering\\\
University of Michigan, Ann Arbor, MI-48105, USA\\\
}

% The \author macro works with any number of authors. There are two commands
% used to separate the names and addresses of multiple authors: \And and \AND.
%
% Using \And between authors leaves it to \LaTeX{} to determine where to break
% the lines. Using \AND forces a linebreak at that point. So, if \LaTeX{}
% puts 3 of 4 authors names on the first line, and the last on the second
% line, try using \AND instead of \And before the third author name.

\newcommand{\fix}{\marginpar{FIX}}
\newcommand{\new}{\marginpar{NEW}}


\nipsfinalcopy % Uncomment for camera-ready version
\graphicspath{{./figures/}}

\begin{document}
\maketitle
\input{./body/abstract}
\input{./body/intro}
\input{./body/figures}
\input{./body/tables}
\small
%\scriptsize
%\input{reference}
\normalsize

\end{document}

EOF

mkdir body

cat > ./body/abstract.tex <<EOF
\begin{abstract}
Stock market indicators including MACD, CCI, and DMI are studied in this project and applied to QQQ, DIA, and IWM, daily, weekly, and monthly.
\end{abstract}
EOF

cat > ./body/intro.tex <<EOF
\section{Introduction}
Cited from StockCharts.com

\subsection{Moving Average Convergence/Divergence Oscillator (MACD)}
Developed by Gerald Appel in the late seventies, the Moving Average Convergence/Divergence oscillator (MACD) is one of the simplest and most effective momentum indicators available. The MACD turns two trend-following indicators, moving averages, into a momentum oscillator by subtracting the longer moving average from the shorter moving average. As a result, the MACD offers the best of both worlds: trend following and momentum. The MACD fluctuates above and below the zero line as the moving averages converge, cross and diverge. Traders can look for signal line crossovers, centerline crossovers and divergences to generate signals. Because the MACD is unbounded, it is not particularly useful for identifying overbought and oversold levels.

Calculation:

MACD Line: (12-day EMA - 26-day EMA)

Signal Line: 9-day EMA of MACD Line

MACD Histogram: MACD Line - Signal Line

The MACD Line is the 12-day Exponential Moving Average (EMA) less the 26-day EMA. Closing prices are used for these moving averages. A 9-day EMA of the MACD Line is plotted with the indicator to act as a signal line and identify turns. The MACD Histogram represents the difference between MACD and its 9-day EMA, the Signal line. The histogram is positive when the MACD Line is above its Signal line and negative when the MACD Line is below its Signal line.

The values of 12, 26 and 9 are the typical setting used with the MACD, however other values can be substituted depending on your trading style and goals.

Signal line crossovers are the most common MACD signals. The signal line is a 9-day EMA of the MACD Line. As a moving average of the indicator, it trails the MACD and makes it easier to spot MACD turns. A bullish crossover occurs when the MACD turns up and crosses above the signal line. A bearish crossover occurs when the MACD turns down and crosses below the signal line. Crossovers can last a few days or a few weeks, it all depends on the strength of the move.

In this report, we would focus on trading based on signal line crossovers.

\subsection{Commodity Channel Index (CCI)}
Developed by Donald Lambert and featured in Commodities magazine in 1980, the Commodity Channel Index (CCI) is a versatile indicator that can be used to identify a new trend or warn of extreme conditions. Lambert originally developed CCI to identify cyclical turns in commodities, but the indicator can successfully applied to indices, ETFs, stocks and other securities. In general, CCI measures the current price level relative to an average price level over a given period of time. CCI is relatively high when prices are far above their average. CCI is relatively low when prices are far below their average. In this manner, CCI can be used to identify overbought and oversold levels.

A CCI period of 20 is also used for the calculations of the simple moving average and Mean Deviation in this report.

CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)

Typical Price (TP) = (High + Low + Close)/3

Constant = .015

There are four steps to calculating the Mean Deviation. First, subtract 
the most recent 20-period average of the typical price from each period's 
typical price. Second, take the absolute values of these numbers. Third, 
sum the absolute values. Fourth, divide by the total number of periods (20). 

Lambert set the constant at .015 to ensure that approximately 70 to 80 percent of CCI values would fall between -100 and +100. This percentage also depends on the look-back period. A shorter CCI (10 periods) will be more volatile with a smaller percentage of values between +100 and -100. Conversely, a longer CCI (40 periods) will have a higher percentage of values between +100 and -100.

As noted above, the majority of CCI movement occurs between -100 and +100. A move that exceeds this range shows unusual strength or weakness that can foreshadow an extended move. Think of these levels as bullish or bearish filters. Technically, CCI favors the bulls when positive and the bears when negative. However, using a simple zero line crossovers can result in many whipsaws. Although entry points will lag more, requiring a move above +100 for a bullish signal and a move below -100 for a bearish signal reduces whipsaws.

The plue/minus 100 line crossovers would be used in this report for the determination of buy/sell.

\subsection{Average Directional Index (ADX), Directional Movement Index (DMI)}
The Average Directional Index (ADX), Minus Directional Indicator (-DI) and Plus Directional Indicator (+DI) represent a group of directional movement indicators that form a trading system developed by Welles Wilder. Wilder designed ADX with commodities and daily prices in mind, but these indicators can also be applied to stocks. The Average Directional Index (ADX) measures trend strength without regard to trend direction. The other two indicators, Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI), complement ADX by defining trend direction. Used together, chartists can determine both the direction and strength of the trend.

The calculation steps for the Average Directional Index (ADX) are detailed in each step. Average True Range (ATR) is Wilder's version of the two period trading range. Smoothed versions of Plus Directional Movement (+DM) and Minus Directional Movement (-DM) are divided by a smoothed version Average True Range (ATR) to reflect the true magnitude of a move. A 14-day ADX calculation is as follows:

1. Calculate the True Range (TR), Plus Directional Movement (+DM) and Minus Directional Movement (-DM) for each period.

2. Smooth these periodic values using the Wilder's smoothing techniques. These are explained in detail in the next section.

3. Divide the 14-day smoothed Plus Directional Movement (+DM) by the 14-day smoothed True Range to find the 14-day Plus Directional Indicator (+DI14). Multiply by 100 to move the decimal point two places. This +DI14 is the Plus Directional Indicator (green line) that is plotted along with ADX.

4. Divide the 14-day smoothed Minus Directional Movement (-DM) by the 14-day smoothed True Range to find the 14-day Minus Directional Indicator (-DI14). Multiply by 100 to move the decimal point two places. This -DI14 is the Minus Directional Indicator (red line) that is plotted along with ADX.

5. The Directional Movement Index (DX) equals the absolute value of +DI14 less - DI14 divided by the sum of +DI14 and - DI14.

6. After all these steps, it is time to calculate the Average Directional Index (ADX). The first ADX value is simply a 14-day average of DX. Subsequent ADX values are smoothed by multiplying the previous 14-day ADX value by 13, adding the most recent DX value and dividing this total by 14.

The Average Directional Index (ADX) is used to measure the strength or weakness of a trend, not the actual direction. Directional movement is defined by +DI and -DI. In general, the bulls have the edge when +DI is greater than - DI, while the bears have the edge when - DI is greater. Crosses of these directional indicators can be combined with ADX for a complete trading system.

Wilder put forth a simple system for trading with these directional movement indicators. The first requirement is for ADX to be trading above 25. This ensures that prices are trending. Many traders, however, use 20 as the key level. A buy signal occurs when +DI crosses above - DI. Wilder based the initial stop on the low of the signal day. The signal remains in force as long as this low holds, even if +DI crosses back below - DI. Wait for this low to be penetrated before abandoning the signal. This bullish signal is reinforced if/when ADX turns up and the trend strengthens. Once the trend develops and becomes profitable, traders will have to incorporate a stop-loss and trailing stop should the trend continue. A sell signal triggers when - DI crosses above +DI. The high on the day of the sell signal becomes the initial stop-loss.

The DI Crossover with ADX above 25 would be used in this project.
EOF

cat > ./body/figures.tex <<EOF
\section{Figures}
EOF

foreach stock(`cat stocklist.dat`)
cat >> ./body/figures.tex <<EOF
\begin{figure}
\centerline{\includegraphics[width=\paperwidth]{${stock}_days}}
\caption{
\label{fig:Price_${stock}_d}
}
\end{figure}

\begin{figure} 
\centerline{\includegraphics[width=\paperwidth]{${stock}_weeks}}
\caption{
\label{fig:Price_${stock}_w}
}
\end{figure} 

\begin{figure} 
\centerline{\includegraphics[width=\paperwidth]{${stock}_months}}
\caption{
\label{fig:Price_${stock}_m}
}
\end{figure} 

\clearpage
EOF
end

cat > ./body/tables.tex <<EOF
\section{Tables}

\begin{table}[H]
\caption{Performance in the past ${time_range} days based on the daily $method chart.}
\label{tab:days}
\begin{center}
\begin{tabular}{ccccccccc}
Stock name & Transactions & \#Gain & \#Loss & Avg\_Gain & Avg\_Loss & Balance & Ref\_Balance & \%Extra\\\
\hline
EOF
awk '{print $1 "&" $2 "&" $3 "&" $4 "&" $5 "&" $6 "&" $7 "&" $8 "&" $9 "\\\\" }' summary.dat.${time_range}.d >> ./body/tables.tex

cat >> ./body/tables.tex <<EOF
\hline
\end{tabular}
\end{center}
\end{table}
EOF

cat >> ./body/tables.tex <<EOF

\begin{table}[H]
\caption{Performance in the past ${time_range} weeks based on the weekly $method chart.}
\label{tab:weeks}
\begin{center}
\begin{tabular}{ccccccccc}
Stock name & Transactions & \#Gain & \#Loss & Avg\_Gain & Avg\_Loss & Balance & Ref\_Balance & \%Extra\\\   
\hline
EOF
awk '{print $1 "&" $2 "&" $3 "&" $4 "&" $5 "&" $6 "&" $7 "&" $8 "&" $9 "\\\\" }' summary.dat.${time_range}.w >> ./body/tables.tex

cat >> ./body/tables.tex <<EOF
\hline
\end{tabular}
\end{center}
\end{table}
EOF

cat >> ./body/tables.tex <<EOF

\begin{table}[H]
\caption{Performance in the past ${time_range} months based on the monthly $method chart.}
\label{tab:months}
\begin{center}
\begin{tabular}{ccccccccc}
Stock name & Transactions & \#Gain & \#Loss & Avg\_Gain & Avg\_Loss & Balance & Ref\_Balance & \%Extra\\\   
\hline
EOF
awk '{print $1 "&" $2 "&" $3 "&" $4 "&" $5 "&" $6 "&" $7 "&" $8 "&" $9 "\\\\" }' summary.dat.${time_range}.m >> ./body/tables.tex

cat >> ./body/tables.tex <<EOF
\hline
\end{tabular}
\end{center}
\end{table}
EOF
