import requests

BASE_URL = "http://localhost:8000/api/news"

news_items = [
    {
        "titulo": "Nueva Temporada de Jujutsu Kaisen confirmada",
        "subtitulo": "MAPPA revela detalles del arco de Culling Game",
        "contenido": "La espera ha terminado. El estudio MAPPA ha confirmado que la producción de la siguiente fase de Jujutsu Kaisen está en marcha. Se espera que explore eventos oscuros y batallas épicas...",
        "imagen_url": "https://piks.eldesmarque.com/bin/2023/12/28/jujutsu_kaisen_culling_game.jpg",
        "categoria": "Estrenos"
    },
    {
        "titulo": "Anime Expo 2026: Fechas anunciadas",
        "subtitulo": "El evento más grande de anime vuelve a Los Ángeles",
        "contenido": "Los organizadores de Anime Expo han revelado las fechas para la edición 2026. Los fans podrán disfrutar de paneles exclusivos, cosplays de primer nivel y anuncios de grandes franquicias...",
        "imagen_url": "https://www.anime-expo.org/wp-content/uploads/2023/07/AX2024_SocialSharing_1200x630.jpg",
        "categoria": "Eventos"
    },
    {
        "titulo": "Solo Leveling rompe récords de streaming",
        "subtitulo": "La adaptación del manhwa es un éxito global",
        "contenido": "Desde su estreno, Solo Leveling ha dominado las listas de popularidad en todas las plataformas de streaming, consolidándose como uno de los animes más vistos del año...",
        "imagen_url": "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2024/01/solo-leveling-ep-1.jpg",
        "categoria": "General"
    }
]

def seed():
    for item in news_items:
        try:
            response = requests.post(BASE_URL, json=item)
            if response.status_code == 201:
                print(f"Noticia creada: {item['titulo']}")
            else:
                print(f"Error al crear '{item['titulo']}': {response.text}")
        except Exception as e:
            print(f"Error conectando a la API: {e}")

if __name__ == "__main__":
    seed()
