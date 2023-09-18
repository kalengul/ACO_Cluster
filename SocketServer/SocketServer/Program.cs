using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Server
{
    static string Port = "8080";
    static string Arg0 = "127.0.0.1";
    static float[] SocketClusterTime = new float[1024]; // массив для хранения времени работы кластера для каждого подключенного клиента

    static void ServeClient(object arg)
    { // метод обслуживания клиента
        int clientSock = (int)arg; // преобразование аргумента в номер сокета клиента
        IPEndPoint clientEndPoint = (IPEndPoint)((Socket)clientSock).RemoteEndPoint; // получение IP-адреса и порта клиента
        Console.WriteLine("Client #{0} connected {1}:{2}", clientSock, clientEndPoint.Address, clientEndPoint.Port); // вывод сообщения о подключении клиента
        bool endServe = true; // флаг окончания обслуживания клиента
        while (endServe)
        { // цикл обслуживания клиента
            byte[] data = new byte[1024]; // буфер для приема данных от клиента
            while (!Encoding.ASCII.GetString(data).Contains("\r\n"))
            { // пока не получен полный пакет данных
                int bytesReceived = ((Socket)clientSock).Receive(data, data.Length, 0); // получение данных от клиента
                if (bytesReceived <= 0)
                { // если соединение разорвано
                    break;
                }
            }
            string dataString = Encoding.ASCII.GetString(data); // преобразование байтов в строку
            string typePacket = dataString.Substring(0, 5); // извлечение типа пакета
            string payload = dataString.Substring(5); // извлечение полезной нагрузки пакета
            if (typePacket == "WAYAG")
            { // если получен пакет с запросом на вычисление целевой функции
                string[] payloadSplit = payload.Split('*'); // разделение полезной нагрузки на тип кластера и путь
                int typeKlaster = int.Parse(payloadSplit[0]); // преобразование типа кластера в целое число
                float[] path = Array.ConvertAll(payloadSplit[1].Split('|'), float.Parse); // преобразование пути в массив чисел с плавающей точкой
                float OF = GetObjectivFunction(path, typeKlaster, SocketClusterTime[clientSock]); // вычисление целевой функции
                string stringNumbers = OF.ToString("F2") + "\r\n"; // преобразование результата в строку
                ((Socket)clientSock).Send(Encoding.ASCII.GetBytes(stringNumbers)); // отправка результата клиенту
            }
            else if (typePacket == "CTIME")
            { // если получен пакет с временем работы кластера
                SocketClusterTime[clientSock] = float.Parse(payload); // сохранение времени работы кластера для данного клиента
            }
            else if (typePacket == "CLOSE")
            { // если получен пакет с запросом на закрытие соединения
                endServe = false; // установка флага окончания обслуживания клиента
                ((Socket)clientSock).Close(); // закрытие соединения с клиентом
                Console.WriteLine("Client #{0} closed {1}:{2}", clientSock, clientEndPoint.Address, clientEndPoint.Port); // вывод сообщения о закрытии соединения с клиентом
            }
        }
    }

    static void RunServerCluster()
    { // метод запуска сервера кластера
        Console.WriteLine("Starting socket server cluster process"); // вывод сообщения о запуске сервера кластера
        Console.WriteLine("{0} {1}", Arg0, Port); // вывод IP-адреса и порта сервера кластера
        Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp); // создание сокета для прослушивания подключений
        listener.Bind(new IPEndPoint(IPAddress.Parse(Arg0), Port)); // связывание сокета с IP-адресом и портом сервера кластера
        listener.Listen(1024); // установка максимального числа подключений в очереди
        while (true)
        { // бесконечный цикл прослушивания подключений
            int clientSock = listener.Accept(); // принятие подключения от клиента
            Thread thread = new Thread(new ParameterizedThreadStart(ServeClient)); // создание потока для обслуживания клиента
            thread.Start(clientSock); // запуск потока для обслуживания клиента
        }
    }

    static void Main(string[] args)
    { // метод запуска программы
        RunServerCluster(); // запуск сервера кластера
    }
}