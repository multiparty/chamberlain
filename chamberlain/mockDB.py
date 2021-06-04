from random import getrandbits
import time


class DB:
    """
    Simple DB interface for the server to  interact with
    a delay can be introduced to simulate computation time
    """
    def __init__(self):
        self.store = {'HRI107':
                [
                    (1, 'http://35.196.45.45:80'),
                    (2, 'http://35.245.230.36:80'),
                    (3, 'http://52.150.39.162:5000')
                    ]
                }

    def retrieve(self, key: str, refresh: bool = False, delay: float = 0.0):
        if delay > 0.0:
            time.sleep(delay)
        if key in self.store and not refresh:
            return self.store[key]
        else:
            return None
