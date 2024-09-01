from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'Api_key'  

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={API_KEY}&contentType=json'
            response = requests.get(url)
            data = response.json()

            print("API Response:", data)

            if response.status_code == 200:
                try:
                    current_day = data['currentConditions']
                    weather_data = {
                        'city': data['address'],
                        'country': data['resolvedAddress'].split(', ')[-1],  
                        'temperature': current_day['temp'],
                        'humidity': current_day['humidity'],
                        'description': current_day['conditions'],
                        'icon': current_day['icon'] 
                    }
                except KeyError as e:
                    weather_data = {'error': f'Missing key in response: {e}'}
            else:
                error_message = data.get('message', 'Unknown error')
                weather_data = {'error': f'Error: {error_message}'}
    
    return render_template('index.html', weather=weather_data)


if __name__ == '__main__':
    app.run(debug=True)





