# chatbot/mcp_integration.py

SPOTIFY_MCP_PATH = r"C:\REDES\MoodST\mcp\spotifyserver.py"

# Historial temporal de búsquedas
spotify_history = []

def search_song(query: str, limit: int = 5):
    """
    Función mock para búsqueda de canciones.
    Devuelve resultados de prueba si el MCP de Spotify no está activo.
    """
    try:
        # Aquí iría la llamada real al MCP server
        # response = spotify_client.call_tool(...)
        # Simulamos un error de conexión y devolvemos datos de prueba
        raise ConnectionError("Simulación de MCP de Spotify no disponible")
    except Exception as e:
        print(f"⚠ Error al buscar canción: {e}")
        # Retornamos resultados de prueba
        results = [
            {"id": "1", "name": f"{query} Song 1", "artists": ["Artista A"]},
            {"id": "2", "name": f"{query} Song 2", "artists": ["Artista B"]},
            {"id": "3", "name": f"{query} Song 3", "artists": ["Artista C"]},
        ]
        spotify_history.extend(results[:limit])
        return results[:limit]

def create_playlist(name: str, track_ids: list, public: bool = True):
    """
    Función mock para crear playlist.
    Devuelve URL de prueba.
    """
    print(f"✅ Playlist '{name}' creada con {len(track_ids)} canciones (simulación).")
    return f"http://fake.spotify/{name.replace(' ', '_')}"

def add_to_history(tracks):
    """Agrega canciones al historial mock"""
    spotify_history.extend(tracks)

def get_history():
    """Obtiene historial mock"""
    return spotify_history
