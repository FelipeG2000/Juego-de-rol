import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from clases import Guerrero,Mago,Hechicero,Explorador,Clerigo
import sqlite3
from PIL import Image, ImageTk
     
class Juego:
    """
    Clase que maneja los menús del juego.
    """

    personajes = ['Mago', 'Guerrero', 'Hechicero', 'Explorador', 'Clèrigo'] # Lista de personajes disponibles

    def __init__(self, jugadores, formato=('Arial', 12)):
        """
        Inicializa la clase Menus con los siguientes atributos:
        - jugadores: lista de jugadores
        - formato: tupla de dos elementos que especifica el tipo de fuente y su tamaño
        """
        self.jugadores = jugadores
        self.formato = formato
        self.imagenes = {}
        self.imagenes['Guerrero'] = None
        self.imagenes['Mago'] = None
        self.imagenes['Hechicero'] = None
        self.imagenes['Explorador'] = None
        self.imagenes['Clèrigo'] = None

    def crear_personaje(self, seleccion):
        """
        Método que crea un personaje dependiendo de la selección.
        """
        if seleccion == 'Mago':
            personaje = Mago()
        elif seleccion == 'Guerrero':
            personaje = Guerrero()
        elif seleccion == 'Hechicero':
            personaje = Hechicero()
        elif seleccion == 'Explorador':
            personaje = Explorador()
        elif seleccion == 'Clèrigo':
            personaje = Clerigo()
        else:
            return f'Personaje aún no especificado'
        return personaje

    def guardar_jugadores(self):
        """
        Método que guarda la lista de jugadores en una base de datos.
        """
        conn = sqlite3.connect('data_base.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS jugadores (id INTEGER, nombre TEXT, tipo TEXT)''')
        for jugador in self.jugadores:
            id = jugador.id
            nombre = jugador.nombre
            tipo = jugador.clan
            # Verificar si ya existe un registro con el mismo ID
            c.execute("SELECT id FROM jugadores WHERE id = ?", (jugador.id,))
            resultado = c.fetchone()
            if resultado is not None:
                pass
            else:
                c.execute("INSERT INTO jugadores (id, nombre, tipo) VALUES (?, ?, ?)",
                                (id, nombre, tipo))
        conn.commit()
        conn.close()
   
    def recuperar_personajes(self,ventana):
        """
        Metodo que recupera los personajes de la base de datos
        """
        try:
            # Conectarse a la base de datos
            conn = sqlite3.connect('data_base.db')
            c = conn.cursor()

            # Consultar la cantidad de filas en la tabla "personajes"
            c.execute("SELECT nombre, tipo FROM jugadores")
            resultado = c.fetchall()

            for nombre, tipo in resultado:
                personaje = self.crear_personaje(tipo)
                personaje.nombre = nombre
                self.jugadores.append(personaje)
            conn.close()
            ventana.destroy()
            self.menu()

        except ValueError:
            messagebox.showerror('Error','No has creado ninguna partida aun')
            ventana.destroy()
            self.primer_menu()
        
    def titulo(self, ventana, titulo):
        """ 
        Metodo para poner titulos de manera mas rapida y eficiente
        """
        mostrar_titulo = tk.Label(ventana, text=titulo, font=self.formato, anchor='center')
        mostrar_titulo.pack(pady=5)        
        
    def boton(self, ventana, boton_texto, comando):
        """ 
        Metodo para crear un boton de manera mas rapida y eficiente
        """
        boton = tk.Button(ventana, text=boton_texto, font=self.formato, command=comando)
        boton.pack(pady=10,side=tk.BOTTOM)
    
    def obtener(self,lista, ventana_agregar):
        """ 
        Metodo para recuperar la eleccion del usuario
        """
        seleccion = lista.curselection()
        if not seleccion:
            #Dado el caso de no haber eleccion mostrara una ventana emergente con un error 
            messagebox.showerror("Error", "Por favor seleccione una tarea.")
            return None
        else:
            return seleccion[0]
        
    def create(self):
        """ 
        Metodo para crear personajes en el juego, este reutiliza muchos de los metodos anteriores, y es uno de los metodos principales
        """
        ventana_agregar = tk.Toplevel()
        ventana_agregar.title('Crear personaje')

        # Crear el título centrado
        self.titulo(ventana_agregar,'¡Elige tu personaje favorito!')

        # Crear la lista centrada
        lista_frame = tk.Frame(ventana_agregar)
        lista_frame.pack(pady=5)
        lista = tk.Listbox(lista_frame, width=30, height=5, font=('Arial', 12))
        lista.pack(expand=True, fill='both', padx=10, pady=10)
        for opcion in self.personajes:
            lista.insert(tk.END, f'{opcion}')

        # Establecer el ancho de la ventana al ancho de la lista
        ancho_ventana = max(lista.winfo_reqwidth()+40, 320)
        ventana_agregar.geometry(f"{ancho_ventana}x300")

        # Crear el label y el entry centrados
        nombre_label = tk.Label(ventana_agregar, text='Nombre del personaje:', font=("Arial", 12), anchor="center")
        nombre_label.pack(pady=5)
        nombre_entry = ttk.Entry(ventana_agregar, width=30, font=("Arial", 12), style='EntryStyle.TEntry')
        nombre_entry.pack()
        def boton():
            #recupera la seleccion del usuario
            seleccion = self.obtener(lista,ventana_agregar)
            if seleccion == None:
                ventana_agregar.destroy()
                return
            personaje = self.crear_personaje(self.personajes[seleccion])
            if not nombre_entry.get():
                messagebox.showerror("Error", "Debes ponerle un nombre a tu personaje.")
                ventana_agregar.destroy()
                return
            else:
                nombre_personaje = nombre_entry.get()
                personaje.nombre = nombre_personaje
                self.jugadores.append(personaje)
                ventana_agregar.destroy()
        
        #establece el boton de crear
        self.boton(ventana_agregar, 'Crear', comando=boton)

    def personajes_creados(self):
        """
        Metodo para ver los personajes creados
        """
        if not self.jugadores:
            messagebox.showerror("Error", "No has creado personajes para realizar esta accion.")
            
        else:
            # Crear ventana de Tkinter
            ventana = tk.Tk()
            ventana.geometry("400x400")
            ventana.title("Personajes creados")
            
            self.titulo(ventana,'Personajes creados')
            
            # Crear etiqueta para la lista de personajes creados
            lista_personajes = tk.Text(ventana, width=30, height=5, font=self.formato)
            lista_personajes.pack(expand=True, fill='both',padx=10, pady=10)
            
            # Recorrer la lista de personajes y agregarlos a la etiqueta
            for i, personaje in enumerate(self.jugadores):
                texto_personaje = f'{i+1}. Nombre: {personaje.nombre}\n' + f'Tipo de personaje: {personaje.clan}\n'
                lista_personajes.insert(tk.END, texto_personaje)
            lista_personajes.config(state='disabled')
                
            # Crear botón para cerrar la ventana
            self.boton(ventana, 'Cerrar', ventana.destroy)
    
    def ver_detalles(self, personaje):
        """ 
        Metodo para ver los detalles de un personaje en particular
        """
        #creamos la ventana
        ventana = tk.Toplevel()
        ventana.geometry("550x400")
        ventana.title(f"Detalles de {personaje.nombre}")
        
        #ponemos el titulo de la ventana
        self.titulo(ventana,f'Detalles de {personaje.nombre}')
        
        #Creamos el cuadro de texto donde insertaremos los detalles del personaje
        texto = tk.Text(ventana, width=60, height=20, font=self.formato, wrap='word')
        
        #En este tipo de packs pondremos algunas restricciones para que los detalles no se vean mal
        texto.pack(expand=True, fill='both',padx=10, pady=10)
        
        #insertamos los detalles en el cuadro de texto 
        texto.insert(tk.END, f'{personaje.descripcion}\n\n')
        texto.insert(tk.END, f'{personaje.ataque_base}\n\n')
        texto.insert(tk.END, f'{personaje.habilidades_de_clase}\n\n')
        texto.insert(tk.END, f'{personaje.competencias}\n\n')
        
        #Desabilitamos la opcion de escribir sobre este cuadro de texto
        texto.config(state='disabled')
        
        #Le adicionamos una scrollbar en caso de ser necesaria
        scrollbar = tk.Scrollbar(ventana)
        scrollbar.pack(side='right', fill='y')
        texto.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=texto.yview)
         
    def elegir_personaje(self, titulo, encabezado, boton_nombre, funcion, lanzador = None):
        """ 
        Estructura para elegir un jugador entre los jugadores creados
        """
        #creamos la ventana
        ventana = tk.Toplevel()
        ventana.geometry("320x300")
        
        #Ponemos el titulo pasado como parametro de entrada
        ventana.title(titulo)
        
        #Ponemos el encabezado pasado como parametro de entrada
        mostrar_titulo = tk.Label(ventana, text=encabezado, font=self.formato, anchor='center')
        mostrar_titulo.pack(pady=5)
        
        #creamos la lista y adicionaremos los jugadores creados
        lista_frame = tk.Frame(ventana)
        lista_frame.pack(pady=5)
        lista = tk.Listbox(lista_frame, width=30, height=5, font=self.formato)
        lista.pack(expand=True, fill='both', padx=10, pady=10)
        for jugador in self.jugadores:
            lista.insert(tk.END, f'{jugador} -- {jugador.clan}')
        ancho_ventana = max(lista.winfo_reqwidth()+40, 320)
        ventana.geometry(f"{ancho_ventana}x300")
        
        #Creamos una subfuncion para crear las acciones que iran despues de presionar el boton
        def boton():
            #recuperamos la seleccion digitada por el usuario
            seleccion = self.obtener(lista,ventana)
            #Dado el caso de que no seleccione nada destruimos la ventana
            if seleccion == None:
                ventana.destroy()
                return
            
            #Recuperamos el jugador seleccionado
            personaje = self.jugadores[seleccion]
            
            #si el usuario digito un lanzador, lo pasaremos a la funcion, de lo contrario no lo haremos
            if lanzador is not None:
                funcion( lanzador, personaje)
            else:
                funcion(personaje)
            ventana.destroy()
        #creamos el boton con el nombre que haya digitado el usuario
        self.boton(ventana, boton_nombre,comando=boton)
         
    def lanzar(self, lanzador):
        """ 
        Metodo para pasar los parametros del personaje que lanzara el poder
        """
        #si la persona que realizara la habilidad es del tipo explorador, no le pasaremos personaje2
        if lanzador.clan == 'Explorador':
            self.despliegue(lanzador, personaje2=None)
        else:
            #se define bien el lanzador para, no haber errores de sintaxis
            self.elegir_personaje(lanzador.destreza(),f'¿{lanzador.nombre} a que personaje deseas {lanzador.destreza()}?', lanzador.destreza(), self.despliegue,lanzador=lanzador)
    
    def despliegue(self, personaje1, personaje2):
        """ 
        Metodo para hacer el despliegue del poder, mostrando una imagen representativa
        """
        #Creamos la ventana
        ventana = tk.Toplevel()
        ventana.title('Crear personaje')

        # cargar imágenes
        imagenes = {}
        imagenes['Guerrero'] = Image.open('imagenes/Guerrero.png')
        imagenes['Mago'] = Image.open('imagenes/Mago.png')
        imagenes['Hechicero'] = Image.open('imagenes/Hechicero.png')
        imagenes['Explorador'] = Image.open('imagenes/Explorador.png')
        imagenes['Clèrigo'] = Image.open('imagenes/Clèrigo.png')

        # redimensionar y convertir a ImageTk.PhotoImage
        self.imagenes = {}
        for nombre, imagen in imagenes.items():
            imagen_resized = imagen.resize((600,400), Image.ANTIALIAS)
            self.imagenes[nombre] = ImageTk.PhotoImage(imagen_resized)

        #Mostramos la imagen en pantalla segun el personaje que este lanzando su poder
        imagen = self.imagenes[personaje1.clan]
        etiqueta = tk.Label(ventana, text= personaje1.poder(personaje2),compound=tk.BOTTOM, font= self.formato)
        etiqueta['image'] = imagen
        etiqueta.pack(pady=10)
        self.boton(ventana, 'Cerrar', ventana.destroy)
        
    def detalles(self):
        """ 
        Metodo para ver los detalles de un personaje en particular
        """
        #Si no se han creado jugadores aun, mostraremos el mensaje de error, de lo contrario activademos la funcion elegir_personaje con los parametros necesarios
        if not self.jugadores:
            messagebox.showerror("Error", "No has creado personajes para realizar esta accion.")
        else:
            self.elegir_personaje('Detalle','Detalle del personaje', 'Detalles',self.ver_detalles)
        
    def habilidades(self):
        """ 
        Metodo para lanzar las habilidades de un personaje en particular
        """
        # De no haber personajes creados, lo mostraremos en pantalla 
        if not self.jugadores:
            messagebox.showerror("Error", "No has creado personajes para realizar esta accion.")
        else:
            #Si hay almenos un personaje, activaremos la funcion elegir_personaje con los parametros conrrespondientes 
            self.elegir_personaje('Habilidad', '¿Que personaje lanzara la habilidad?', 'Lanzar', self.lanzar)
  
    def salir(self,ventana):
        """ 
        Metodo para salir del juego, no sin antes guardar los personajes creados en la base de datos
        """
        self.guardar_jugadores()
        ventana.destroy()
              
    def menu(self):
        """ 
        Metodo para crear el menu principal
        """

        #creamos la ventana 
        ventana = tk.Tk()
        ventana.title("Juego rpg")
        ventana.geometry('300x300')
        
        #agregamos el titulo
        self.titulo(ventana, 'Menu principal')
        
        #agregamos los botonoes que activan las funciones correspondientes
        self.boton(ventana, 'Salir', comando = lambda : self.salir(ventana))

        self.boton(ventana, 'Habilidades especiales',self.habilidades)
        
        self.boton(ventana, 'Detalles',  self.detalles, )

        self.boton(ventana, 'Personajes creados',  self.personajes_creados)

        self.boton(ventana, 'Crear personajes', self.create)
      
        #ponemos que la ventana este en loop, para asi cerrar el ciclo
        ventana.mainloop()
        
    def primer_menu(self):
        """  
        Menu para indicar si es una nueva partida o cargar partida
        """
        
        #Creamos la ventana
        ventana = tk.Tk()
        ventana.title("Juego rpg")
        ventana.geometry('300x100')
        #Agregamos el boton de cargar partida, que activara la funcion de recuperar personajes
        self.boton(ventana, 'Cargar partida', lambda : self.recuperar_personajes(ventana))
        def nueva():
            """ 
            Funcion que de llama al persionar el boton de nueva partida, eliminara la partida anterior y dara paso 
            """
            # Conectarse a la base de datos
            conn = sqlite3.connect('data_base.db')
            c = conn.cursor()

            # Ejecutar la instrucción SQL para eliminar la tabla
            c.execute("DROP TABLE IF EXISTS jugadores")

            # Guardar los cambios
            conn.commit()

            # Cerrar la conexión
            conn.close()
            ventana.destroy()
            self.menu() 
        #se agrega el boton de nueva partida con la funcion previamente creada
        self.boton(ventana, 'Nueva partida', comando=nueva)
        ventana.mainloop()