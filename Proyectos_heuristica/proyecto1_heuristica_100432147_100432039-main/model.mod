/*VARIABLES MODELO.mod*/

set Localizaciones;
set Paradas within Localizaciones;
set parking within Localizaciones;
set parada_s1 within Localizaciones;
set parada_s2 within Localizaciones;
set parada_s3 within Localizaciones;
set colegio within Localizaciones;

/*Establecemos variable de matriz de rutas -> binaria*/
var rutas {i in Localizaciones, j in Localizaciones} binary;

/*Establecemos variable de matriz del flujo de alumnos -> Entero*/
var flujo_alumnos {i in Localizaciones, j in Localizaciones} integer, >= 0;

/*Parámetros*/
param precio_rutas;
param precio_km_recorridos;
param coste_trayecto {i in Localizaciones, j in Localizaciones};
param autobuses_disponibles;
param capacidad_maxima_autobuses;
param alumno_parada {i in Localizaciones};

/*FUNCIÓN OBJETIVO = > Minimizar el coste en las rutas*/
minimize Coste: (precio_rutas * sum{i in parking, j in Localizaciones} rutas[i,j]) + precio_km_recorridos * (sum{i in Localizaciones, j in Localizaciones} rutas[i,j] * coste_trayecto[i,j]);

/*RESTRICCIONES*/
/*Restricciones de que a cada parada solo va una ruta*/
s.t. rutallega {i in Paradas} : sum{j in Localizaciones} rutas[i,j] = 1;

/*Restricciones de que a cada parada solo sale una ruta*/
s.t. rutasale {j in Paradas} : sum{i in Localizaciones} rutas[i,j] = 1;

/*Restricción salen el mismo numero de rutas que llegan*/
s.t. rutasparkingcolegio : sum{i in parking, j in Localizaciones} rutas[i, j] = sum{i in Localizaciones, j in colegio} rutas[i, j];

/*Restricción Restricción de que no salgan más de 3 rutas*/
s.t. maximorutas : sum{i in parking, j in Localizaciones} rutas[i, j] <= autobuses_disponibles;

/*Restricción de que los buses no lleven más alumnos de su capacidad*/
s.t. flujo_alumnos_capacidad {i in Localizaciones, j in Localizaciones}: flujo_alumnos[i,j] <= capacidad_maxima_autobuses * rutas[i,j];

/*Restricciones de control del flujo para cada parada*/
s.t. flujoparadas {j in Paradas}: (sum{i in Localizaciones} flujo_alumnos[j,i]) = ((sum{i in Localizaciones} flujo_alumnos[i,j]) + alumno_parada[j]);


