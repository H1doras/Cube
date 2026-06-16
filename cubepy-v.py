import math
import time
import os

# Инициализация углов поворота
A, B, C = 0.0, 0.0, 0.0

width, height = 160, 44
background_ascii_code = '.'
distance_from_cam = 100
K1 = 40
increment_speed = 0.6

# Глобальные переменные для горизонтального смещения кубов
horizontal_offset = 0.0
cube_width = 20.0

# Инициализируем буферы нужного размера
z_buffer = [0.0] * (width * height)
buffer = [background_ascii_code] * (width * height)


def calculate_x(i, j, k):
    """3D Вращение по оси X"""
    return (j * math.sin(A) * math.sin(B) * math.cos(C) -
            k * math.cos(A) * math.sin(B) * math.cos(C) +
            j * math.cos(A) * math.sin(C) +
            k * math.sin(A) * math.sin(C) +
            i * math.cos(B) * math.cos(C))


def calculate_y(i, j, k):
    """3D Вращение по оси Y"""
    return (j * math.cos(A) * math.cos(C) +
            k * math.sin(A) * math.cos(C) -
            j * math.sin(A) * math.sin(B) * math.sin(C) +
            k * math.cos(A) * math.sin(B) * math.sin(C) -
            i * math.cos(B) * math.sin(C))


def calculate_z(i, j, k):
    """3D Вращение по оси Z"""
    return k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)


def calculate_for_surface(cube_x, cube_y, cube_z, ch):
    global z_buffer, buffer

    # 1. Поворот точки в 3D пространстве
    x = calculate_x(cube_x, cube_y, cube_z)
    y = calculate_y(cube_x, cube_y, cube_z)
    z = calculate_z(cube_x, cube_y, cube_z) + distance_from_cam

    # 2. Рассчитываем обратную глубину (One Over Z)
    ooz = 1 / z

    # 3. Проекция 3D на 2D экран (с учетом соотношения сторон терминала * 2)
    xp = int(width / 2 + horizontal_offset + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)

    # 4. Проверка границ экрана и Z-буферизация
    idx = xp + yp * width
    if 0 <= idx < width * height:
        if ooz > z_buffer[idx]:
            z_buffer[idx] = ooz
            buffer[idx] = ch


def main():
    global A, B, C, cube_width, horizontal_offset, z_buffer, buffer

    # Включаем поддержку ANSI кодов в Windows (если запускается там)
    if os.name == 'nt':
        os.system('')

    # Очистка экрана в начале работы
    print("\x1b[2J", end="")

    try:
        while True:
            # Сброс буферов для нового кадра
            buffer = [background_ascii_code] * (width * height)
            z_buffer = [0.0] * (width * height)

            # --- Рендеринг трех кубов разного размера ---

            # Первый куб (Большой, смещен влево)
            cube_width = 20.0
            horizontal_offset = -2 * cube_width
            render_cube()

            # Второй куб (Средний, смещен чуть вправо)
            cube_width = 10.0
            horizontal_offset = 1 * cube_width
            render_cube()

            # Третий куб (Маленький, смещен сильно вправо)
            cube_width = 5.0
            horizontal_offset = 8 * cube_width
            render_cube()

            # Вывод кадра на экран (перенос курсора в левый верхний угол)
            print("\x1b[H", end="")

            # Собираем символы в строки для быстрой печати в Python
            output = []
            for k in range(width * height):
                if k % width == 0 and k > 0:
                    output.append('\n')
                output.append(buffer[k])
            print("".join(output), end="")

            # Изменение углов для анимации вращения
            A += 0.05
            B += 0.05
            C += 0.01

            # Задержка (в секундах)
            time.sleep(0.016)

    except KeyboardInterrupt:
        # Корректный выход по Ctrl+C
        print("\nПрограмма остановлена.")


def render_cube():
    """Проход по двум координатам для отрисовки всех 6 граней куба"""
    cube_x = -cube_width
    while cube_x < cube_width:
        cube_y = -cube_width
        while cube_y < cube_width:
            calculate_for_surface(cube_x, cube_y, -cube_width, '@')
            calculate_for_surface(cube_width, cube_y, cube_x, '$')
            calculate_for_surface(-cube_width, cube_y, -cube_x, '~')
            calculate_for_surface(-cube_x, cube_y, cube_width, '#')
            calculate_for_surface(cube_x, -cube_width, -cube_y, ';')
            calculate_for_surface(cube_x, cube_width, cube_y, '+')
            cube_y += increment_speed
        cube_x += increment_speed


if __name__ == "__main__":
    main()