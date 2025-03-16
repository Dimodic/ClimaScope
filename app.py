import time
from datetime import datetime

import pandas as pd
import streamlit as st

from src import analysis, api, generate_data, parallel, utils

# --- Настройка приложения ---
st.set_page_config(
    page_title="ClimaScope",
    page_icon="src/assets/favicon.ico"
)
st.title("ClimaScope: анализ температуры")


# --- Боковая панель: Работа с файлом ---
st.sidebar.header("Конфигурация")
uploaded_file = st.sidebar.file_uploader("CSV файл", type="csv")
default_filepath = "src/assets/temperature_data.csv"

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    col_info, col_gen = st.sidebar.columns([4, 1])

    with col_info:
        status_text = st.empty()
        status_text.info("Файл по умолчанию")

    with col_gen:
        gen_clicked = st.button("↻", key="gen_file", help="Сгенерировать файл")

    if gen_clicked:
        df = generate_data.generate_temperature_data(default_filepath)
        status_text.success("Файл перегенерирован")
    else:
        df = generate_data.generate_temperature_data(default_filepath)

df['timestamp'] = pd.to_datetime(df['timestamp'])


# --- Боковая панель: Выбор города ---
cities = df['city'].unique().tolist()
selected_city = st.sidebar.selectbox(
    "Город",
    options=cities,
    index=None,
    placeholder="Выберите город"
)


# --- Боковая панель: Работа с API ключом ---
st.sidebar.subheader("API ключ OpenWeatherMap")
if "api_key_input" not in st.session_state:
    st.session_state["api_key_input"] = ""

api_key_input = st.sidebar.text_input(
    "Введите API ключ",
    value=st.session_state["api_key_input"],
    type="password"
)

col_confirm, col_delete = st.sidebar.columns([5, 1])

if col_confirm.button("Подтвердить API ключ"):
    st.session_state["api_key"] = api_key_input
    st.session_state["api_key_input"] = api_key_input
    st.sidebar.success("API ключ сохранён")

if st.session_state.get("api_key"):
    if col_delete.button("x"):
        st.session_state.pop("api_key", None)
        st.session_state["api_key_input"] = ""
        st.sidebar.info("API ключ удалён")


# --- Приветственное сообщение ---
if not selected_city:
    st.markdown("""
        ## Добро пожаловать в ClimaScope!

        **ClimaScope** — это удобное интерактивное приложение для анализа температурных данных, 
        отслеживания изменений погоды и мониторинга актуальной информации о погодных условиях в выбранном городе.
    """)
    st.info("Для продолжения работы выберите город в меню боковой панели")
    st.stop()


# --- Анализ данных: вычисление скользящего среднего, статистики и аномалий ---
df = analysis.compute_rolling_avg(df, window=30)
season_stats = analysis.compute_season_stats(df)
df = analysis.detect_anomalies(df)

city_df = df[df['city'] == selected_city].copy()
city_stats = analysis.compute_season_stats(city_df)
city_df = analysis.detect_anomalies(city_df)

st.header(f"Исторический анализ для города {selected_city}")


# --- Описательная статистика ---
st.subheader("Описательная статистика")
st.write(city_df.describe())


# --- Визуализация временного ряда ---
st.subheader("Временной ряд температур")
fig_ts = utils.plot_time_series(city_df)
st.plotly_chart(fig_ts)


# --- Сезонные профили ---
st.subheader("Сезонные профили")
fig_season = utils.plot_seasonal_stats(city_stats)
st.plotly_chart(fig_season)


# --- Параллельный анализ ---
st.subheader("Параллельный анализ для всех городов")

if st.button("Запустить параллельный анализ"):
    with st.spinner("Выполняется параллельный анализ..."):
        parallel_results = parallel.parallel_analyze(df, cities)

    st.success("Параллельный анализ завершён")
    st.write(f"Данные для города {selected_city}:")
    st.write(parallel_results[selected_city]["stats"])


# --- Мониторинг текущей температуры ---
st.subheader("Мониторинг текущей температуры")
api_key = st.session_state.get("api_key")

if api_key:
    method = st.radio(
        "Выберите метод запроса к API",
        options=["sync", "async"],
        horizontal=True
    )

    start_time = time.time()
    with st.spinner("Получение текущей температуры..."):
        result = api.get_current_temperature(selected_city, api_key, method=method)
    elapsed_time = time.time() - start_time

    st.info(f"Метод **{method}** выполнен за {elapsed_time:.2f} секунд")

    if "error" in result:
        st.error(f"Ошибка при запросе: {result['error']}")
    else:
        current_temp = result["temperature"]
        st.metric(label="Текущая температура", value=f"{current_temp} °C")

        current_date = datetime.now()
        current_season = utils.get_season_from_date(current_date)
        st.write(f"Текущий сезон: **{current_season}**")

        season_data = city_df[city_df['season'] == current_season]

        if not season_data.empty:
            season_mean = season_data['temperature'].mean()
            season_std = season_data['temperature'].std()
            lower_bound = season_mean - 2 * season_std
            upper_bound = season_mean + 2 * season_std

            st.markdown(f"Исторический диапазон для сезона {lower_bound:.1f} °C – {upper_bound:.1f} °C")

            if current_temp < lower_bound or current_temp > upper_bound:
                st.error("Текущая температура **аномальная** для данного сезона!")
            else:
                st.success("Текущая температура **в норме** для данного сезона")
        else:
            st.warning("Нет данных для текущего сезона, невозможно провести сравнение")
else:
    st.info("Для отображения данных о текущей температуре введите API ключ в меню боковой панели")
