set title "Indice de corrélation entre le nombre de vélos libres et le nombre de places libre dans les parkings"
set ylabel "Parking voiture"
set xlabel "Parking vélo"
set zlabel "Indice de corrélation"
set datafile separator comma
set terminal png size 2500,1000 enhanced
set output 'heatmap.png'
plot "heatmap.dat" matrix rowheaders columnheaders using 1:2:3 with image