import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox


# Функция для загрузки данных из текстового файла
def load_data(file_path):
    # Чтение данных в DataFrame
    df = pd.read_csv(file_path, sep=' ', header=None)
    return df


# Функция для агрегации данных по выбранным столбцам
def aggregate_data(df, x_index, y_index):
    # Преобразование выбранных столбцов в числовой формат
    #print(df[y_index], df[x_index])

    # Удаление запятых и других символов из значений в выбранных столбцах
    for col in [x_index, y_index]:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = df[col].str.replace('(', '', regex=False)
        df[col] = df[col].str.replace(')', '', regex=False)
        df[col] = df[col].str.replace('[', '', regex=False)
        df[col] = df[col].str.replace(']', '', regex=False)

    #print(df[y_index], df[x_index])

    # Преобразование в числовой формат
    df[x_index] = pd.to_numeric(df[x_index], errors='coerce')
    df[y_index] = pd.to_numeric(df[y_index], errors='coerce')
    #print(df[y_index], df[x_index])

    # Удаление строк с y_index равным 9223372036854775807
    df = df.loc[df[y_index] < 8000000000000000000]

    # Агрегация данных
    aggregated_data = df.groupby(x_index)[y_index].agg(['mean', 'max', 'min']).reset_index()

    return aggregated_data


# Функция для обновления графиков
def update_graphs():
    file_path = file_combobox.get()
    try:
        x_index = int(x_index_entry.get())
        y_index = int(y_index_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Индексы должны быть целыми числами.")
        return

    df = load_data(file_path)
    if df is not None:
        aggregated_data = aggregate_data(df, x_index, y_index)
        print(aggregated_data)

        # Очистка предыдущих графиков
        for widget in graph_frame.winfo_children():
            widget.destroy()

        fig=plt.figure(figsize=(12, 6))

        # График среднего значения
        plt.subplot(1, 3, 1)
        plt.bar(aggregated_data[x_index], aggregated_data['mean'], color='blue')
        plt.title('Среднее значение')
        plt.xlabel('x_index')
        # включаем основную сетку
        plt.grid(which='major')
        # включаем дополнительную сетку
        plt.grid(which='minor', linestyle=':')
        # plt.ylabel('Среднее значение')

        # График максимального значения
        plt.subplot(1, 3, 2)
        plt.bar(aggregated_data[x_index], aggregated_data['max'], color='green')
        plt.title('Максимальное значение')
        plt.xlabel('x_index')
        # включаем основную сетку
        plt.grid(which='major')
        # включаем дополнительную сетку
        plt.grid(which='minor', linestyle=':')
        # plt.ylabel('Максимальное значение')

        # График минимального значения
        plt.subplot(1, 3, 3)
        plt.bar(aggregated_data[x_index], aggregated_data['min'], color='red')
        plt.title('Минимальное значение')
        plt.xlabel('x_index')
        # plt.ylabel('Минимальное значение')
        # включаем основную сетку
        plt.grid(which='major')
        # включаем дополнительную сетку
        plt.grid(which='minor', linestyle=':')

        plt.tight_layout()

        # Отображение графиков в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Список стандартных имен файлов
standard_files = [
    "log_file_RosaviationStart_mini3_0.txt",
    "log_file_RosaviationStart_mini3_0DF.txt",
    "Log_file_RosaviationStart_mini3_1.txt",
    "Log_file_RosaviationStart_mini3_2.txt",
    "Log_file_RosaviationStart_mini3_13.txt",
    "Log_file_RosaviationStart_mini3_14.txt",
    "Log_file_RosaviationStart_mini3_17.txt",
    "Log_file_RosaviationStart_mini3_18.txt",
    "Log_file_RosaviationStart_mini3_23.txt",
    "Log_file_RosaviationStart_mini3_24.txt"
]
if __name__ == '__main__':
    # Создание основного окна
    root = tk.Tk()
    root.title("Графики агрегации данных")

    # Поля выбора для имени файла и индексов
    ttk.Label(root, text="Выберите файл:").pack(pady=5)
    file_combobox = ttk.Combobox(root, values=standard_files, width=40)
    file_combobox.pack(pady=5)
    file_combobox.current(0)  # Устанавливаем первый элемент как выбранный

    ttk.Label(root, text="Индекс X:").pack(pady=5)
    x_index_entry = ttk.Entry(root)
    x_index_entry.pack(pady=5)

    ttk.Label(root, text="Индекс Y:").pack(pady=5)
    y_index_entry = ttk.Entry(root)
    y_index_entry.pack(pady=5)

    # Кнопка для обновления графиков
    update_button = ttk.Button(root, text="Построить графики", command=update_graphs)
    update_button.pack(pady=20)

    # Фрейм для графиков
    graph_frame = ttk.Frame(root)
    graph_frame.pack(pady=10)

    # Запуск основного цикла приложения
    root.mainloop()
