from PIL import Image
import numpy as np

from test_metrics_2 import Metrics
from picture_utils import Picture

def hide_message(message, cover_path, stego_path):
    cover = Image.open(cover_path)

    if cover.size[0] * cover.size[1] * 8 < 24 + 8 * len(message + '\x00'):
        print("Изображение слишком маленькое")
        return

    cover = np.array(cover)

    # Добавление признака встраивания
    embed_string_bin = string_to_bin(message + '\x00')
    embed_string_bin_len = len(embed_string_bin)
    if embed_string_bin_len % 8 != 0:
        embed_string_bin += '0' * (8 - embed_string_bin_len % 8)
    embed_string_bin += '11111111'

    rows, cols, rgb = cover.shape
    b = cover[:, :, 2].flatten().tolist()
    b_idx = 0

    for bit in embed_string_bin:
        # Получение компонента
        x, _ = b_idx // cols, b_idx % cols
        lsb = b[b_idx] & 1

        # Встраивание бита
        if lsb != int(bit):
            b[b_idx] = (b[b_idx] & ~1) | int(bit)

        b_idx += 1

    # Конвертация обратно в изображение
    b = np.array(b).reshape((rows, cols))
    stego = Image.fromarray(np.dstack([cover[:, :, 0], cover[:, :, 1], b]).astype('uint8'))
    stego.save(stego_path)


def reveal_message(stego_path):
    stego = Image.open(stego_path)

    stego = np.array(stego)

    # Индексация пикселей и RGBA-каналов
    rows, cols, rgb = stego.shape
    b = stego[:, :, 2].flatten().tolist()
    b_idx = 0

    # Нахождение признака встраивания
    embed_bits = []
    current_bits = []
    while current_bits != [1, 1, 1, 1, 1, 1, 1, 1]:
        if b_idx >= len(b):
            break
        _, y = b_idx // cols, b_idx % cols
        lsb = b[b_idx] & 1
        current_bits.append(lsb)
        b_idx += 1
        if len(current_bits) == 8:
            embed_bits.extend(current_bits)
            current_bits = []

    # Получение скрытой строки
    embed_string = ''
    for i in range(0, len(embed_bits), 8):
        byte = ''.join([str(bit) for bit in embed_bits[i:i + 8]])
        char = chr(int(byte, 2))
        embed_string += char
        if char == '\x00':
            break

    return embed_string[:-1]

def char_to_bin(char):
    return bin(ord(char))[2:].zfill(8)

def string_to_bin(string):
    return ''.join([char_to_bin(char) for char in string])

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '016b') for char in message)
    return binary_message


container_image_path = "container_img.png"
container_image = Image.open(container_image_path)

secret_message = "ANTONIO,10.2'erieriferigierg iveromp revnrveio;"
print("Успешно скрыто сообщение:", secret_message)

hidden_image_path = "container_img.png"
hide_message(secret_message, container_image_path, hidden_image_path)

hidden_image = Image.open(hidden_image_path)
extracted_message = reveal_message(hidden_image_path)
print("Извлечённое сообщение:", extracted_message)

metrics = Metrics(Picture(container_image_path), Picture(hidden_image_path))
metric_maxD = metrics.calculate_maxD()
print(f"Максимальное абсолютное отклонение maxD =", metric_maxD)

metric_mse = metrics.calculate_NMSE()
print(f"Среднее квадратичное отклонение MSE =", metric_mse)

metric_lP = metrics.calculate_Lp()
print(f"Норма Минковского Lp =", metric_lP)
