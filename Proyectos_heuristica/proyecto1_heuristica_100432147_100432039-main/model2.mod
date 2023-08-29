/*VARIABLES MODELO.mod -> Parte 2*/

set Localizaciones;
set Paradas within Localizaciones;
set parking within Localizaciones;
set parada_s1 within Localizaciones;
set parada_s2 within Localizaciones;
set parada_s3 within Localizaciones;
set colegio within Localizaciones;
set numero_alumnos;

/*Establecemos variable de matriz de rutas -> binaria*/
var rutas {i in Localizaciones, j in Localizaciones} binary;

/*Establecemos variable de matriz del flujo de alumnos -> Entero*/
var flujo_alumnos {i in Localizaciones, j in Localizaciones} integer, >= 0;

/*Establecemos la matriz de asignación de paradas*/
var paradas_asignadas {i in numero_alumnos, j in Paradas} binary;

/*Actualizamos en número de alumnos en cada parada*/
var alumno_parada {i in Paradas};

/*Parámetros*/
param precio_rutas;
param precio_km_recorridos;
param coste_trayecto {i in Localizaciones, j in Localizaciones};
param autobuses_disponibles;
param capacidad_maxima_autobuses;
param hermanos {i in numero_alumnos, j in numero_alumnos} binary;
param posibilidades_alumnos {i in numero_alumnos, j in Paradas} binary;

/*FUNCIÓN OBJETIVO = > Minimizar el coste en las rutas*/
minimize Coste: (precio_rutas * sum{i in parking, j in Localizaciones} rutas[i,j]) + precio_km_recorridos * (sum{i in Localizaciones, j in Localizaciones} rutas[i,j] * coste_trayecto[i,j]);

/*RESTRICCIONES - > Primera parte*/
/*Restricciones de que a cada parada solo va una ruta*/
s.t. rutallega {i in Paradas} : sum{j in Localizaciones} rutas[i,j] <= 1;
/*Restricciones de que a cada parada solo sale una ruta*/
s.t. rutasale {j in Paradas} : sum{i in Localizaciones} rutas[i,j] <= 1;
/*Restricción salen el mismo numero de rutas que llegan*/
s.t. rutasparkingcolegio : sum{i in parking, j in Localizaciones} rutas[i, j] = sum{i in Localizaciones, j in colegio} rutas[i, j];
/*Restricción Restricción de que no salgan más del número de buses posibles*/
s.t. maximorutas : sum{i in parking, j in Localizaciones} rutas[i, j] <= autobuses_disponibles;
/*Restricción de que los buses no lleven más alumnos de su capacidad*/
s.t. flujo_alumnos_capacidad {i in Localizaciones, j in Localizaciones}: flujo_alumnos[i,j] <= capacidad_maxima_autobuses * rutas[i,j];
/*Restricciones de control del flujo para cada parada*/
s.t. flujoparadas {j in Paradas}: (sum{i in Localizaciones} flujo_alumnos[j,i]) = ((sum{i in Localizaciones} flujo_alumnos[i,j]) + alumno_parada[j]);

/*RESTRICCIONES - > Segunda parte*/
/*En cada parada no haya asignado más de 4 alumnos*/
s.t. num_alumnos_parada {j in Paradas} : sum{i in numero_alumnos} paradas_asignadas[i,j] <= capacidad_maxima_autobuses;
/*Cada alumno asignado a 1 parada*/
s.t. alumno_parada_asignada {i in numero_alumnos} : sum{j in Paradas} paradas_asignadas[i,j] = 1;
/*Cada asignación de alumno corresponde con las posibilidades de cada alumnos*/
s.t. asig_alumno_parada_posibilidad {i in numero_alumnos, j in Paradas} : paradas_asignadas[i,j] <= posibilidades_alumnos[i,j];
/*Cada hermano va a la misma parada*/
s.t. hermanos_misma_parada {j in Paradas, k in numero_alumnos}: sum {i in numero_alumnos} hermanos[i,k] * paradas_asignadas[i,j] = paradas_asignadas[k,j] * sum{l in numero_alumnos} hermanos[k,l];
/*Cada valor del vector*/
s.t. alumnosparada {j in Paradas} : alumno_parada[j] = sum{i in numero_alumnos} paradas_asignadas[i,j];
