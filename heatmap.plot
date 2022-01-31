set title "Indice de corrélation entre le nombre de vélos libres et le nombre de places libres dans les parkings"
set ylabel "Parkings voitures"
set xlabel "Parkings vélos"
set zlabel "Indice de corrélation"
set datafile separator comma
set terminal png size 2500,1000 enhanced
set output 'heatmap.png'
plot "heatmap.dat" matrix rowheaders columnheaders using 1:2:3 with image
