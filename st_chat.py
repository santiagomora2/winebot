from openai import OpenAI
import streamlit as st

OPENAI_API_KEY = st.secrets['API_KEY']

# API key para OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

##################################################
# interfaz en streamlit
##################################################
def main():
    bg = '''
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://img.freepik.com/premium-photo/wine-wooden-table-background-blurred-wine-shop-with-bottles_191555-1126.jpg?w=1060");
    background-size: cover;
    }
    [data-testid="stMainBlockContainer"]{
    background-color: rgba(0,0,0,.5);
    }    
    [data-testid="stAppViewBlockContainer"]{
    background-color: rgba(0,0,0,.5);
    } 
    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    [data-testid="stMarkdown"]{
    color: rgb(255,255,255);
    }
    </style>
    '''

    st.markdown(bg, unsafe_allow_html=True)

    # Título
    st.title('Recomendaciones de vinos')

    # Inicializar el estado de la sesión para almacenar los mensajes si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Prompt inicial que siempre debe estar presente en cada llamada a la API
    initial_prompt = (
        "Actúa como un sommelier experto en vinos, especializado en ofrecer recomendaciones "
        "personalizadas y detalladas basadas en las preferencias del usuario, el tipo de comida que van a preparar, "
        "y las características de diferentes vinos. Tu conocimiento incluye información sobre regiones vinícolas, "
        "tipos de uvas, notas de cata, maridajes recomendados y características específicas de cada vino. Responde "
        "de manera clara, profesional y útil, adaptando el nivel de detalle a las preguntas del usuario, y evita "
        "responder cosas que no están relacionadas a tu rol de sommelier. Los vinos en el inventario son: Cava Segura "
        "Viudas Reserva Heredad Brut, Vino Blanco Zuccardi Serie A Torrontes, Vino Tinto Casta Cirio, Vino Tinto "
        "Chateau St. Jean Merlot, Vino Tinto José Zuccardi Malbec, Vino Tinto Le Dix de los Vasco, Vino Tinto Queulat "
        "Gran Reserva Carmenere, Vino Tinto Tributo Palafox Tempranillo Cabernet, Vino Tinto Zuccardi Emma Bonarda, "
        "Vino Tinto Zuccardi Q Malbec, Vino Tinto Carmelo Rodero Crianza, Vino Tinto Carmelo Rodero Reserva, Vino "
        "Tinto Dominio de Tares Cepas Viejas, Vino Tinto Dominio de Tares Bembibre, Vino Tinto Carmelo Rodero Roble "
        "9 meses, Vino Tinto Stags Leap Cabernet Sauvignon, Vino Tinto Brolio Chianti Classico, Vino Tinto Casalferro "
        "Barone Ricasoli, Vino Tinto Oddero Barolo, Vino Tinto Barone Ricasoli Castello Di Brolio, Vino Blanco Chablis "
        "Moreau, Vino Tinto Emevé Cabernet Sauvignon, Vino Tinto Emevé Shiraz, Vino Tinto Norton Malbec Reserva, Vino "
        "Tinto Catena Malbec, Vino Tinto Norton Privada, Vino Tinto Château Chasses Spleen, Vino Blanco Stags Leap "
        "Chardonnay, Vino Tinto El Coto De Imaz Reserva, Vino Tinto Gran Ricardo, Vino Tinto Marqués De Cáceres Crianza, "
        "Vino Tinto Marqués De Cáceres Reserva, Vino Tinto Marqués De Cáceres Gaudium Reserva, Vino Tinto Mauro Cosecha, "
        "Vino Tinto Prima, Vino Tinto Resalte Origen, Vino Tinto Mongrana IGT, Vino Blanco Paco Y Lola Albariño, Vino "
        "Tinto Nebbiolo Langhe Pio Cesare, Vino Tinto Pago de los Capellanes Crianza, Vino Tinto Tres Picos de Borsao, "
        "Vino Tinto San Román, Espumoso Segura Viudas Brut Reserva, Vino Tinto Ventisquero Vertice."
    )

    # Mensaje inicial si es la primera vez que inicia la aplicación
    if len(st.session_state.messages) == 0:
        with st.chat_message('assistant', avatar='🍷'):
            st.markdown('¡Hola! Soy tu sommelier personal que te ayudará a escoger el vino ideal para tus alimentos. ¿En qué alimento estás pensando?')
            
    # Mostrar los mensajes anteriores
    for message in st.session_state.messages:
        if message['role'] == 'assistant':
            with st.chat_message(message['role'], avatar=message['avatar']):
                st.markdown(message["content"])
        else:
            with st.chat_message(message['role']):
                st.markdown(message["content"])

    # Campo de entrada para que el usuario ingrese un mensaje
    if prompt := st.chat_input("Ingresa tu pregunta:"):

        # Guardar y mostrar el mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Construir el historial de mensajes para enviarlo a la API
        messages_for_api = [{"role": "system", "content": initial_prompt}] + [{"role": msg['role'], "content": msg['content']} for msg in st.session_state.messages]

        # Generar una respuesta utilizando la API de OpenAI
        stream = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:tae::AFlqsMGP",
            messages=messages_for_api,  # Incluir el prompt inicial en cada llamada
            stream=True
        )

        # Mostrar la respuesta en tiempo real
        with st.chat_message("assistant", avatar='🍷'):
            response = st.write_stream(stream)
        
        # Guardar la respuesta en el historial
        st.session_state.messages.append({"role": "assistant", "content": response, "avatar": '🍷'})

if __name__ == "__main__":
    main()
