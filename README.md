# ligamagic-card-price-searcher
Um script para procurar preços de deck de magic pelo liga magic

Exemplo: 
```
python3 main.py lista.txt output.csv


lista.txt:
4 Fanatical Firebrand (RIX) 101
4 Ghitu Lavarunner (DAR) 127
4 Goblin Chainwhirler (DAR) 129
3 Runaway Steam-Kin (GRN) 115
4 Viashino Pyromancer (M19) 166
20 Mountain (XLN) 273
2 Lightning Strike (XLN) 149
4 Risk Factor (GRN) 113
3 Shock (M19) 156
4 Wizard's Lightning (DAR) 152
4 Light Up the Stage (RNA) 107
4 Skewer the Critics (RNA) 115
2 Electrostatic Field (GRN) 97
3 Lightning Mare (M19) 151
3 Rekindling Phoenix (RIX) 111
1 Lightning Strike (XLN) 149
2 Fight with Fire (DAR) 119
3 Lava Coil (GRN) 108
1 Mountain (XLN) 273
```

O output gerado é:
```
name,quantity,price_min,price_med,price_max,total_min,total_med,total_max
"Fanatical Firebrand",4,0.20,1.16,10.00,0.80,4.64,40.00
"Ghitu Lavarunner",4,0.12,1.17,2.75,0.48,4.68,11.00
"Goblin Chainwhirler",4,16.99,25.13,57.47,67.96,100.52,229.88
"Runaway Steam-Kin",3,9.75,18.07,50.00,29.25,54.21,150.00
"Viashino Pyromancer",4,0.09,1.58,9.95,0.36,6.32,39.80
"Mountain",20,0.18,0.73,5.27,3.60,14.60,105.40
"Lightning Strike",2,0.25,1.54,14.00,0.50,3.08,28.00
"Risk Factor",4,18.00,30.71,78.00,72.00,122.84,312.00
"Shock",3,0.10,0.77,4.75,0.30,2.31,14.25
"Wizard's Lightning",4,4.31,8.29,29.99,17.24,33.16,119.96
"Light Up the Stage",4,7.99,14.37,48.00,31.96,57.48,192.00
"Skewer the Critics",4,3.25,5.90,59.99,13.00,23.60,239.96
"Electrostatic Field",2,0.20,1.40,7.00,0.40,2.80,14.00
"Lightning Mare",3,0.36,1.15,6.54,1.08,3.45,19.62
"Rekindling Phoenix",3,67.50,90.41,170.02,202.50,271.23,510.06
"Lightning Strike",1,0.25,1.54,14.00,0.25,1.54,14.00
"Fight with Fire",2,0.35,1.85,10.89,0.70,3.70,21.78
"Lava Coil",3,4.49,9.92,24.90,13.47,29.76,74.70
"Mountain",1,0.18,0.73,5.27,0.18,0.73,5.27

total min,456.03
total min,740.65
total min,2141.68
```

