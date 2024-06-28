from gen_escenario import escenario
from gen_escenario_conprio import escenario_prioridad
from sol_escenario_diferencia import main
import time

if __name__ == '__main__':
    time.sleep(3)
    i=0
    t=1
    while i<=5:
        if i%2==0:
            escenario(t,3000)
            main(6000)
            i+=1
            t+=1
        else:
            escenario_prioridad(t,3000)
            main(6000)
            i+=1
            t+=1

