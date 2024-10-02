from openai import OpenAI
import streamlit as st

OPENAI_API_KEY = st.secrets['API_KEY']

# API key para OpenAI
client = OpenAI(api_key = OPENAI_API_KEY)

##################################################
# interfaz en streamlit
##################################################
def main():

    bg='''
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://img.freepik.com/premium-photo/wine-wooden-table-background-blurred-wine-shop-with-bottles_191555-1126.jpg?w=1060");
    bacjground-size: container;
    }
    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }
    </style>
    '''

    st.markdown(bg, unsafe_allow_html = True)

    # Título
    st.title('Recomendaciones de vinos')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mensaje inicial
    with st.chat_message('assistant', avatar='🍷'):
        st.markdown('¡Hola! Soy tu asistente personal que te ayudará a escoger el vino ideal para tus alimentos. ¿En qué alimento estás pensando?')

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message['role'] == 'assistant':
            avatar = '🍷'
            with st.chat_message(message['role'], avatar = avatar):
                st.markdown(message["content"])
        else:
            with st.chat_message(message['role']):
                st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ingresa tu pregunta:"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.


        ### INPUTS:
        # question -- str - texto de pregunta a hacerse

        ### OUTPUTS:
        # stream - texto de respuesta de la IA conforme lo va generando

        stream = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:tae::AB12SPoT",
        messages=[
            {"role": "system", "content": "Eres un asistente de ventas especializado en vinos. Tu función es recomendar únicamente los siguientes vinos: Cava Segura Viudas Reserva Heredad Brut, Vino Blanco Zuccardi Serie A Torrontes, Vino Tinto Casta Cirio, Vino Tinto Chateau St. Jean Merlot, Vino Tinto José Zuccardi Malbec, Vino Tinto Le Dix de los Vasco, Vino Tinto Queulat Gran Reserva Carmenere, Vino Tinto Tributo Palafox Tempranillo Cabernet, Vino Tinto Zuccardi Emma Bonarda, Vino Tinto Zuccardi Q Malbec, Vino Tinto Carmelo Rodero Crianza, Vino Tinto Carmelo Rodero Reserva, Vino Tinto Dominio de Tares Cepas Viejas, Vino Tinto Dominio de Tares Bembibre, Vino Tinto Carmelo Rodero Roble 9 meses, Vino Tinto Stags Leap Cabernet Sauvignon, Vino Tinto Brolio Chianti Classico, Vino Tinto Casalferro Barone Ricasoli, Vino Tinto Oddero Barolo, Vino Tinto Barone Ricasoli Castello Di Brolio, Vino Blanco Chablis Moreau, Vino Tinto Emevé Cabernet Sauvignon, Vino Tinto Emevé Shiraz, Vino Tinto Norton Malbec Reserva, Vino Tinto Catena Malbec, Vino Tinto Norton Privada, Vino Tinto Château Chasses Spleen, Vino Blanco Stags Leap Chardonnay, Vino Tinto El Coto De Imaz Reserva, Vino Tinto Gran Ricardo, Vino Tinto Marqués De Cáceres Crianza, Vino Tinto Marqués De Cáceres Reserva, Vino Tinto Marqués De Cáceres Gaudium Reserva, Vino Tinto Mauro Cosecha, Vino Tinto Prima, Vino Tinto Resalte Origen, Vino Tinto Mongrana IGT, Vino Blanco Paco Y Lola Albariño, Vino Tinto Nebbiolo Langhe Pio Cesare, Vino Tinto Pago de los Capellanes Crianza, Vino Tinto Tres Picos de Borsao, Vino Tinto San Román, Espumoso Segura Viudas Brut Reserva, Vino Tinto Ventisquero Vertice."}, {"role": "user", "content": "Hoy voy a comer un ribeye a la parrilla, ¿qué vino me recomiendas?"}, {"role": "assistant", "content": "Para un ribeye a la parrilla, te recomiendo los siguientes vinos: Carmelo Rodero Crianza, Stags Leap Cabernet Sauvignon, José Zuccardi Malbec, Gran Ricardo, Norton Privada. (Si la pregunta no es sobre comida o vino, simplemente di que tu función es recomendar vinos)."},
            {"role": "user", "content": prompt}
        ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant", avatar='🍷'):
            response = st.write_stream(stream)
        avatar='🍷'
        st.session_state.messages.append({"role": "assistant", "content": response, 'avatar': avatar})

        
if __name__ == "__main__":
    main()
