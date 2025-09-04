import urllib
from dotenv import load_dotenv
import functools
import requests
import json
import os
    
load_dotenv()
bot_key = os.getenv("BOT_API_KEY")
weather_key = os.getenv("WEATHER_API_KEY")
currency_key = os.getenv("CURRENCY_API_KEY")

def send_to_bot(method):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            url = f"https://api.telegram.org/bot{bot_key}/{method}"
            
            result = func(*args, **kwargs)
            
            if method == "sendPhoto":
                response = requests.post(url, data={'chat_id': '872029097', 'photo': result})
                response.raise_for_status()
                return result
            
            response = requests.post(url, data={'chat_id': '872029097', 'text': result})
            response.raise_for_status()
            return result
        return wrapper
    return decorator
        
@send_to_bot('sendMessage')
def weather_api_req(city: str) -> str :
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params={'q': city, 'appid': weather_key, 'units': 'metric'})
    
    response.raise_for_status()
    data = response.json()
    
    city = data["name"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    return f"""City: {city}
Temperature: {temperature} °C
Weather: {weather_description}
Humidity: {humidity}%"""

@send_to_bot('sendMessage')
def currency_api_req(currency: str) -> str :
    url = "https://api.exchangerate.host/convert"
    response = requests.get(url, params={
        'from': currency.upper(),
        'to': 'UAH',
        'amount': '1',
        'access_key': currency_key})
    
    response.raise_for_status()
    
    data = response.json()
    
    rate = data["result"]
    
    return f"1 {currency.upper()} = {rate:.2f} UAH"

@send_to_bot('sendMessage')
def translate_en_api_req(text: str, source_lang: str, target_lang: str) -> str:
    url = "https://api.mymemory.translated.net/get"
    response = requests.get(url, params={'q': text, 'langpair': f'{source_lang}|{target_lang}'})
    data = response.json()
    
    translation = data.get("responseData", {}).get("translatedText", None)
    
    return f"""Text: {text}
Translation: {translation}"""

@send_to_bot('sendMessage')
def cat_api_req(args: str) -> str :
    url = 'https://corporatebs-generator.sameerkumar.website/'
 
    return requests.get(url).json()['phrase']
 
@send_to_bot(method='sendPhoto')
def planet_api_req(args: str):
    url = f'https://api.bootprint.space/img/{args}'
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()['image']


if __name__ == "__main__":
    print("""Enter your requests (leave empty to exit)
Exambple:
    /weather Kyiv (target city)
    /currency USD (target currency)
    /translate UA (language source) EN (target language)
    /buzz-words
    /planet Mars (planet; works for Uranus, Mars, Mercury, Venus, Jupiter, Saturn) (doesn't work with 'Earth' for some reason)""" 
    )
    req = '.'
    while req:
        req = input('> ')
        temp = req.split(' ')
        path = temp[0]
        temp.pop(0)
        
        match path:
            case "/weather":
                weather_api_req(" ".join(temp))
            case "/currency":
                currency_api_req(" ".join(temp))
            case "/translate":
                text = input('Enter text to translate: ')
                translate_en_api_req(text, temp[0], temp[1])
            case "/buzz-words":
                cat_api_req(" ".join(temp))
            case "/planet":
                planet_api_req(" ".join(temp))