def check_distance(landmark: float, distance_min: int, distance_max: int) -> bool:
    """
    Функция проверяет, входит ли расстояние в указанный диапазон пользователем.
    """

    return distance_min <= landmark <= distance_max
