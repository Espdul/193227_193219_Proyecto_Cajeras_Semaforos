from tkinter import * 
import threading
import time
import random

class cajero(threading.Thread):

    def __init__(self, cajerasArray):
        threading.Thread.__init__(self)
        self.cajeras = cajerasArray #cajeras
        self.listaClientes = [0,0,0]  #lista de clientes 
        self.listaEspera = []  #lista de clientes en espera
        self.tiempo = [3,6,9]  #Tiempo que va a tardar en atender al cliente
        self.totalAcumulado = 0 #Para el total acumulado
        self.totalCajero = [0,0,0] #Total de ventas para cada cajero
        self.contador = 0 #Para saber que clientes estan en espera
        self.bandera = 0
   
    def terminarPrograma(self): #Para que se detenga el while y se cierre la ventana
        self.bandera = 1
        view.destroy()

    def clienteNuevo(self):
        listbox.insert(self.contador,"Cliente en espera") #Mostrar cliente en espera
        self.contador = self.contador + 1
        if self.contador > 0:
            submit2["state"] = DISABLED #Inhabilitar el boton de terminar programa
        for i in range(len(self.listaClientes)):
            if self.listaClientes[i] == 0: #Agregar cliente a la lista de clientes para atender
                self.listaClientes[i] = 1
                break
            else:
                if i == 2: #Si es la utlima posicion de la lista de clientes y no hay lugar se agrega al nuevo cliente a la lista de espera
                    self.listaEspera.append(1)
    
    def atenderlistaEspera(self): #Pasar clientes de la lista de espera a la lista de clientes
        for j in range(len(self.listaClientes)):
            if self.listaClientes[j] == 0:
                if len(self.listaEspera) > 0:
                    self.listaClientes[j] = 1
                    self.listaEspera.pop()
    
    def atenderCliente(self):
        while True:
            if self.bandera == 1:
                break
            else:
                for j in range(len(self.listaClientes)):
                    if self.listaClientes[j] == 1:
                        self.cajeras[j].acquire() 
                        self.cobrar(j)
            
    def cobrar(self,j):
        self.contador = self.contador - 1
        listbox.delete(self.contador) #Borrar cliente de la lista
        total = random.randint(0,100) 
        self.totalAcumulado = self.totalAcumulado + total
        self.totalCajero[j] = self.totalCajero[j] + total #Total para cada cajero
        if j == 0:
            cliente1.place(x = 620, y = 50) #Mostrar cliente
            estadocajera1_1.set("ATENDIENDO...") #CAMBIAR ESTADO DEL CAJERO
        elif j == 1:
            cliente2.place(x = 620, y = 250)  #Mostrar cliente
            estadocajera2_2.set("ATENDIENDO...") #CAMBIAR ESTADO DEL CAJERO
        elif j == 2:
            cliente3.place(x = 620, y = 450)  #Mostrar cliente
            estadocajera3_3.set("ATENDIENDO...") #CAMBIAR ESTADO DEL CAJERO
        tiempo = random.choice(self.tiempo)
        time.sleep(tiempo)
        self.listaClientes[j] = 0 #El cliente se iguala a 0 ya que esta atendido
        #CAMBIAR ESTADO DEL CAJERO
        if j == 0:
            estadocajera1_1.set("COBRANDO...")
            cajera1_1.set("Cajera 1 $" + str(self.totalCajero[j])) #Mostrar total del cajero 1
        elif j == 1:
            estadocajera2_2.set("COBRANDO...")
            cajera2_2.set("Cajera 2 $" + str(self.totalCajero[j]))  #Mostrar total del cajero 2
        elif j == 2:
            estadocajera3_3.set("COBRANDO...")
            cajera3_3.set("Cajera 3 $" + str(self.totalCajero[j]))  #Mostrar total del cajero 3
        time.sleep(3)
        totalAcumuladoR_R.set("$ "+str(self.totalAcumulado)) #Mostrar total acumulado
        #OCULTAR CLIENTE
        if j == 0:
            cliente1.place_forget()
            estadocajera1_1.set("DESOCUPADO")
        elif j == 1:
            cliente2.place_forget()
            estadocajera2_2.set("DESOCUPADO")
        elif j == 2:
            cliente3.place_forget()
            estadocajera3_3.set("DESOCUPADO") 
        self.cajeras[j].release()
        if self.contador == 0:
            submit2["state"] = NORMAL #Habilitar boton para terminar el programa
        self.atenderlistaEspera()  #Verificar si hay clientes en espera

    def run(self):
        self.atenderCliente()  
        
