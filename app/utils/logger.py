# logger.py
import logging
import sys

def get_logger(name: str):
    # 创建一个日志记录器
    logger = logging.getLogger(name)

    # 设置日志级别
    logger.setLevel(logging.DEBUG)

    # 创建一个文件处理器，将日志输出到文件
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # 创建一个流处理器，将日志输出到 stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)

    # 创建一个日志格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger
