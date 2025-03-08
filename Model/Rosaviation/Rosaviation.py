import sys

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import GoTime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import warnings
import os
import tensorflow as tf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Input, LSTM, Dropout, Dense
from keras.callbacks import EarlyStopping

train=None
test=None
data=None
column_index = 2

def start_rosaviation():
    os.environ[
        'TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all messages, 1 = filter out INFO messages, 2 = filter out WARNING messages
    # Загрузка Excel файла с данными
    excel_file = '/Model/Rosaviation/file.xlsx'  # Укажите путь к вашему Excel файлу
    data = pd.read_excel(os.getcwd() + excel_file)  # Загружаем данные из Excel
    data['month'] = pd.to_datetime(data['month'], format='%d.%m.%Y')  # Преобразование столбца 'month' в формат даты
    data.set_index('month', inplace=True)  # Установка столбца 'month' в качестве индекса
    data = data.asfreq('MS')  # Установите 'MS' для начала месяца или 'M' для конца месяца
    return data

def create_train_and_test(data,column_index = 0, tren_size=0.8):
    # Получаем данные из указанного столбца
    data_column = data.iloc[:, column_index]
    data_diff = data_column

    # Если данные не стационарны, делаем разности
    while adfuller(data_diff)[1] > 0.05:  # Тест Дики-Фуллера
        print('Тест Дики-Фуллера не пройден',adfuller(data_diff)[1])
        data_diff = data_diff.diff().dropna()  # Делаем разности и убираем NaN
    data_column=data_diff
    # Разделение данных на обучающую и тестовую выборки
    train_size = int(len(data_column) * tren_size)
    train, test = data_column[:train_size], data_column[train_size:]
    return train, test

# Создание и обучение модели
def create_lstm_model(time_steps, n_features, p_dropout, kol_lstm_layers):
    inputs = Input(shape=(time_steps, n_features))
    lstm1 = LSTM(kol_lstm_layers[0], return_sequences=True)(inputs)
    dropout = Dropout(p_dropout)(lstm1)
    output = Dense(n_features)(dropout)  # Выход с двумя нейронами для двух признаков
    model = Model(inputs=inputs, outputs=output)
    model.compile(optimizer='adam', loss='mse')
    return model

def prepare_data(series, n_steps):
    X, y = [], []
    for i in range(len(series) - n_steps):
        X.append(series[i:i + n_steps])
        y.append(series[i + n_steps])
    return np.array(X), np.array(y)

def forecast_components_lstm(train, test, seasonal_period, periods_predict):
    try:
        n_features=1
        p_dropout=0.2
        kol_lstm_layers=[128]
        # Декомпозиция временного ряда на компоненты
        stl = STL(train)
        result = stl.fit()

        trend = result.trend.dropna()
        seasonal = result.seasonal.dropna()
        resid = result.resid.dropna()

        # Функция для прогнозирования компоненты с использованием LSTM
        def forecast_component(component):
            scaler = MinMaxScaler()
            component_scaled = scaler.fit_transform(component.values.reshape(-1, 1))

            # Подготовка данных для обучения моделей
            time_steps = seasonal_period  # количество временных шагов
            X, y = prepare_data(component_scaled, time_steps)
            # Изменение формы для LSTM [samples, time steps, features]
            X = X.reshape((X.shape[0], X.shape[1], n_features))
            # Создание и обучение модели
            model = create_lstm_model(time_steps, n_features, p_dropout, kol_lstm_layers)
            model.fit(X, y, epochs=200, verbose=0)

            # Прогнозирование
            last_batch = component_scaled[-time_steps:].reshape((1, time_steps, 1))
            forecast = []

            for _ in range(len(test) + periods_predict):
                next_pred = model.predict(last_batch)[0][0]
                forecast.append(next_pred)
                last_batch = np.append(last_batch[:, 1:, :], [[next_pred]], axis=1)

            forecast_inverse = scaler.inverse_transform(np.array(forecast).reshape(-1, 1)).flatten()
            return forecast_inverse[:len(test)], forecast_inverse[len(test):]

        # Прогнозируем каждую компоненту
        trend_forecast, trend_forecast_next = forecast_component(trend)
        seasonal_forecast, seasonal_forecast_next = forecast_component(seasonal)
        resid_forecast, resid_forecast_next = forecast_component(resid)

        # Суммируем прогнозы по компонентам
        final_forecast = trend_forecast + seasonal_forecast + resid_forecast
        final_forecast_next = trend_forecast_next + seasonal_forecast_next + resid_forecast_next

        # Вычисляем метрики точности
        mae = mean_absolute_error(test, final_forecast)
        mse = mean_squared_error(test, final_forecast)
        rmse = np.sqrt(mse)

        print(f'MAE: {mae}')
        print(f'MSE: {mse}')
        print(f'RMSE: {rmse}')

        return final_forecast_next, mae, mse, rmse

    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        return None, None, None, None

def forecast_components(train, test, seasonal_period,periods_predict,order_trend,seasonal_order_trend,order_seasonal,seasonal_order_seasonal,order_resid,seasonal_order_resid):
    try:
        # Декомпозиция временного ряда на компоненты
        #result = seasonal_decompose(train, period=seasonal_period)
        stl = STL(train)#, period=seasonal_period)
        result = stl.fit()

        trend = result.trend
        seasonal = result.seasonal
        resid = result.resid
        itog=trend+seasonal+resid
        #print('train,itog')
        #print(train, itog)

        # Прогнозирование компонентов с помощью SARIMAX
        def forecast_component(component,periods_predict,order,seasonal_order):
            model = SARIMAX(component.dropna(), order=order,seasonal_order=seasonal_order)  # Параметры можно настроить
            results = model.fit(disp=False)
            forecast = results.get_forecast(steps=len(test))
            forecast_next = results.get_forecast(steps=len(test)+periods_predict)
            return forecast.predicted_mean,forecast_next.predicted_mean

        # Прогнозируем каждую компоненту
        trend_forecast,trend_forecast_next = forecast_component(trend,periods_predict,order_trend,seasonal_order_trend)
        seasonal_forecast, seasonal_forecast_next = forecast_component(seasonal,periods_predict,order_seasonal,seasonal_order_seasonal)
        resid_forecast, resid_forecast_next = forecast_component(resid,periods_predict,order_resid,seasonal_order_resid)

        # Суммируем прогнозы по компонентам
        final_forecast = trend_forecast + seasonal_forecast + resid_forecast
        final_forecast_next=trend_forecast_next + seasonal_forecast_next + resid_forecast_next
        #print('test, final_forecast')
        #print(test, final_forecast)

        # Вычисляем метрики точности
        mae = mean_absolute_error(test, final_forecast)
        mse = mean_squared_error(test, final_forecast)
        rmse = np.sqrt(mse)

        #print(f'MAE: {mae}')
        #print(f'MSE: {mse}')
        #print(f'RMSE: {rmse}')

        return final_forecast_next, mae, mse, rmse

    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        return None, None, None, None

def forecast_series(train,test, steps, order, seasonal_order):
    try:
        # Создание и обучение модели SARIMAX
        model = SARIMAX(endog=train, order=order, seasonal_order=seasonal_order)
        results = model.fit(disp=False)
        conf_int={}

        # Получение прогноза для тестирования модели
        forecast = results.get_forecast(steps=len(test))
        predicted_mean = forecast.predicted_mean

        # Вычисление метрик точности
        mae = mean_absolute_error(test, predicted_mean)
        mse = mean_squared_error(test, predicted_mean)
        rmse = np.sqrt(mse)

        #print(f'MAE: {mae}')
        #print(f'MSE: {mse}')
        #print(f'RMSE: {rmse}')
        # Получение прогноза
        forecast = results.get_forecast(steps=len(test)+steps)
        predicted_mean = forecast.predicted_mean

        # Возвращаем предсказанные значения и доверительные интервалы
        return predicted_mean, conf_int,mae,mse,rmse

    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        return None, None

def forecast_SARIMAX(train,test,periods_predict,order, seasonal_order):
    forecast_results = {}  # Прогнозирование
    try:
        last_value = train.iloc[-1]  # Сохраняем последнее значение для восстановления
        # Прогнозируем разности
        forecast_diff, conf_int, mae, mse, rmse = forecast_series(train,test, periods_predict, order, seasonal_order)  # Распаковываем возвращаемые значения

        # Восстанавливаем предсказанные значения
        forecast_values = last_value + forecast_diff.cumsum()  # Суммируем разности и добавляем к последнему значению
        # Сохраняем результаты в словаре
        forecast_results[0] = forecast_values

    except Exception as e:
        print(f"Ошибка при прогнозировании: {e}")
        return None, None, None, None,None
    # Преобразуем результаты в DataFrame
    forecast_df = pd.DataFrame(forecast_results)

    # Создаем индекс для прогноза (84 месяца)
    if forecast_df.empty:
        print("Нет данных для создания прогноза.")
    else:
        forecast_index = pd.date_range(start=data.index[-1] + pd.DateOffset(months=1), periods=len(forecast_df),
                                       freq='ME')
        forecast_df.index = forecast_index[:len(forecast_df)]
        return forecast_df, conf_int, mae, mse, rmse

def goSARIMAX(path):
    Time1=GoTime.now()
    sdvig = 0
    offset = sdvig + 1
    p = path[offset] + path[offset + 1] + path[offset + 2]  # порядок авторегрессии
    d = path[offset + 3]  # порядок интегрирования
    q_offset = offset + 3 + 1
    q = path[q_offset] + path[q_offset + 1] + path[q_offset + 2]  # порядок скользящей средней
    P_offset = q_offset + 3
    P = path[P_offset] + path[P_offset + 1] + path[P_offset + 2]  # порядок сезонной авторегрессии
    D = path[P_offset + 3]  # порядок сезонного интегрирования
    Q_offset = P_offset + 3 + 1
    Q = path[Q_offset] + path[Q_offset + 1] + path[Q_offset + 1 + 1]  # порядок сезонной скользящей средней
    s = 12  # период сезонности
    periods_predict = 40
    order = (p,d,q)
    seasonal_order = (P,D,Q,s)
    #order = (1,0,1)
    #seasonal_order = (1,0,1,s)
    #print(periods_predict,order, seasonal_order)
    forecast_df, conf_int, mae, mse, rmse = forecast_SARIMAX(train, test,periods_predict,order, seasonal_order)
    if mae==None:
        mae=sys.maxsize
        mse = sys.maxsize
        rmse = sys.maxsize
    # Сохранение результатов в список
    res = [mae, mse, rmse]
    original_stdout = sys.stdout  # Save a reference to the original standard output
    with open(os.getcwd() + '/Log_file.txt', 'a') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print(GoTime.now(),GoTime.now()-Time1,periods_predict,order, seasonal_order,res,path)
    sys.stdout = original_stdout  # Reset the standard output to its original value
    #print(GoTime.now(),GoTime.now()-Time1,periods_predict,order, seasonal_order,res)
    return res

def goSARIMAX_component(path):
    Time1=GoTime.now()
    # Начальное смещение
    sdvig = 0
    # Параметры модели для первого набора
    p = path[sdvig + 1] + path[sdvig + 2] + path[sdvig + 3]  # порядок авторегрессии
    d = path[sdvig + 4]  # порядок интегрирования
    q = (path[sdvig + 5] + path[sdvig + 6] + path[sdvig + 7])  # порядок скользящей средней
    P = (path[sdvig + 8] + path[sdvig + 9] + path[sdvig + 10])  # порядок сезонной авторегрессии
    D = path[sdvig + 11]  # порядок сезонного интегрирования
    Q = (path[sdvig + 12] + path[sdvig + 13] + path[sdvig + 14])  # порядок сезонной скользящей средней

    # Обновляем смещение для следующего набора параметров
    sdvig += 14
    # Параметры модели для второго набора
    p1 = path[sdvig + 1] + path[sdvig + 2] + path[sdvig + 3]  # порядок авторегрессии
    d1 = path[sdvig + 4]  # порядок интегрирования
    q1 = (path[sdvig + 5] + path[sdvig + 6] + path[sdvig + 7])  # порядок скользящей средней
    P1 = (path[sdvig + 8] + path[sdvig + 9] + path[sdvig + 10])  # порядок сезонной авторегрессии
    D1 = path[sdvig + 11]  # порядок сезонного интегрирования
    Q1 = (path[sdvig + 12] + path[sdvig + 13] + path[sdvig + 14])  # порядок сезонной скользящей средней

    # Обновляем смещение для третьего набора параметров
    sdvig += 14
    # Параметры модели для третьего набора
    p2 = path[sdvig + 1] + path[sdvig + 2] + path[sdvig + 3]  # порядок авторегрессии
    d2 = path[sdvig + 4]  # порядок интегрирования
    q2 = (path[sdvig + 5] + path[sdvig + 6] + path[sdvig + 7])  # порядок скользящей средней
    P2 = (path[sdvig + 8] + path[sdvig + 9] + path[sdvig + 10])  # порядок сезонной авторегрессии
    D2 = path[sdvig + 11]  # порядок сезонного интегрирования
    Q2 = (path[sdvig + 12] + path[sdvig + 13] + path[sdvig + 14])  # порядок сезонной скользящей средней

    # Параметры сезонности и прогнозирования
    s = 12  # период сезонности
    periods_predict = 40

    # Формирование кортежей для параметров модели
    order_trend = (p, d, q)
    seasonal_order_trend = (P, D, Q, s)
    order_seasonal = (p1, d1, q1)
    seasonal_order_seasonal = (P1, D1, Q1, s)
    order_resid = (p2, d2, q2)
    seasonal_order_resid = (P2, D2, Q2, s)



    # Прогнозирование компонентов с использованием заданных параметров
    forecast_df, mae, mse, rmse = forecast_components(
        train, test, s, periods_predict,
        order_trend, seasonal_order_trend,
        order_seasonal, seasonal_order_seasonal,
        order_resid, seasonal_order_resid
    )

    # Проверка на наличие ошибок в метриках и установка значений по умолчанию
    if mae is None:
        mae = sys.maxsize
        mse = sys.maxsize
        rmse = sys.maxsize

    # Сохранение результатов в список
    res = [mae, mse, rmse]
    # Вывод информации о времени выполнения и параметрах модели
    original_stdout = sys.stdout  # Save a reference to the original standard output
    with open(os.getcwd() + '/Log_file.txt', 'a') as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print(GoTime.now() - Time1, order_trend, seasonal_order_trend,
          order_seasonal, seasonal_order_seasonal, order_resid, seasonal_order_resid,res, path)
    sys.stdout = original_stdout  # Reset the standard output to its original value
    #print(GoTime.now() - Time1, order_trend, seasonal_order_trend,
    #      order_seasonal, seasonal_order_seasonal, order_resid, seasonal_order_resid,res)
    return res


def get_sarima_probabilities(data_diff, max_p=8, max_q=8, max_P=2, max_Q=2, seasonal_period=12):

    if data_diff.empty:
        raise ValueError("Входной временной ряд пуст.")

    n = len(data_diff)
    max_lags = min(n // 2 - 1, max_p + max_q)

    # Получаем ACF и PACF
    acf_values = acf(data_diff, nlags=max_lags)
    pacf_values = pacf(data_diff, nlags=max_lags)

    # Вычисляем вероятности для p и q
    p_probs = np.abs(pacf_values[:max_p])
    q_probs = np.abs(acf_values[:max_q])
    p_probs /= p_probs.sum() if p_probs.sum() > 0 else 1
    q_probs /= q_probs.sum() if q_probs.sum() > 0 else 1

    # Вычисляем вероятности для P и Q
    seasonal_lags = min(n // seasonal_period - 1, max_P * seasonal_period)
    seasonal_acf = acf(data_diff, nlags=seasonal_lags)[seasonal_period::seasonal_period][:max_P]
    seasonal_pacf = pacf(data_diff, nlags=seasonal_lags)[seasonal_period::seasonal_period][:max_P]

    P_probs = np.abs(seasonal_pacf)
    Q_probs = np.abs(seasonal_acf)
    P_probs /= P_probs.sum() if P_probs.sum() > 0 else 1
    Q_probs /= Q_probs.sum() if Q_probs.sum() > 0 else 1

    #print(p_probs, q_probs)
    return p_probs, q_probs


def add_pq_to_start_pheromon(print_information=False, p=None, d=None, q=None, P=None, D=None, Q=None,
                             parametric_graph=None, start_sdvig = 1,paramtr_p=3, paramtr_d=1, paramtr_q=3,paramtr_P=3, paramtr_D=1, paramtr_Q=3):
    sdvig = start_sdvig

    def process_graph(param_array, param_count):
        nonlocal sdvig
        if len(param_array) > 0:
            while True:
                path = []
                value_itog = sum(parametric_graph[i + sdvig].node[nom_node_path[i]].val for i in range(param_count))
                path = [parametric_graph[i + sdvig].node[nom_node_path[i]].val for i in range(param_count)]

                for i in range(param_count):
                    parametric_graph[i + sdvig].node[nom_node_path[i]].StartKolPheromon += param_array[int(value_itog)]
                    if print_information:
                        print(i, nom_node_path[i], param_array[int(value_itog)],
                              parametric_graph[i + sdvig].node[nom_node_path[i]].StartKolPheromon)

                if print_information:
                    if value_itog < len(param_array):
                        print(
                            f"Path: {path}, Objective Function Value: {value_itog}, node[nom_p]: {param_array[int(value_itog)]}")
                    else:
                        print(f"Path: {path}, Objective Function Value: {value_itog}, Index out of bounds for p")

                # Увеличиваем индекс для следующей комбинации
                nom_par = 0
                while nom_par < param_count:
                    nom_node_path[nom_par] += 1
                    if nom_node_path[nom_par] < len(parametric_graph[nom_par + sdvig].node):
                        break
                    else:
                        nom_node_path[nom_par] = 0
                        nom_par += 1
                if nom_par == param_count:
                    break
        sdvig += param_count

    nom_node_path = [0] * (paramtr_p + paramtr_d + paramtr_q+paramtr_P + paramtr_D + paramtr_Q)

    process_graph(p, paramtr_p)
    process_graph(d, paramtr_d)
    process_graph(q, paramtr_q)
    process_graph(P, paramtr_P)
    process_graph(D, paramtr_D)
    process_graph(Q, paramtr_Q)

    return 0

def goPDQ_at_ACF(data_diff,lags=40,seasonal_period=12):
    print('data_diff')
    print(data_diff)
    # Определите максимальное количество лагов в зависимости от длины выборки
    max_lags = min(lags, len(data_diff) // 2)

    # Вычисление ACF и PACF
    lag_acf = acf(data_diff, nlags=max_lags)
    lag_pacf = pacf(data_diff, nlags=max_lags)
    print('lag_pacf')
    print(lag_pacf)
    # Определение частоты значений p от 0 до 6
    p_values_count = {i: 0 for i in range(7)}  # Словарь для подсчета частоты p от 0 до 6

    # Подсчет частоты p
    for i in range(len(lag_pacf)):
        if lag_pacf[i] > 0.2 and i <= 6:
            p_values_count[i] += 1

    # Вычисление вероятностей для p от 0 до 6
    total_p_values = sum(p_values_count.values())
    p_probabilities = {k: v / total_p_values if total_p_values > 0 else 0 for k, v in p_values_count.items()}

    # Вывод вероятностей
    print("Вероятности для значений p от 0 до 6:")
    for k, v in p_probabilities.items():
        print(f"p = {k}: вероятность = {v:.2f}")

    # Теперь определяем Q
    q_values_count = {i: 0 for i in range(7)}  # Словарь для подсчета частоты Q от 0 до 6

    # Подсчет частоты Q
    for i in range(len(lag_acf)):
        if lag_acf[i] > 0.2 and i <= 6:
            q_values_count[i] += 1

    # Вычисление вероятностей для Q от 0 до 6
    total_q_values = sum(q_values_count.values())
    q_probabilities = {k: v / total_q_values if total_q_values > 0 else 0 for k, v in q_values_count.items()}

    # Вывод вероятностей для Q
    print("Вероятности для значений Q от 0 до 6:")
    for k, v in q_probabilities.items():
        print(f"q = {k}: вероятность = {v:.2f}")

    # Для сезонных параметров P, D, Q можно использовать аналогичный подход.

    # Вычисление сезонного ACF и PACF
    seasonal_max_lags = min(seasonal_period, len(data_diff) // 2)
    seasonal_acf = acf(data_diff, nlags=seasonal_max_lags)
    seasonal_pacf = pacf(data_diff, nlags=seasonal_max_lags)

    P_values_count = {i: 0 for i in range(7)}  # Словарь для подсчета частоты P от 0 до 6

    # Подсчет частоты P
    for i in range(len(seasonal_pacf)):
        if seasonal_pacf[i] > 0.2 and i <= 6:
            P_values_count[i] += 1

    # Вычисление вероятностей для P от 0 до 6
    total_P_values = sum(P_values_count.values())
    P_probabilities = {k: v / total_P_values if total_P_values > 0 else 0 for k, v in P_values_count.items()}

    # Вывод вероятностей для P
    print("Вероятности для значений P от 0 до 6:")
    for k, v in P_probabilities.items():
        print(f"P = {k}: вероятность = {v:.2f}")

    # Теперь определяем Q
    Q_values_count = {i: 0 for i in range(7)}  # Словарь для подсчета частоты Q от 0 до 6

    # Подсчет частоты Q
    for i in range(len(seasonal_acf)):
        if seasonal_acf[i] > 0.2 and i <= 6:
            Q_values_count[i] += 1

    # Вычисление вероятностей для Q от 0 до 6
    total_Q_values = sum(Q_values_count.values())
    Q_probabilities = {k: v / total_Q_values if total_Q_values > 0 else 0 for k, v in Q_values_count.items()}

    # Вывод вероятностей для Q
    print("Вероятности для значений Q от 0 до 6:")
    for k, v in Q_probabilities.items():
        print(f"Q = {k}: вероятность = {v:.2f}")

def load_data_rosaviation_excel(column_index,tren_size):
    global train
    global test
    global data
    warnings.filterwarnings("ignore", category=UserWarning)
    data = start_rosaviation()
    train, test = create_train_and_test(data, column_index=column_index,tren_size=tren_size)
    print(train, test)
    #test_auto_arima(train)
    p,q=get_sarima_probabilities(train)

    #forecast_df, mae, mse, rmse = forecast_components(train, test, seasonal_period,periods_predict,order_trend,seasonal_order_trend,order_seasonal,seasonal_order_seasonal,order_resid,seasonal_order_resid)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #forecast_df, conf_int, mae, mse, rmse = forecast_SARIMAX(train,test,periods_predict,order_trend, seasonal_order_trend)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #forecast_df, mae, mse, rmse = forecast_components_lstm(train, test, seasonal_period, periods_predict)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return p,q

def test_elemet():
    # Создание DataFrame из ваших данных
    data = {
        'date': ['2020-06-01', '2020-07-01', '2020-08-01', '2020-09-01', '2020-10-01', '2020-11-01'],
        'value': [0.811966, 0.811129, 0.810323, 0.722869, 0.646563, 0.585572]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Проверка на стационарность (тест Дики-Фуллера)
    def check_stationarity(series):
        result = adfuller(series)
        return result[1] <= 0.05  # p-value <= 0.05 указывает на стационарность

    is_stationary = check_stationarity(df['value'])
    print(f"Ряд стационарен: {is_stationary}")

    # Если ряд не стационарен, применяем дифференцирование
    if not is_stationary:
        df['diff'] = df['value'].diff().dropna()
        is_stationary_after_diff = check_stationarity(df['diff'].dropna())
        print(f"Ряд стал стационарным после дифференцирования: {is_stationary_after_diff}")

    # Построение графиков ACF и PACF
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.title('ACF')
    pd.plotting.autocorrelation_plot(df['value'])
    plt.subplot(122)
    plt.title('PACF')
    pd.plotting.autocorrelation_plot(df['value'].diff().dropna())
    plt.show()

    # Проверка Ljung-Box для остатков
    if 'diff' in df.columns:
        lb_test = acorr_ljungbox(df['diff'].dropna(), lags=1)
        p_value = lb_test['lb_pvalue'].iloc[0]
        print(f"Ljung-Box p-value: {p_value}")

def test_auto_arima(df):

    # Генерация временного ряда
    #np.random.seed(42)
    #data = np.random.randn(100) + np.linspace(0, 10, 100)

    # Преобразование в DataFrame
    #df = pd.DataFrame(data, columns=['value'])

    # Автоматический подбор модели ARIMA
    model = auto_arima(df, seasonal=False, stepwise=True, trace=True)

    # Вывод результатов
    print(model.summary())

    # Прогнозирование
    n_periods = 12
    forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)
    print('forecast, conf_int about auto_arima')
    print(forecast, conf_int)



#if __name__ == '__main__':
    #test_auto_arima()

