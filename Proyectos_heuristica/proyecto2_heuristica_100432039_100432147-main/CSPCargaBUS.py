
from constraint import *
import sys
import math
import random

# Poner en el terminal = pip install python-constraint por si te da error.

#pos0 --> Id: identificador del alumno
#pos1 --> Ciclo: 1/2 (primer/segundo ciclo)
#pos2 --> Conflictivo: C/X (Conflictivo/No conflictivo)
#pos3 --> Movilidad: R/X (M. reducida/sin M. reducida)
#pos4 --> IdHermanos: Id del hermano (0 si no tiene)

DOMINIO = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [17, 18, 19, 20],
    [21, 22, 23, 24],
    [25, 26, 27, 28],
    [29, 30, 31, 32],
]

alumnos_conflictivos = []
alumnos_conflictivos_no_hermano = []
alumnos_conflictivos_hermano = []
alumnos_no_conflictivos = []
alumnos_movilidad_reducida = []
alumnos_movilidad = []
alumnos_con_hermano = []
alumnos_sin_hermano = []
alumnos = []

def solve():
    problem = Problem()

    for x in datos:
        if x[1] == 1:
            if x[3] == 'R':
                problem.addVariable(x[0], [1, 2, 3, 4, 13, 14, 15, 16])
            else:
                problem.addVariable(x[0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

        elif x[1] == 2:
            if x[3] == 'R':
                if x[4] == 0:
                    problem.addVariable(x[0], [17, 18, 19, 20])
                else:
                    for j in datos:
                        if x[4] == j[0] and j[1] == 1:
                            problem.addVariable(x[0], [1, 2, 3, 4, 13, 14, 15, 16])
                        elif x[4] == j[0] and j[1] == 2:
                            problem.addVariable(x[0], [17, 18, 19, 20])
            else:
                if x[4] == 0:
                    problem.addVariable(x[0], [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
                else:
                    for j in datos:
                        if x[4] == j[0] and j[1] == 1:
                            if j[3] == 'R':
                                problem.addVariable(x[0], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
                            else:
                                problem.addVariable(x[0], [2, 3, 6, 7, 10, 11, 12, 15])
                        elif x[4] == j[0] and j[1] == 2:
                            problem.addVariable(x[0], [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
            
        if x[2] == 'C':
            alumnos_conflictivos.append(x[0])
        if x[2] == 'C' and x[4] == 0:
            alumnos_conflictivos_no_hermano.append(x[0])
        if x[2] == 'C' and x[4] != 0:
            alumnos_conflictivos_hermano.append(x[0])
        elif x[2] == 'X':
            alumnos_no_conflictivos.append(x[0])

        if x[3] == 'R':
            alumnos_movilidad_reducida.append(x[0])
        elif x[3] == 'X':
            alumnos_movilidad.append(x[0])

        if x[4] == 0:
            alumnos_sin_hermano.append(x[0])
        elif x[4] != 0 and x[3] == 'X': 
            for i in range(0, len(datos)-1):
                if datos[i][0] == x[4] and datos[i][3] == 'X':
                    alumnos_con_hermano.append(x[0])
                    alumnos_con_hermano.append(x[4])

        alumnos.append(x[0])


    # Restricción 1: todos los alumnos se sientan en sitios diferentes.
    problem.addConstraint(AllDifferentConstraint(), alumnos)

    # Restricción 2: los alumnos de movilidad reducida no se pueden sentar juntos.
    # problem.addConstraint(no_movilidad_reducida_pegados, alumnos_movilidad_reducida)
    
    # Restricción 3: los alumnos de movilidad reducida no pueden tener a nadie al lado.
    for alumno in alumnos_movilidad_reducida:
        temp = []
        for mov in alumnos:
            temp.append(mov)
        temp.append(alumno)
        problem.addConstraint(nadie_cerca, temp)

    # Restricción 4: los alumnos conflictivos que no sean hermano tienen que estar separados.
    problem.addConstraint(conflictivos, alumnos_conflictivos_no_hermano)

    # Restricción 5: los alumnos conflictivos que tienen hermanos tienen que estar separados del resto de alumnos conflictivos.
    for conflictivo in alumnos_conflictivos_hermano:
        temp = []
        for alumno in alumnos_conflictivos_no_hermano:
            temp.append(alumno)
        temp.append(conflictivo)
        problem.addConstraint(conflictivo_cerca, temp)
        temp = []

    # Restricción 6: los alumnos conflictivos tienen que sentrase separados de los alumnos con movilidad reducida.
    for conflictivo in alumnos_conflictivos:
        temp = []
        for alumno in alumnos_movilidad_reducida:
            temp.append(alumno)
        temp.append(conflictivo)
        problem.addConstraint(conflictivo_cerca, temp)


    # Restricción 7: los hermanos se sientan juntos.
    problem.addConstraint(funcion_hermanos, alumnos_con_hermano)

    solutions = problem.getSolutions()
    return solutions



def no_movilidad_reducida_pegados(*alumnos):
    for alumno1 in alumnos:
        for alumno2 in alumnos:
            if alumno1 != alumno2:
                if (alumno1 % 2 == 0 and alumno2 == alumno1-1) or (alumno1 % 2 == 1 and alumno2 == alumno1+1):
                    return False
    return True

def nadie_cerca (*alumnos):
    for i in range(0, len(alumnos)-1):
        if alumnos[i] != alumnos[-1]:
            if (alumnos[-1] % 2 == 0 and alumnos[i] == alumnos[-1]-1) or (alumnos[-1] % 2 == 1 and alumnos[i] == alumnos[-1] + 1):
                return False
    return True

def conflictivos (*alumnos):
    for alumno1 in alumnos:
        for alumno2 in alumnos:
            if alumno1 != alumno2:
                if alumno1 % 4 == 0:
                    if alumno2 == alumno1-5 or alumno2 == alumno1-4 or alumno2 == alumno1-1 or alumno2 == alumno1+3 or alumno2 == alumno1+4:
                        return False

                elif alumno1 % 4 == 3 or alumno1 % 4 == 2:
                    if alumno2 == alumno1-5 or alumno2 == alumno1-4 or alumno2 == alumno1-3 or alumno2 == alumno1-1 or alumno2 == alumno1+1 or alumno2 == alumno1+3 or alumno2 == alumno1+4 or alumno2 == alumno1+5:
                        return False

                elif alumno1 % 4 == 1:
                    if alumno2 == alumno1-4 or alumno2 == alumno1-3 or alumno2 == alumno1+1 or alumno2 == alumno1+4 or alumno2 == alumno1+5:
                        return False
    return True

def conflictivo_cerca (*alumnos):
    for i in range(0, len(alumnos)-1):
        if alumnos[i] != alumnos[-1]:
            if alumnos[i] % 4 == 0:
                if alumnos[i] == alumnos[-1]-5 or \
                   alumnos[i] == alumnos[-1]-4 or \
                   alumnos[i] == alumnos[-1]-1 or \
                   alumnos[i] == alumnos[-1]+3 or \
                   alumnos[i] == alumnos[-1]+4:
                    return False

            elif alumnos[i] % 4 == 3 or alumnos[i] % 4 == 2:
                if alumnos[i] == alumnos[-1]-5 or \
                    alumnos[i] == alumnos[-1]-4 or \
                    alumnos[i] == alumnos[-1]-3 or \
                    alumnos[i] == alumnos[-1]-1 or \
                    alumnos[i] == alumnos[-1]+1 or \
                    alumnos[i] == alumnos[-1]+3 or \
                    alumnos[i] == alumnos[-1]+4 or \
                    alumnos[i] == alumnos[-1]+5:
                    return False

            elif alumnos[i] % 4 == 1:
                if alumnos[i] == alumnos[-1]-4 or \
                    alumnos[i] == alumnos[-1]-3 or \
                    alumnos[i] == alumnos[-1]+1 or \
                    alumnos[i] == alumnos[-1]+4 or \
                    alumnos[i] == alumnos[-1]+5:
                    return False
    return True 

def funcion_hermanos (*alumnos):
    for i in range(0, len(alumnos), 2):
        if (alumnos[i] % 2 == 0 and alumnos[i+1] != alumnos[i]-1) or (alumnos[i] % 2 == 1 and alumnos[i+1] != alumnos[i]+1):
                    return False
    return True

def showSolutions(solutions):

    resultado = {}
    sys.stdout = open(file_input+ ".output", "w")
    print("Found %d solutions!" % len(solutions))
    for z in range(0,5,1):
        if len(solutions) > 0:
            x = random.randint(0,len(solutions)-1)
            for i in solutions[x]:
                for j in datos:
                    if i == j[0]:
                        resultado.update({str(i)+j[2]+j[3]:solutions[x][i]})
            resultado_ordenado = {key:value for key, value in sorted(resultado.items(), 
            key=lambda item:item[1])}

            print(resultado_ordenado)
            for row in range(len(DOMINIO)):
                if row == 4:
                    sys.stdout.write(" [] [] | [] []")
                    sys.stdout.write("\n")
                    sys.stdout.write(" [] [] | [] []")
                    sys.stdout.write("\n")
                for col in range(len(DOMINIO[row])):
                    id = DOMINIO[row][col]
                    write = False
                    for i in solutions[x]:
                        if id == solutions[x][i]:
                            if math.ceil(i/10) == 1:
                                if i == 10:
                                    sys.stdout.write(" %s" % (str(i)))
                                    write = True
                                else:
                                    sys.stdout.write("  %s" % (str(i)))
                                    write = True
                            else:
                                sys.stdout.write(" %s" % (str(i)))
                                write = True
                    if write == False:
                        sys.stdout.write("  X")
                    if col == 1:
                        sys.stdout.write(" |")
                sys.stdout.write("\n")


def openFile(input_file):

    try:
        test1 = open(input_file, "r")
        return test1
    except FileNotFoundError:
        print("Error: File does not appear to exist")
        raise
        print("Error: File does not appear to exist")
        raise


file_input = sys.argv[1]
test1 = openFile(str(file_input))

# Instanciacion de los alumnos extraidos del fichero de entrada
datos = []
lineas = test1.readlines()
for linea in lineas:
    alumno = []
    lane = linea.strip()
    elementos = lane.split(",")
    datos.append(elementos)

for i in range(0,len(datos)):
    datos[i][0] = int(datos[i][0])
    datos[i][1] = int(datos[i][1])
    datos[i][4] = int(datos[i][4])

solutions = solve()
showSolutions(solutions)