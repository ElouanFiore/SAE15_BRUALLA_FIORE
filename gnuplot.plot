reset
set xdata time
set timefmt "%d/%m/%Y-%H:%M"
set format x "%H:%M"
plot "datagnuplot.dat" using 1:3 with lines