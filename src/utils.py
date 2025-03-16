import plotly.express as px

def get_season_from_date(date):
    """
    Определяет сезон по заданной дате.
    """
    month = date.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def plot_time_series(df):
    """
    Строит интерактивный график температурных изменений с выделением скользящего среднего и аномалий.
    """
    fig = px.line(df, x="timestamp", y="temperature",
                  labels={"timestamp": "Дата", "temperature": "Температура (°C)"})
    fig.add_scatter(x=df['timestamp'], y=df['rolling_avg'], mode='lines', name='Скользящее среднее')

    anomaly_df = df[df['anomaly'] == True]
    if not anomaly_df.empty:
        fig.add_scatter(x=anomaly_df['timestamp'], y=anomaly_df['temperature'], mode='markers',
                        marker=dict(color='red', size=8), name='Аномалии')

    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            bgcolor="rgba(255,255,255,0.1)"
        ),
        legend_traceorder="reversed"
    )
    return fig

def plot_seasonal_stats(stats):
    """
    Визуализирует средние сезонные температуры с их разбросом (стандартным отклонением).
    """
    fig = px.bar(stats, x="season", y="season_mean", error_y="season_std",
                 labels={"season": "Сезон", "season_mean": "Средняя температура (°C)"})
    return fig