if __name__ == '__main__':
    cajerasArray = [1,1,1]
    for i in range(len(cajerasArray)):
        cajerasArray[i] = threading.Semaphore(1)  #Se utiliza semaforos 
    cajero = cajero(cajerasArray)
    cajero.start()
    view = Tk()
    view.title("Cajeras")
    view.resizable(0,0)
    frame = Frame()
    frame.config(bg = "#FFFFFF", width =1000, height =600)
    frame.pack()
    submit = Button(frame, text="Agregar cliente",width=15, command=cajero.clienteNuevo)
    submit.config(cursor="hand2")
    submit.place(x=800,y= 300)
    submit2 = Button(frame, text="Terminar programa",width=15, command=cajero.terminarPrograma)
    submit2.config(cursor="hand2")
    submit2.place(x=800,y= 500)
    clientes = StringVar()
    Label(view, text= clientes)
    cajeraimg = PhotoImage(file="cajera.png")
    cajera1 = Label(view, image= cajeraimg, width=300, height=150)
    cajera1.place(x = 300, y = 10)
    cajera2 = Label(view, image= cajeraimg, width=300, height=150)
    cajera2.place(x = 300, y = 200)
    cajera3 = Label(view, image= cajeraimg, width=300, height=150)
    cajera3.place(x = 300, y = 400)
    clienteimg = PhotoImage(file="cliente.png")
    cliente1 = Label(view, image=clienteimg, width=100, height=100)
    cliente1.place_forget()
    cliente2 = Label(view, image=clienteimg, width=100, height=100)
    cliente2.place_forget()
    cliente3 = Label(view, image=clienteimg, width=100, height=100)
    cliente3.place_forget()
    #Listabox para mostrar los clientes en espera
    listbox = Listbox(view, bg="#1E1E1E", fg="white") #Par en mostrar los clientes en espera
    listbox.place(x=100, y=10)
    listbox.pack()
    #Para mostrar los totales
    totalAcumulado = Label(view, text="Total acumulado", bg="#FFFFFF", font=("Arial", 15)).place(x=45, y=20)
    totalAcumuladoR_R = StringVar()
    totalAcumuladoR_R.set("$")
    totalAcumuladoR = Label(view,textvariable=totalAcumuladoR_R, bg="#FFFFFF", font=("Arial", 15)).place(x=55, y=55)
    cajera1_1 = StringVar()
    #Para mostrar el total de ventas de cada cajero
    cajera1_1.set("Cajera 1 $")
    labelCajera1 = Label(view, textvariable=cajera1_1, bg="#FFFFFF", font=("Arial", 15)).place(x=120, y=100)
    cajera2_2 = StringVar()
    cajera2_2.set("Cajera 2 $")
    labelCajera2 = Label(view, textvariable=cajera2_2, bg="#FFFFFF", font=("Arial", 15)).place(x=120, y=250)
    cajera3_3 = StringVar()
    cajera3_3.set("Cajera 3 $")
    labelCajera3 = Label(view, textvariable=cajera3_3, bg="#FFFFFF", font=("Arial", 15)).place(x=120, y=450)
    #Para mostrar el estado de cada cajero
    estadocajera1_1 = StringVar()
    estadocajera2_2 = StringVar()
    estadocajera3_3 = StringVar()
    estadoCajera1 = Label(view, textvariable=estadocajera1_1, bg="#FFFFFF", font=("Arial", 15)).place(x=620, y=15)
    estadoCajera2 = Label(view, textvariable=estadocajera2_2, bg="#FFFFFF", font=("Arial", 15)).place(x=620, y=200)
    estadoCajera3 = Label(view, textvariable=estadocajera3_3, bg="#FFFFFF", font=("Arial", 15)).place(x=620, y=400)

    view.mainloop()
