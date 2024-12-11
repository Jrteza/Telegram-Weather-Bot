import nominatim 
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
import seaborn as sns
import io


def get_coordinates(city_name):
    api = nominatim.Nominatim()

    location = api.query(city_name, limit=1)

    if not location:
        raise TypeError

    lat = float(location[0]['lat'])
    lon = float(location[0]['lon'])

    return {
        "city": city_name,
        "latitude": round(lat,2),
        "longitude": round(lon,2),
    }

def data_temp(city_name, date_first, date_secoond):
    position = get_coordinates(city_name)
    cache_session = requests_cache.CachedSession('.cache', expire_after = 600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": position['latitude'],
        "longitude": position['longitude'],
        "start_date": date_first,
        "end_date": date_secoond,
        "hourly": ["temperature_2m"],
        "daily": "weather_code",  
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert(None),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert(None),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe = hourly_dataframe.reset_index(drop=True)
    hourly_dataframe.columns = ["date", "temperature_2m"]
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    return hourly_dataframe

def data_precipitation(city_name, date_first, date_secoond):
    position = get_coordinates(city_name)
    cache_session = requests_cache.CachedSession('.cache', expire_after = 600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": position['latitude'],
        "longitude": position['longitude'],
        "start_date": date_first,
        "end_date": date_secoond,
        "hourly": ["precipitation"],
        "daily": "weather_code",  
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert(None),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert(None),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["precipitation"] = hourly_temperature_2m
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe = hourly_dataframe.reset_index(drop=True)
    hourly_dataframe.columns = ["date", "precipitation"]
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    return hourly_dataframe

def data_surface_pressure(city_name, date_first, date_secoond):
    position = get_coordinates(city_name)
    cache_session = requests_cache.CachedSession('.cache', expire_after = 600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": position['latitude'],
        "longitude": position['longitude'],
        "start_date": date_first,
        "end_date": date_secoond,
        "hourly": ["surface_pressure"],
        "daily": "weather_code",  
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert(None),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert(None),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["surface_pressure"] = hourly_temperature_2m
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe = hourly_dataframe.reset_index(drop=True)
    hourly_dataframe.columns = ["date", "surface_pressure"]
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    return hourly_dataframe
# temperature group
def avg_day_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    avg = group['temperature_2m'].mean()
    return avg

def min_day_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    min = group['temperature_2m'].min()
    return min

def max_day_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    max = group['temperature_2m'].max()
    return max

def avg_month_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    avg = group['temperature_2m'].mean()
    return avg

def min_month_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    min = group['temperature_2m'].min()
    return min

def max_month_temp(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    max = group['temperature_2m'].max()
    return max
# surface_pressure group
def avg_day_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    avg = group['surface_pressure'].mean()
    return avg

def min_day_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    min = group['surface_pressure'].min()
    return min

def max_day_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    max = group['surface_pressure'].max()
    return max

def avg_month_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    avg = group['surface_pressure'].mean()
    return avg

def min_month_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    min = group['surface_pressure'].min()
    return min

def max_month_surface_pressure(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    max = group['surface_pressure'].max()
    return max
# precipitation group
def avg_day_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    avg = group['precipitation'].mean()
    return avg

def min_day_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    min = group['precipitation'].min()
    return min

def max_day_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='D')])
    max = group['precipitation'].max()
    return max

def avg_month_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    avg = group['precipitation'].mean()
    return avg

def min_month_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    min = group['precipitation'].min()
    return min

def max_month_precipitation(data_frame):
    group = data_frame.groupby([pd.Grouper(key='date', freq='ME')])
    max = group['precipitation'].max()
    return max

#plot temp
def plot_data_temperature(avg_temp, min_temp, max_temp, *, color='green', markers='.', type='barplot', flag=False):
    plt.figure(figsize=(12, 6)) 
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.xticks(rotation=60)
    plt.grid()

    if flag:
        plt.title('Температура')
        avg_temp['date'] = avg_temp['date'].dt.strftime('%b-%d %H:%M')
        sns.pointplot(x=avg_temp['date'], y=avg_temp['temperature_2m'], color=color, markers=markers) 
    else:
        plt.title('Средняя температура')
        sns.barplot(x=avg_temp.index, y=avg_temp.values, color=color) 
        sns.pointplot(x=min_temp.index, y=min_temp.values, color='blue', markers=markers)  
        sns.pointplot(x=max_temp.index, y=max_temp.values, color='red', markers=markers)  

    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    return buffer


#plot pressure
def plot_data_surface_pressure(avg_surface_pressure, min_surface_pressure, max_surface_pressure, *, color='green', markers='.', type='barplot', flag=False):
    plt.figure(figsize=(12, 6)) 
    plt.xlabel('Дата')
    plt.ylabel('Давление (гПа)')
    plt.xticks(rotation=60)
    plt.grid()

    if flag:
        plt.title('Давление')
        avg_surface_pressure['date'] = avg_surface_pressure['date'].dt.strftime('%b-%d %H:%M')
        sns.pointplot(x=avg_surface_pressure['date'], y=avg_surface_pressure['surface_pressure'], color=color, markers=markers) 
    else:
        plt.title('Среднее давление')
        sns.pointplot(x=avg_surface_pressure.index, y=avg_surface_pressure.values, color=color) 
        sns.pointplot(x=min_surface_pressure.index, y=min_surface_pressure.values, color='blue', markers=markers, alpha=0.5)  
        sns.pointplot(x=max_surface_pressure.index, y=max_surface_pressure.values, color='red', markers=markers, alpha=0.5)  

        x = range(len(avg_surface_pressure))

        plt.fill_between(
            x,
            max_surface_pressure,
            min_surface_pressure,
            where=(max_surface_pressure > min_surface_pressure),
            color='lightblue',
            alpha=0.5
        )   

    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    return buffer

#plot precipitation
def plot_data_precipitation(avg_precipitation, *, color='green', markers='.', type='barplot', flag=False):
    plt.figure(figsize=(12, 6))  
    plt.xlabel('Дата')
    plt.ylabel('Осадки (мм)')
    plt.xticks(rotation=60)
    plt.grid()

    if flag:
        plt.title('Осадки')
        avg_precipitation['date'] = avg_precipitation['date'].dt.strftime('%b-%d %H:%M')
        sns.pointplot(x=avg_precipitation['date'], y=avg_precipitation['precipitation'], color=color, markers=markers) 
    else:
        plt.title('Средние осадки')
        sns.barplot(x=avg_precipitation.index, y=avg_precipitation.values, color=color) 

    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    return buffer

# Description 
def analyze_temp(avg_temp, min_temp,max_temp, flag=False):
    if flag:
        description = f'''В течение анализируемого периода температура колебалась от {min(min_temp): .2f}°C до {max(max_temp): .2f}°C,
    средняя температура составила примерно {sum(avg_temp['temperature_2m']) / len(avg_temp['temperature_2m']): .2f}°C.
    Максимальная температура была зафиксирована {max_temp.idxmax().strftime('%Y-%m-%d')},
    а минимальная температура наблюдалась {min_temp.idxmin().strftime('%Y-%m-%d')}.'''
        return description
    description = f'''В течение анализируемого периода температура колебалась от {min(min_temp): .2f}°C до {max(max_temp): .2f}°C,
средняя температура составила примерно {sum(avg_temp) / len(avg_temp): .2f}°C.
Максимальная температура была зафиксирована {max_temp.idxmax().strftime('%Y-%m-%d')},
а минимальная температура наблюдалась {min_temp.idxmin().strftime('%Y-%m-%d')}.'''
    return description

def analyze_surface_pressure(avg_surface_pressure, min_surface_pressure, max_surface_pressure, flag=False):
    if flag:
        description = f'''В течение анализируемого периода атмосферное давление колебалось от {min(min_surface_pressure):.2f} гПа до {max(max_surface_pressure):.2f} гПа,
    среднее давление составило примерно {sum(avg_surface_pressure['surface_pressure']) / len(avg_surface_pressure['surface_pressure']):.2f} гПа.
    Максимальное давление было зафиксировано {max_surface_pressure.idxmax().strftime('%Y-%m-%d')},
    а минимальное давление наблюдалось {min_surface_pressure.idxmin().strftime('%Y-%m-%d')}.'''
        return description
    description = f'''В течение анализируемого периода атмосферное давление колебалось от {min(min_surface_pressure):.2f} гПа до {max(max_surface_pressure):.2f} гПа,
среднее давление составило примерно {sum(avg_surface_pressure) / len(avg_surface_pressure):.2f} гПа.
Максимальное давление было зафиксировано {max_surface_pressure.idxmax().strftime('%Y-%m-%d')},
а минимальное давление наблюдалось {min_surface_pressure.idxmin().strftime('%Y-%m-%d')}.'''
    return description

def analyze_precipitation(avg_precipitation, min_precipitation,max_precipitation, flag=False):
    if flag:
        description = f'''В течение анализируемого периода уровень осадков варьировался от {min(min_precipitation):.2f} мм до {max(max_precipitation):.2f} мм,
    средний уровень осадков составил примерно {sum(avg_precipitation['precipitation']) / len(avg_precipitation['precipitation']):.2f} мм.
    Максимальное количество осадков было зафиксировано {max_precipitation.idxmax().strftime('%Y-%m-%d')},
    а минимальное количество осадков наблюдалось {min_precipitation.idxmin().strftime('%Y-%m-%d')}.'''
        return description
    description = f'''В течение анализируемого периода уровень осадков варьировался от {min(min_precipitation):.2f} мм до {max(max_precipitation):.2f} мм,
средний уровень осадков составил примерно {sum(avg_precipitation) / len(avg_precipitation):.2f} мм.
Максимальное количество осадков было зафиксировано {max_precipitation.idxmax().strftime('%Y-%m-%d')},
а минимальное количество осадков наблюдалось {min_precipitation.idxmin().strftime('%Y-%m-%d')}.'''
    return description

