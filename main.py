from src.app_controller import AppController

import threading



if __name__ == "__main__":
    app_controller = AppController()
    app_controller.start_watcher()
    app_controller.start()


