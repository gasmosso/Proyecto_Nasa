# service.py
from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
from ...config import config
import requests

def getAllImages(input=None):
    try:
        # Obtener la colección de imágenes desde el módulo de transporte
        json_collection = transport.getAllImages(input)
        
        # Mapear la colección JSON a objetos NASACard
        images = []
        for item in json_collection:
            if 'links' in item and len(item['links']) > 0 and 'href' in item['links'][0]:
                try:
                    nasa_card = mapper.NASACard(
                        title=item['data'][0]['title'],
                        description=item['data'][0]['description'],
                        image_url=item['links'][0]['href'],
                        date=item['data'][0]['date_created']
                    )
                    images.append(nasa_card)
                except KeyError as e:
                    print(f"Error al mapear el objeto {item}: {e}")
            else:
                print(f"El objeto {item} no contiene la clave 'href' o la lista 'links' está vacía")
        
        return images
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud a la API de la NASA: {e}")
        return []


# def getAllImages(input=None):
#     # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
#     # ¡OJO! el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.
#     json_collection = []

#     images = []

#     # recorre el listado de objetos JSON, lo transforma en una NASACard y lo agrega en el listado de images. Ayuda: ver mapper.py.

#     return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una NASACard.
    fav.user = '' # le seteamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositorio TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            nasa_card = '' # transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.