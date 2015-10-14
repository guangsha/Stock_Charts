#!bin/tcsh

set time_range = 200 
set today = `date | awk '{print $2, $3, $6}'`
set nstock = `wc -l stocklist.dat | awk '{print $1}'`
set method = MACD+ADX

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


\title{MACD+ADX applied to nine stocks for 200 time periods, 05/10/2015}

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
 MACD+ADX is applied to QQQ, DIA, IWM, SPY, WMT, GS, EWH, EWG, and EWJ, daily, weekly, and monthly.
\end{abstract}
EOF

cat > ./body/intro.tex <<EOF
\section{Protocol}
In this study, we buy when DIF (faster line in MACD) and ADX kisses (ADX reaches local maximum when DIF is at local minimum), and sell at "death crossing" in MACD.
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
