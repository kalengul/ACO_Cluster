using System;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;



class Server
{
    const int CLASTER_SIZE = 2048;
    private const double V = 0;// "Сильное";
    private static int Port = 8080;
    private static string Arg0 = "127.0.0.1";
    private static float[] SocketClusterTime = new float[CLASTER_SIZE]; // массив для хранения времени работы кластера для каждого подключенного клиента
    private static Stopwatch[] StartEnd = new Stopwatch[CLASTER_SIZE];
    private static Stopwatch[] GoOFFunction = new Stopwatch[CLASTER_SIZE];

    static void ServeClient(object arg)
    { // метод обслуживания клиента
        Socket clientEndPoint = (Socket) arg;
        bool endServe = true; // флаг окончания обслуживания клиента
        while (endServe)
        { // цикл обслуживания клиента
            byte[] data = new byte[1024]; // буфер для приема данных от клиента
            while (!Encoding.ASCII.GetString(data).Contains("\r\n"))
            { // пока не получен полный пакет данных
                int bytesReceived = clientEndPoint.Receive(data, data.Length, 0); // получение данных от клиента
                if (bytesReceived <= 0)
                { // если соединение разорвано
                    break;
                }
            }
            string dataString = Encoding.ASCII.GetString(data); // преобразование байтов в строку
            Console.WriteLine(dataString);
            string typePacket = dataString.Substring(0, 5); // извлечение типа пакета
            string payload = dataString.Substring(5); // извлечение полезной нагрузки пакета
            Console.WriteLine("|"+payload +"|");
            Console.WriteLine("|" + typePacket + "|");
            if (typePacket == "WAYAG")
            { // если получен пакет с запросом на вычисление целевой функции
                string[] payloadSplit = payload.Split('*'); // разделение полезной нагрузки на тип кластера и путь
                int nom = int.Parse(payloadSplit[0]);
                int typeKlaster = int.Parse(payloadSplit[1]); // преобразование типа кластера в целое число
                double[] path = Array.ConvertAll(payloadSplit[2].Split('|'), double.Parse); // преобразование пути в массив чисел с плавающей точкой
                double OF = GetObjectivFunction(path, typeKlaster, SocketClusterTime[nom]); // вычисление целевой функции
                string stringNumbers = OF.ToString("F32") + "\r\n"; // преобразование результата в строку
                clientEndPoint.Send(Encoding.ASCII.GetBytes(stringNumbers)); // отправка результата клиенту
            }
            else if (typePacket == "START")
            {// если получен пакет с запоминанием времени старта
                int nom = int.Parse(payload);
                StartEnd[nom].Reset(); // обнуляем значение времени
                StartEnd[nom].Start(); // запускаем замер заново
                Console.WriteLine("Время выполнения: " + StartEnd[nom].Elapsed);
            }
            else if (typePacket == "FINSH")
            {// если получен пакет с ожиданием отправки времени работы кластера
                int nom = int.Parse(payload);
                StartEnd[nom].Stop();
                Console.WriteLine("Время выполнения: " + StartEnd[nom].Elapsed);
            }
            else if (typePacket == "CTIME")
            { // если получен пакет с временем работы кластера
                string[] payloadSplit = payload.Split('*'); // разделение полезной нагрузки на время и номер клиента
                int nom = int.Parse(payloadSplit[0]);
                SocketClusterTime[nom] = (float)int.Parse(payloadSplit[1]); // сохранение времени работы кластера для данного клиента
            }
            else if (typePacket == "CLOSE")
            { // если получен пакет с запросом на закрытие соединения
                endServe = false; // установка флага окончания обслуживания клиента
                Console.WriteLine($"Client closed {clientEndPoint.RemoteEndPoint}"); // вывод сообщения о закрытии соединения с клиентом
                clientEndPoint.Close(); // закрытие соединения с клиентом
            }
        }
    }

