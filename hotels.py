from openai import OpenAI
import streamlit as st
from amadeus import Client, ResponseError, Location

AMADEUS_API_KEY = 'Q9GWN9iAAmRnIPhEZFDw5qWAkyhyKxEF'
AMADEUS_API_SECRET = 'SgPgcnlNT9AXQiKF'

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)
# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_city_code(user_str):
    system_input = """
    The user will provide an input which includes a city name. You have to return just the IATA code as shown
    example input : what are the available hotels in paris?
    output : PAR
    input : what are the available hotels in mumbai
    output: MUM
    input: hotels in hyderabad
    output:HYD
    """

    completion = client.chat.completions.create(
    model="RichardErkhov/meta-llama_-_Meta-Llama-3-8B-Instruct-gguf",
    messages=[
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_input}
    ],
    temperature=0.7, 
    max_tokens=10
    )

    # Extract the output content
    response = completion.choices[0].message.content.strip()

    # Remove leading and trailing backticks and any additional newlines
    clean_response = response.strip("` \n")

    # Print the cleaned response
    return clean_response



def search_hotels(citycode):
    try:
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=citycode).data
        
        
        return response
    except ResponseError as error:
        print(f"Error: {error}")
        return None
    
#par = get_city_code(user_input)
#print(search_hotels(par))

st.title("Hotel Search")

user_input = st.text_input("Enter hotel details required")

if user_input:
    city_code = get_city_code(user_input)
    if city_code:
        st.write(f"City Code: {city_code}")
        hotel_data = search_hotels(city_code)
        if hotel_data:
            st.write("Hotel Data:")
            st.write(hotel_data)  # Display the hotel data in a formatted JSON view
        else:
            st.write("No hotel data found.")
    else:
        st.write("Could not extract city code.")