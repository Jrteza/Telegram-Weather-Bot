from aiogram.filters import Command # Для отлавливания команд в хендлере
from aiogram.types import Message, FSInputFile # Это для обработки сообщенийи файлов 
from aiogram import F, Router 
import weaher_func.Whether as ww # Отсюда достаем все по погоде
from aiogram.fsm.state import StatesGroup, State # Это классы для введения состояни человека
from aiogram.fsm.context import FSMContext # Это нужно для управления состоянием 
from openmeteo_requests.Client import OpenMeteoRequestsError
import app.text_comand as txt 
import re
import datetime

router = Router() # Router для связи с файлом telegram_bot и в нем с Dispatcher

# Структура данных (состояние) temperature
class Temperature_city(StatesGroup):
    city = State()
    first_date = State()
    second_date = State()

# Структура данных (состояние) precipitation
class Precipitation_city(StatesGroup):
    city = State()
    first_date = State()
    second_date = State()

# Структура данных (состояние) surface_pressure
class Surface_pressure_city(StatesGroup):
    city = State()
    first_date = State()
    second_date = State()


# Обработка команды старт 
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(txt.comand_start)
    
@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer(txt.comand_help)


# функцуия для обработки запроса 
@router.message(Command('Temperature_plot'))
async def city_name(message: Message, state: FSMContext):
    await state.set_state(Temperature_city.city)
    await message.answer('Введите название города на английском')
    
@router.message(Temperature_city.city)
async def first_date(message: Message, state: FSMContext):
    if re.match(r'^[a-zA-Z\s]+$', message.text):
        await state.update_data(city=message.text)
        await state.set_state(Temperature_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Temperature_city.city)
        await message.answer('Введите название города на английском')

