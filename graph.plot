set title 'Vélos et places de parkings disponibles des parkings les plus corrélé (0.9378) en fonction du temps'
set xdata time
set timefmt '%d/%m/%Y-%H:%M'
set format x '%H:%M'
set xlabel 'Heure de la journée du 27/01/2022 et 28/02/2022'
set ylabel 'Place de parkings disponibles'
set y2tics
set y2range [2:17]
set y2label 'Vélos disponibles'
set terminal png size 2000,1000 enhanced
set output 'graph.png'
plot 'graph.dat' using 1:2 with lines title 'Mosson voiture', 'graph.dat' using 1:3 with lines axes x1y2 title 'Renouvier vélo'
