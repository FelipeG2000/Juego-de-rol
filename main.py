from ventanas import Juego


def main():
    """ 
    Funcion principal, donde se iniciara la variable de personajes, y se accedera al juego 
    """
    personajes = []
    
    #Creamos la intancia en la clase de juego con el diccionario donde iremos almacenando los personajes
    intento1=Juego(personajes)
    
    #Activamos el juego llamando al primer menu
    intento1.primer_menu()

if __name__=='__main__':
    main()