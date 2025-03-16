# ClimaScope

Интерактивное приложение на **Streamlit** для анализа исторических и текущих температурных данных с использованием **OpenWeatherMap API**.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-EB6E4B?logo=openweathermap&logoColor=white)

## Описание

Приложение **ClimaScope** позволяет детально анализировать температурные данные, выявлять сезонные закономерности и аномалии, а также отслеживать текущую погоду при помощи OpenWeatherMap API.

## Основной функционал

### Анализ исторических данных
- Использование скользящего среднего для сглаживания колебаний температуры.
- Расчёт сезонной статистики (средняя температура и стандартное отклонение).
- Определение и визуализация температурных аномалий.

### Мониторинг текущей погоды
- Получение актуальной информации о температуре с помощью OpenWeatherMap API.
- Сравнение текущих данных с историческими показателями.

### Интерактивная визуализация
- Временные ряды с выделением аномальных значений температуры.
- Сезонные температурные профили с помощью интерактивных графиков Plotly.

## Запуск приложения

1. Склонируйте репозиторий:
```bash
git clone https://github.com/username/climascope.git
```

2. Перейдите в директорию проекта и установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
streamlit run app.py
```

## Получение ключа OpenWeatherMap API

- Зарегистрируйтесь и получите бесплатный ключ API на сайте [OpenWeatherMap](https://openweathermap.org/api).
- Введите полученный ключ в соответствующее поле интерфейса приложения.

## Развёртывание на Streamlit Cloud

- Создайте приложение на платформе [Streamlit Cloud](https://streamlit.io/cloud).
- Подключите GitHub-репозиторий с проектом и выполните развёртывание.

## Контакты

По всем вопросам и предложениям обращайтесь по электронной почте: **smmaximss@gmail.com**

## Лицензия

Проект распространяется под лицензией **MIT**.