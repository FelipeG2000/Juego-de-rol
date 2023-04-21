import requests
from selectorlib import Extractor


class CaracteristicasPrincipales:
    """
    Clase que almacena las características principales de un personaje, obtenidas mediante web scrapping
    """
    id = 1
    
    # URL base de la wiki en la que se obtendrán las características
    url_estatica = 'https://nwn-espanol.fandom.com/es/wiki/'
    
    # User-Agent para las peticiones web
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
     
    def __init__(self, nombre, clan) :
        """
        Constructor de la clase CaracteristicasPrincipales.
        
        Args:
        - nombre: string con el nombre del personaje
        - clan: string con el clan del personaje
        """
        self.id = CaracteristicasPrincipales.id
        CaracteristicasPrincipales.id += 1
        self.__nombre_ = nombre
        self.__clan_ = clan
        self.url_completa = self.url_estatica + clan
        
        # Inicialización del extractor de la información de la página web y obtención de las características
        self.scrapping = Extractor.from_yaml_file('webscrapping.yml')
        response = requests.get(self.url_completa, headers=self.headers)
        self.diccionario = self.scrapping.extract(response.text)
        
    @property
    def nombre(self):
        """
        Devuelve el nombre del personaje
        """
        return self.__nombre_
    
    @property
    def clan(self):
        """
        Devuelve el clan del personaje
        """
        return self.__clan_
    
    @property
    def descripcion(self):
        """
        Devuelve la descripción del personaje
        """
        return self.diccionario.get('description')
    
    @property
    def ataque_base(self):
        """
        Devuelve el valor del ataque base del personaje
        """
        return self.diccionario.get('speed')
    
    @property
    def habilidades_de_clase(self):
        """
        Devuelve las habilidades de clase del personaje
        """
        return self.diccionario.get('skills')
    
    @property
    def competencias(self):
        """
        Devuelve las competencias del personaje
        """
        return self.diccionario.get('stats')
    
    @nombre.setter
    def nombre(self,nuevo_nombre):
        """
        Establece un nuevo nombre para el personaje
        """
        self.__nombre_ = nuevo_nombre
        
    def __str__(self):
        """
        Devuelve el nombre del personaje como string
        """
        return self.nombre       
    
class Guerrero(CaracteristicasPrincipales):
    """
    Esta clase define a un guerrero, que es un personaje de tipo 'Guerrero'.
    Con esta misma estructura se crearan las clases del resto de personajes. 
    """
    def __init__(self, name='', clan='Guerrero'):
        """
        Constructor de la clase Guerrero.
        
        :param name: nombre del guerrero.
        :type name: str.
        :param clan: nombre del clan del guerrero.
        :type clan: str.
        """
        super().__init__(name, clan)
        
    def destreza(self):
        """
        Devuelve la destreza del guerrero.
        """
        return f'Ataca!'
        
    def poder(self,personaje):
        """ 
        Devuelve el ataque del guerrero
        """
        if self == personaje:
            return f'{self.nombre} esta muy mal herido por las batallas pasadas'
        return f'¡{self.nombre} arremete contra {personaje.nombre} con furia!'    
        
class Mago(CaracteristicasPrincipales):
    #personaje principal, con la misma estructura del guerrero
    def __init__(self, name = '', clan = 'Mago'):
        super().__init__(name, clan)
        
    def destreza(self):
        """
        Devuelve la destreza del mago
        """
        return f'Lanzar hechizos¡'
    
    def poder(self, enemigo):
        """
        Devuelve el poder del mago 
        """
        if self == enemigo:
            return f'{self.nombre} Recivio una contra al lanzar sus hechizos, reciviendo daño de estos'
        return f'{self.nombre} esta lanzando hechizos mortales a {enemigo.nombre}'
        
class Hechicero(CaracteristicasPrincipales):
    #Personaje principal con la misma estructura del guerrero 
    def __init__(self, name = '', clan = 'Hechicero'):
        super().__init__(name, clan)
        
    def destreza(self):
        """
        Devuelve la destreza de la clase de hechicero
        """
        return f'Conjurar hechizos¡'
    
    def poder(self, enemigo):
        if self == enemigo:
            return f'A {self.nombre} le salieron mal los conjuros, padesiendo de una enfermedad destructiva '
        return f'{self.nombre} esta conjurando pociones para usar en contra de {enemigo.nombre}'
            
#tanto el explorador como el clerigo tienen herencia multiple, y estos tambien heredan las cosas ta heredadas de los perosnajes 
class Explorador(Guerrero,Hechicero):
    def __init__(self, name='', clan='Explorador'):
        super().__init__(name, clan)

    def destreza(self):
        """
        Devuelve la destreza de clase del personaje explorador
        """
        return f'Trepa'
    
    def poder(self, vacio=None):
        """
        Devuelve el poder de clase del personaje al trepar
        """
        return f'{self.nombre} esta trepando'

class Clerigo(Guerrero,Mago):
    #Se vuelve a definir su clase ya que a diferencia del resto de personajes, esta no conincide con la que se usa para hacer web scrapping
    clan_ = 'Clèrigo'
    def __init__(self, name = '', clan = 'Cl%C3%A9rigo'):
        super().__init__(name, clan)
    
    @property
    def clan(self):
        """
        Devuelve el nombre del clan del personaje clerigo
        """
        return self.clan_

    def destreza(self):
        """
        Devuelve la destreza de clase del personaje clerigo
        """
        return f'Cura heridos'

    def poder(self, aliado):
        """
        Devuelve el poder de clase del personaje al curar a un aliado
        """
        if self == aliado:
            return f'{self.nombre} Esta usando su poder para salvarse a si mismo '
        return f'{self.nombre} esta usando su poder para salvar a {aliado.nombre}'