import os
import json
import time
import logging
import threading
from datetime import datetime
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

class SeekeyLogger:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super(SeekeyLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        # 1. 自动定位路径：获取 helpers 文件夹的上一级作为项目根目录
        current_file_path = os.path.abspath(__file__) 
        helpers_dir = os.path.dirname(current_file_path)
        self.root_dir = os.path.dirname(helpers_dir)

        # 2. 加载 .env 配置文件
        load_dotenv(os.path.join(self.root_dir, ".env"))

        # 从 .env 读取配置
        self.system_name = os.getenv("SYSTEM_NAME", "SeekeySDK")
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, log_level_str, logging.INFO)

        # 3. 在根目录下创建 Logs 文件夹（与 helpers 平级）
        log_dir = os.path.join(self.root_dir, "Logs")
        os.makedirs(log_dir, exist_ok=True)

        # 4. 生成文件名
        file_date = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(log_dir, f"{self.system_name}_{file_date}.log")

        # 5. 配置 Logger
        self.logger = logging.getLogger(self.system_name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # --- 自定义 JSON 格式化器 ---
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_record = {
                    "time": self.formatTime(record, "%H:%M:%S"),
                    "pid": record.process,
                    "level": record.levelname,
                    "module": record.name,
                    "message": record.getMessage(),
                }
                # 提取额外的字段
                if hasattr(record, 'extra_data'):
                    log_record.update(record.extra_data)
                return json.dumps(log_record, ensure_ascii=False)

        # 6. 文件处理器：JSON 格式，带自动切分（10MB）
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)

        # 7. 控制台处理器：普通文本格式，方便调试
        console_handler = logging.StreamHandler()
        console_fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%H:%M:%S')
        console_handler.setFormatter(console_fmt)
        self.logger.addHandler(console_handler)

        self._initialized = True

    def _log(self, level, msg, **kwargs):
        if self.logger.isEnabledFor(level):
            # 将 kwargs 作为 extra 传入，方便 JSON 序列化
            self.logger.log(level, msg, extra={'extra_data': kwargs})

    def add_info(self, msg, **kwargs): self._log(logging.INFO, msg, **kwargs)
    def add_error(self, msg, **kwargs): self._log(logging.ERROR, msg, **kwargs)
    def add_debug(self, msg, **kwargs): self._log(logging.DEBUG, msg, **kwargs)

    @contextmanager
    def timer(self, task_name="Task"):
        """计时上下文管理器：用于记录 API 耗时"""
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = round(time.perf_counter() - start, 4)
            self._log(logging.INFO, f"{task_name} 完成", duration_sec=duration)

# 直接实例化，外部 import 即可使用
logger = SeekeyLogger()