@router.message(Temperature_city.first_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(first_date=message.text)
        await state.set_state(Temperature_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Temperature_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')

@router.message(Temperature_city.second_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(second_date=message.text)
        data = await state.get_data()
        await state.clear()
    else:
        await state.set_state(Temperature_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    try:
        data['first_date'] = datetime.datetime.strptime(data['first_date'], "%Y-%m-%d")
        data['second_date'] = datetime.datetime.strptime(data['second_date'], "%Y-%m-%d")
        if data['first_date'] > data['second_date']:
            time = data['first_date']
            data['first_date'] = data['second_date']
            data['second_date'] = time
        temp = ww.data_temp(data['city'], datetime.datetime.strftime(data['first_date'], '%Y-%m-%d'), datetime.datetime.strftime(data['second_date'], '%Y-%m-%d'))
        await message.answer(f'Погода в {data["city"]} с {datetime.datetime.strftime(data['first_date'], '%Y-%m-%d')} по {datetime.datetime.strftime(data['second_date'], '%Y-%m-%d')}')
        if (data['second_date'] - data['first_date']).days < 2:
            avg_temp = temp
            min_temp = ww.min_day_temp(temp)
            max_temp = ww.max_day_temp(temp)
            flag = True
        elif (data['second_date'] - data['first_date']).days < 40:
            avg_temp = ww.avg_day_temp(temp)
            min_temp = ww.min_day_temp(temp)
            max_temp = ww.max_day_temp(temp)
            flag = False
        else:
            avg_temp = ww.avg_month_temp(temp)
            min_temp = ww.min_month_temp(temp)
            max_temp = ww.max_month_temp(temp)
            flag=False
        plot_buffer = ww.plot_data_temperature(avg_temp, min_temp, max_temp, flag=flag)
        with open("plot.png", "wb") as f:
            f.write(plot_buffer.getvalue())
        # Отправка графика как фото из временного файла
        input_file = FSInputFile("plot.png")
        await message.answer_photo(
            photo=input_file,
            caption=ww.analyze_temp(avg_temp, min_temp, max_temp, flag)
        )
    except TypeError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except UnboundLocalError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except OpenMeteoRequestsError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    except ValueError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    


@router.message(Command('Precipitation_plot'))
async def city_name(message: Message, state: FSMContext):
    await state.set_state(Precipitation_city.city)
    await message.answer('Введите название города на английском')
    
@router.message(Precipitation_city.city)
async def first_date(message: Message, state: FSMContext):
    if re.match(r'^[a-zA-Z\s]+$', message.text):
        await state.update_data(city=message.text)
        await state.set_state(Precipitation_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Precipitation_city.city)
        await message.answer('Введите название города на английском')

@router.message(Precipitation_city.first_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(first_date=message.text)
        await state.set_state(Precipitation_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Precipitation_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')

@router.message(Precipitation_city.second_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(second_date=message.text)
        data = await state.get_data()
        await state.clear()
    else:
        await state.set_state(Precipitation_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    try:
        data['first_date'] = datetime.datetime.strptime(data['first_date'], "%Y-%m-%d")
        data['second_date'] = datetime.datetime.strptime(data['second_date'], "%Y-%m-%d")
        if data['first_date'] > data['second_date']:
            time = data['first_date']
            data['first_date'] = data['second_date']
            data['second_date'] = time
        
        temp = ww.data_precipitation(data['city'], datetime.datetime.strftime(data['first_date'], '%Y-%m-%d'), datetime.datetime.strftime(data['second_date'], '%Y-%m-%d'))
        await message.answer(f'Осадки в {data['city']} с {datetime.datetime.strftime(data['first_date'], '%Y-%m-%d')} по {datetime.datetime.strftime(data['second_date'], '%Y-%m-%d')}')
        if (data['second_date'] - data['first_date']).days < 2:
            avg_precipitation = temp
            min_precipitation = ww.min_day_precipitation(temp)
            max_precipitation = ww.max_day_precipitation(temp)
            flag = True
        elif (data['second_date'] - data['first_date']).days < 40:
            avg_precipitation = ww.avg_day_precipitation(temp)
            min_precipitation = ww.min_day_precipitation(temp)
            max_precipitation = ww.max_day_precipitation(temp)
            flag = False
        else:
            avg_precipitation = ww.avg_month_precipitation(temp)
            min_precipitation = ww.min_month_precipitation(temp)
            max_precipitation = ww.max_month_precipitation(temp)
            flag = False
        plot_buffer = ww.plot_data_precipitation(avg_precipitation, flag=flag)
        with open("plot.png", "wb") as f:
            f.write(plot_buffer.getvalue())
        input_file = FSInputFile("plot.png")
        await message.answer_photo(
            photo=input_file,
            caption=ww.analyze_precipitation(avg_precipitation, min_precipitation, max_precipitation, flag=flag)
        )    
    except TypeError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except UnboundLocalError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except OpenMeteoRequestsError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    except ValueError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    


@router.message(Command('Surface_pressure_plot'))
async def city_name(message: Message, state: FSMContext):
    await state.set_state(Surface_pressure_city.city)
    await message.answer('Введите название города на английском')
    
@router.message(Surface_pressure_city.city)
async def first_date(message: Message, state: FSMContext):
    if re.match(r'^[a-zA-Z\s]+$', message.text):
        await state.update_data(city=message.text)
        await state.set_state(Surface_pressure_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Surface_pressure_city.city)
        await message.answer('Введите название города на английском')

@router.message(Surface_pressure_city.first_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(first_date=message.text)
        await state.set_state(Surface_pressure_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    else:
        await state.set_state(Surface_pressure_city.first_date)
        await message.answer('Введите начальную дату в формате YYYY-mm-dd ')

@router.message(Surface_pressure_city.second_date) 
async def first_date(message: Message, state: FSMContext):
    if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
        await state.update_data(second_date=message.text)
        data = await state.get_data()
        await state.clear()
    else:
        await state.set_state(Surface_pressure_city.second_date)
        await message.answer('Введите конечную дату в формате YYYY-mm-dd ')
    
    try:    
        data['first_date'] = datetime.datetime.strptime(data['first_date'], "%Y-%m-%d")
        data['second_date'] = datetime.datetime.strptime(data['second_date'], "%Y-%m-%d")
        if data['first_date'] > data['second_date']:
            time = data['first_date']
            data['first_date'] = data['second_date']
            data['second_date'] = time
    
        temp = ww.data_surface_pressure(data['city'], datetime.datetime.strftime(data['first_date'], '%Y-%m-%d'), datetime.datetime.strftime(data['second_date'], '%Y-%m-%d'))
        await message.answer(f'Давление в {data["city"]} с {datetime.datetime.strftime(data["first_date"], "%Y-%m-%d")} по {datetime.datetime.strftime(data["second_date"], "%Y-%m-%d")}')
        if (data['second_date'] - data['first_date']).days < 2:
            avg_surface_pressure = temp
            min_surface_pressure = ww.min_day_surface_pressure(temp)
            max_surface_pressure = ww.max_day_surface_pressure(temp)
            flag = True
        elif (data['second_date'] - data['first_date']).days < 40:
            avg_surface_pressure = ww.avg_day_surface_pressure(temp)
            min_surface_pressure = ww.min_day_surface_pressure(temp)
            max_surface_pressure = ww.max_day_surface_pressure(temp)
            flag = False
        else:
            avg_surface_pressure = ww.avg_month_surface_pressure(temp)
            min_surface_pressure = ww.min_month_surface_pressure(temp)
            max_surface_pressure = ww.max_month_surface_pressure(temp)
            flag = False
        plot_buffer = ww.plot_data_surface_pressure(avg_surface_pressure, min_surface_pressure, max_surface_pressure, flag=flag)
        with open("plot.png", "wb") as f:
            f.write(plot_buffer.getvalue())
        input_file = FSInputFile("plot.png")
        await message.answer_photo(
            photo=input_file,
            caption=ww.analyze_surface_pressure(avg_surface_pressure, min_surface_pressure, max_surface_pressure, flag=flag)
        )
    except TypeError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except UnboundLocalError:
        await message.answer(f'Такого города не существует  "{data['city']}"')
    except OpenMeteoRequestsError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    except ValueError:
        await message.answer(f'Неправильный формат дат {data['first_date']} - {data['second_date']}')
    


    




    