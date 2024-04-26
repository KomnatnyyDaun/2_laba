from PIL import Image, ImageDraw


class Picture:

    def __init__(self, path: str):
        self.image: Image = Image.open(path)

        self.width: int = self.image.size[0]
        self.height: int = self.image.size[1]
        self.draw: ImageDraw = ImageDraw.Draw(self.image)
        self.path: str = path

    def max_length_text(self) -> int:
        step = 4
        lenText = ((self.width - step) // step)
        lenText *= ((self.height - step) // step)
        return lenText

    def get_pix(self, row: int, col: int):
        return (self.image.load()[row, col][0], self.image.load()[row, col][1], self.image.load()[row, col][2])

    def set_pixel(self, row, col, val):
        self.image.putpixel((row, col), val)

    def plus_pixel(self, row, col, val):
        self.image.putpixel((row, col),
                            (self.get_pix(row, col)[0] + val[0],
                             self.get_pix(row, col)[1] + val[1],
                             self.get_pix(row, col)[2] + val[2])
                            )

    # Метод для получения среднего значения компонентов
    def get_awg_pix(self, row: int, col: int):
        return sum(self.image.load()[row, col]) / len(self.image.load()[row, col])
