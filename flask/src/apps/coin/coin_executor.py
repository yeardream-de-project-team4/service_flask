import subprocess
import threading

class CoinExecutor:
    _instance = None
    _lock = threading.Lock() 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CoinExecutor, cls).__new__(cls)
            cls._instance.process = None
        return cls._instance

    def start_background_script(self):
        with CoinExecutor._lock:
            if self.process is None or self.process.poll() is not None:
                try:
                    # 특정 파이썬 파일을 백그라운드에서 실행합니다.
                    self.process = subprocess.Popen(['python', 'apps/coin_producer.py'])
                    return "Background script started."
                except Exception as e:
                    return "Failed to start background script."
            else:
                return "Background script is already running."
            

    def stop_background_script(self):
        with CoinExecutor._lock: 
            if self.process is not None and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()
                self.process = None
                return "Background script stopped."
            else:
                return "No background script is currently running."
        
        
coin_executor_instance = CoinExecutor()