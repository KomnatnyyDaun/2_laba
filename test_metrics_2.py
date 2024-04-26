from picture_utils import Picture
class Metrics:

    def __init__(self, p1: Picture, p2: Picture):
        self.p1 = p1
        self.p2 = p2

    # Максимальное абсолютное отклонение
    def calculate_maxD(self):
        max_1 = -1
        max_2 = -1
        for i in range(self.p1.width):
            for j in range(self.p1.height):
                if abs(max_2 - max_1) < abs(self.p1.get_awg_pix(i, j) - self.p2.get_awg_pix(i, j)):
                    max_1 = self.p1.get_awg_pix(i, j)
                    max_2 = self.p2.get_awg_pix(i, j)

        if max_1 > max_2:
            return max_1
        else:
            return max_2

    # Норма Минковского
    def calculate_Lp(self, p=3):
        sum = 0
        for i in range(self.p1.width):
            for j in range(self.p1.height):
                sum += abs(self.p1.get_awg_pix(i, j) - self.p2.get_awg_pix(i, j)) ** p

        return (sum / (self.p1.width * self.p1.height)) ** (1 / p)

    # Нормированное среднее квадратичное отклонение
    def calculate_NMSE(self):
        sum_ch = 0
        sum_zn = 0
        for i in range(self.p1.width):
            for j in range(self.p1.height):
                sum_ch += (self.p1.get_awg_pix(i, j) - self.p2.get_awg_pix(i, j)) ** 2
                sum_zn += self.p1.get_awg_pix(i, j) ** 2

        return sum_ch / sum_zn

