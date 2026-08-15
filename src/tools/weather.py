from ..models import BaseTool, HTTPClient

from typing import Dict, Optional, List


class WeatherTool(BaseTool):
    def __init__(self, url: str = "https://wttr.in"):
        super().__init__()

        self.http = HTTPClient(base_url=url)

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Accept-Language": "ru",
            "Accept": "application/json"
        }

    @staticmethod
    def get_data(req: Dict) -> Dict[str, str]:
        weather_days: List[Dict] = req.get('weather', [])
        if not weather_days:
            raise ValueError
        
        today = weather_days[0]
        temp_min = today['mintempC']
        temp_max = today['maxtempC']
        
        hourly_data = today.get('hourly', [])
        hourly_wind = [float(h['windspeedKmph']) for h in hourly_data]
        wind_speed_avg = sum(hourly_wind) / len(hourly_wind) if hourly_wind else 0.0

        if 'current_condition' in req and req['current_condition']:
            current = req['current_condition'][0]
            
            temp_now = current['temp_C']
            humidity = current['humidity']
            precip = current['precipMM']
            wind_speed_now = current['windspeedKmph']
            
            if 'lang_ru' in current and current['lang_ru']:
                condition = current['lang_ru'][0]['value']
            else:
                condition = current['weatherDesc'][0]['value']
        else:
            midday = hourly_data[4] if len(hourly_data) > 4 else (hourly_data[0] if hourly_data else {})
            
            temp_now = midday.get('tempC', temp_min)
            humidity = midday.get('humidity', '0')
            precip = midday.get('precipMM', '0.0')
            wind_speed_now = midday.get('windspeedKmph', '0')
            
            if 'lang_ru' in midday and midday['lang_ru']:
                condition = midday['lang_ru'][0]['value']
            elif 'weatherDesc' in midday and midday['weatherDesc']:
                condition = midday['weatherDesc'][0]['value']
            else:
                condition = "Нет данных"

        return {
             "condition": condition,
             "humidity": humidity,
             "precip": precip,
             "temp_now": temp_now,
             "temp_min": temp_min,
             "temp_max": temp_max,
             "windspeed_now": wind_speed_now,
             "windspeed_avg": f"{wind_speed_avg:.1f}"
        }

    async def __call__(self, location: str, date: Optional[str] = None) -> Dict[str, str]:
        """Получает прогноз погоды на конкретную дату

        :param location: название города на английском языке, str
        :param date: дата в формате 'YYYY-MM-DD', Optional[str] default=None

        :returns Dict[str, Union[str, int, float]]: вернет {
             "condition": condition,
             "humidity": humidity,
             "precip": precip,
             "temp_now": temp_now,
             "temp_min": temp_min,
             "temp_max": temp_max,
             "windspeed_now": wind_speed_now,
             "windspeed_avg": wind_speed_avg
        """
        if date:
            url = f"/{location}@{date}?format=j1&m"
        else:
            url = f"/{location}?format=j1&m"

        req = await self.http.request(
            url=url, 
            headers=self.headers
        )
        json_data = req.json()

        return self.get_data(req=json_data)