    static void RunServerCluster()
    { // метод запуска сервера кластера
        try
        {
            string filePath = "Socket_parametr_C#.txt"; 

            // Чтение данных из файла
            string[] lines = File.ReadAllLines(filePath);

            // Парсинг данных
            int Port = int.Parse(lines[0]); // первая строка содержит значение Port
            string Arg0 = lines[1]; // вторая строка содержит значение IP-адреса

            // Использование загруженных данных
            Console.WriteLine("Port: " + Port);
            Console.WriteLine("Arg0: " + Arg0);
        }
        catch (Exception e)
        {
            Console.WriteLine("An error occurred: " + e.Message);
        }
        for (int i = 0; i < CLASTER_SIZE; i++)
        {
            StartEnd[i] = new Stopwatch();
            GoOFFunction[i] = new Stopwatch();
        }
        Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp); // создание сокета для прослушивания подключений
        listener.Bind(new IPEndPoint(IPAddress.Parse(Arg0), Port)); // связывание сокета с IP-адресом и портом сервера кластера
        // получаем конечную точку, с которой связан сокет
        Console.WriteLine(listener.LocalEndPoint); 
        listener.Listen(1024); // установка максимального числа подключений в очереди
        while (true)
        { // бесконечный цикл прослушивания подключений
            Socket clientSock = listener.Accept(); // принятие подключения от клиента
            Console.WriteLine($"Адрес подключенного клиента: {clientSock.RemoteEndPoint}");
            Thread thread = new Thread(new ParameterizedThreadStart(ServeClient)); // создание потока для обслуживания клиента
            thread.Start(clientSock); // запуск потока для обслуживания клиента
        }
    }

    static void Main(string[] args)
    { // метод запуска программы
        RunServerCluster(); // запуск сервера кластера
    }

    static public double GetObjectivFunction(double[] path, int TypeKlaster, float SocketClusterTime)
    {
        double OF = 0;
        switch (TypeKlaster)
        {
            case 1:  OF = Klaster1(path); break;
            case 2:  OF = Klaster2(path); break;
            case 2001:  OF = Klaster2o(path); break;
            case 2002:  OF = Klaster2no(path); break;
            case 2003:  OF = Klaster2so(path); break;
            case 2004:  OF = Klaster2nso(path); break;
            case 3:  OF = Klaster3(path); break;
            //        case 401:  OF = Bench1(path); break;
            //        case 4019:  OF = Bench1m(path); break;
            case 404:  OF = Bench4(path); break;
            //        case 4049:  OF = Bench4m(path); break;
            case 4040:  OF = Bench4x(path); break;
            case 4041:  OF = Bench4x1(path); break;
            case 4042:  OF = Bench4x2(path); break;
            case 40442:  OF = Bench4x3(path); break;
            case 40443:  OF = Bench4x4(path); break;
            case 4043:  OF = Bench4x22(path); break;
            case 4044:  OF = Bench4x222(path); break;
            case 4045:  OF = Bench4x2222(path); break;
            case 40451:  OF = Bench4xo2222(path); break;
            //        case 410:  OF = Bench10(path); break;
            //        case 4109:  OF = Bench10(path); break;
            case 980:  OF = BenchRozenbrok(path); break;
            case 981:  OF = BenchMultiFunction(path); break;
            case 982:  OF = BenchBirdFunction(path); break;
            case 983:  OF = BenchShevefeliaFunction(path); break;
            case 9800:  OF = BenchRozenbrokx10(path); break;
            case 9810:  OF = BenchMultiFunctionx10(path); break;
        }
        Console.WriteLine(OF + " " + String.Join(",", path) + " " + TypeKlaster);
        Console.WriteLine(SocketClusterTime);
        int milliseconds = (int)(SocketClusterTime); // преобразование в миллисекунды
        Thread.Sleep(milliseconds); // использование преобразованной переменной в Thread.Sleep
        return OF;
    }

    static int Klaster1(double[] path)
    {
        int OF = 0;
        if (path[0] > 3)
        {
            OF += 10;
        }
        if (path[2] == 0)
        {
            OF *= 5;
        }
        if (path[4] == 0)
        {
            OF += 3;
        }
        return OF;
    }

    static public double BenchRozenbrok(double[] path)
    {
        double alf = 100;
        double OF = -alf * (path[1] - path[0] * path[0]) * (path[1] - path[0] * path[0]) - (1 - path[0]) * (1 - path[0]);
        return OF;
    }

    static public double BenchMultiFunction(double[] path)
    {
        double OF = path[0] * Math.Sin(4 * Math.PI * path[0]) + path[1] * Math.Sin(4 * Math.PI * path[1]);
        return OF;
    }

    static public double BenchBirdFunction(double[] path)
    {
        double OF = -Math.Sin(path[0]) * Math.Exp((1 - Math.Cos(path[1])) * (1 - Math.Cos(path[1]))) - Math.Cos(path[1]) * Math.Exp((1 - Math.Sin(path[0])) * (1 - Math.Sin(path[0])) - (path[0] - path[1]) * (path[0] - path[1]));
        return OF;
    }

    static public double BenchShevefeliaFunction(double[] path)
    {
        double OF = -Math.Abs(path[0]) - Math.Abs(path[1]) - Math.Abs(path[0]) * Math.Abs(path[1]);
        return OF;
    }

    static public double BenchRozenbrokx10(double[] path)
    {
        double alf = 100;
        double x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5]);
        double x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11]);
        double OF = -alf * (x2 - x1 * x1) * (x2 - x1 * x1) - (1 - x1) * (1 - x1);
        return OF;
    }

    static public double BenchMultiFunctionx10(double[] path)
    {
        double x1 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5]);
        double x2 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11]);
        double OF = x1 * Math.Sin(4 * Math.PI * x1) + x2 * Math.Sin(4 * Math.PI * x2);
        return OF;
    }
    static public double Klaster2(double[] path)
    {
        double OF = 0;
        OF = OF + (path[0] - path[1] + 2 * path[2] + path[3] + 2 * path[4]);
        OF = OF + 0.5 * path[5] - 0.12 * path[6] - path[7] + 80 * path[8] + 0.00001 * path[9];
        if (path[10] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Klaster2o(double[] path)
    {
        double OF = 0;
        OF = OF + (path[4] - path[12] + 2 * path[2] + path[3] + 2 * path[5]);
        OF = OF + 0.5 * path[7] - 0.12 * path[10] - path[11] + 80 * path[0] + 0.00001 * path[6];
        if (path[1] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Klaster2no(double[] path)
    {
        double OF = 0;
        OF = OF + (path[8] - path[0] + 2 * path[10] + path[9] + 2 * path[7]);
        OF = OF + 0.5 * path[5] - 0.12 * path[2] - path[1] + 80 * path[12] + 0.00001 * path[6];
        if (path[11] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Klaster2so(double[] path)
    {
        double OF = 0;
        OF = OF + (path[5] - path[4] + 2 * path[7] + path[12] + 2 * path[3]);
        OF = OF + 0.5 * path[9] - 0.12 * path[6] - path[8] + 80 * path[10] + 0.00001 * path[11];
        if (path[1] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Klaster2nso(double[] path)
    {
        double OF = 0;
        OF = OF + (path[12 - 5] - path[12 - 4] + 2 * path[12 - 7] + path[12 - 12] + 2 * path[12 - 3]);
        OF = OF + 0.5 * path[12 - 9] - 0.12 * path[12 - 6] - path[12 - 8] + 80 * path[12 - 10] + 0.00001 * path[12 - 11];
        if (path[12 - 1] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Klaster3(double[] path)
    {
        double OF = 0;
        OF = OF + (Math.Pow(path[0] - 4, 2) + Math.Cos(path[1]) + Math.Cos(Math.Exp(path[2])) + Math.Pow(path[3] - 10, 2) + 2 * path[4]);
        OF = OF + 0.5 * path[5] - 0.12 * path[6] - path[7] + 80 * path[8] + 0.00001 * path[9];
        OF = OF * 15;
        if (path[10] == V)
        {
            OF = OF + 20;
        }
        return OF;
    }

    static public double Bench4(double[] path)
    {
        double a1 = Math.Pow(path[0], 2);
        double a2 = Math.Pow(path[1], 2);
        double a = 1 - (Math.Sqrt(a1 + a2) / Math.PI);
        double OF = Math.Pow(Math.Cos(path[0]) * Math.Cos(path[1]) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x(double[] path)
    {
        double p0 = path[0] + path[1];
        double p1 = path[2] + path[3];
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - (Math.Sqrt(a1 + a2) / Math.PI);
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x1(double[] path)
    {
        double p0 = path[0] * path[1];
        double p1 = path[2] * path[3];
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - (Math.Sqrt(a1 + a2) / Math.PI);
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x2(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2]);
        double p1 = path[3] * (path[4] + path[5]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x3(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2] + path[3]);
        double p1 = path[4] * (path[5] + path[6] + path[7]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x4(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2] + path[3] + path[4]);
        double p1 = path[5] * (path[6] + path[7] + path[8] + path[9]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x22(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2] + path[3]);
        double p1 = path[4] * (path[5] + path[6] + path[7]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x222(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2] + path[3] + path[4]);
        double p1 = path[5] * (path[6] + path[7] + path[8] + path[9]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4x2222(double[] path)
    {
        double p0 = path[0] * (path[1] + path[2] + path[3] + path[4] + path[5]);
        double p1 = path[6] * (path[7] + path[8] + path[9] + path[10] + path[11]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }

    static public double Bench4xo2222(double[] path)
    {
        double p0 = path[10] * (path[8] + path[6] + path[4] + path[2] + path[0]);
        double p1 = path[11] * (path[9] + path[7] + path[5] + path[3] + path[1]);
        double a1 = Math.Pow(p0, 2);
        double a2 = Math.Pow(p1, 2);
        double a = 1 - Math.Sqrt(a1 + a2) / Math.PI;
        double OF = Math.Pow(Math.Cos(p0) * Math.Cos(p1) * Math.Exp(Math.Abs(a)), 2);
        return OF;
    }
}