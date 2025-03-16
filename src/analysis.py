def compute_rolling_avg(df, window = 30):
    """
    Сглаживает температурные данные с помощью скользящего среднего.
    """
    df = df.sort_values(by='timestamp')
    df['rolling_avg'] = df['temperature'].rolling(window=window, min_periods=1).mean()
    return df

def compute_season_stats(df):
    """
    Рассчитывает среднюю температуру и разброс для каждого сезона.
    """
    stats = df.groupby('season')['temperature'].agg(['mean', 'std']).reset_index()
    stats = stats.rename(columns={'mean': 'season_mean', 'std': 'season_std'})
    return stats

def detect_anomalies(df):
    """
    Определяет температурные аномалии, выходящие за пределы нормального сезонного диапазона.
    """
    def compute_anomalies(group):
        season_mean = group['temperature'].mean()
        season_std = group['temperature'].std()
        lower_bound = season_mean - 2 * season_std
        upper_bound = season_mean + 2 * season_std
        group['anomaly'] = (group['temperature'] < lower_bound) | (group['temperature'] > upper_bound)
        return group

    # Применяем вычисления для каждой группы по сезону
    df = df.groupby('season', group_keys=False).apply(compute_anomalies)
    return df
