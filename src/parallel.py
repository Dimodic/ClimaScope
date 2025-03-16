from concurrent.futures import ProcessPoolExecutor
from src import analysis

def analyze_city(city, df):
    """
    Выполняет полный анализ температурных данных (сглаживание, статистика, аномалии) для одного города.
    """
    city_df = df[df['city'] == city].copy()
    city_df = analysis.compute_rolling_avg(city_df)
    stats = analysis.compute_season_stats(city_df)
    city_df = analysis.detect_anomalies(city_df)
    return city, city_df, stats

def parallel_analyze(df, cities):
    """
    Параллельно анализирует температурные данные сразу для нескольких городов.
    """
    results = {}
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(analyze_city, city, df): city for city in cities}
        for future in futures:
            city, city_df, stats = future.result()
            results[city] = {"data": city_df, "stats": stats}
    return results
