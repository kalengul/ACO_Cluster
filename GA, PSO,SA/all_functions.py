from math import sqrt, exp, cos, sin, pi, e, fabs
# https://ru.wikipedia.org/wiki/Тестовые_функции_для_оптимизации

KolIterStatistics = 100

def Rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def BenchRozenbrokx10(x,y):
    alf = 100
    x1 = x
    x2 = y
    OF = alf * (x2 - x1 * x1) * (x2 - x1 * x1) + (1 - x1) * (1 - x1)
    return OF

def Rastrigin(x, y):
    return 20 + x ** 2 + y ** 2 - 10 * (cos(2 * pi * x) + cos(2 * pi * y))

def BenchRastriginFunctionx10(x, y):
    x1 = x
    x2 = y
    OF = 20 - (10 * cos(2 * pi * x1) - x1 * x1) - (10 * cos(2 * pi * x2) - x2 * x2)
    return OF


def Ackley(x, y):
    return -20*exp(-0.2*sqrt(0.5*(x**2+y**2)))-exp(0.5*(cos(2*pi*x)+cos(2*pi*y)))+e+20

def Sphere(x, y):
    return x**2 + y**2

def Himmelblau(x, y):
    return (x**2+y-11)**2 + (x+y**2-7)**2

def Holder(x, y):
    return -1 * abs(sin(x)*cos(y)*exp(abs(1 - (sqrt(x**2 + y**2))/pi) ))

def BenchMultiFunctionx10(x, y):
    x1 = x
    x2 = y
    OF = x1 * sin(4 * pi * x1) + x2 * sin(4 * pi * x2)
    return -OF


def BenchShafferaFunctionx10(x, y):
    x1 = x
    x2 = y
    OF = 1 / 2 - (sin(sqrt(x1 * x1 + x2 * x2)) * sin(sqrt(x1 * x1 + x2 * x2)) - 0.5) / (
                1 + 0.001 * (x1 * x1 + x2 * x2))
    return -OF


def BenchKornFunctionx10(x, y):
    x1 = x
    x2 = y
    z = complex(x1, x2)
    OF = 1 / (1 + abs(pow(z, 6) - 1))
    return -OF

def BenchBirdFunctionx10(x, y):
    x1 = x
    x2 = y
    OF = -sin(x1) * exp(pow(1 - cos(x2), 2)) - cos(x2) * exp(pow(1 - sin(x1), 2)) - pow(
        x1 - x2, 2)
    return -OF


def BenchEkliFunctionx10(x, y):
    x1 = x
    x2 = y
    OF = -e + 20 * exp(-sqrt((pow(x1, 2) + pow(x2, 2)) / 50)) + exp(
        1 / 2 * (cos(2 * pi * x1) + cos(2 * pi * x2)))
    return -OF

def Bench4(x, y):
    a1 = x ** 2
    a2 = y ** 2
    a = 1 - (a1 + a2) ** 0.5 / pi
    OF = (cos(x) * cos(y) * exp((fabs(a)))) ** 2
    return -OF
