from random import getrandbits
import time
class DB:
    '''
    Simple DB interface for the server to  interact with
    a delay can be introduced to simulate computation time
    '''
    def __init__(self):
        self.store = {'HRI107':
                [
                    (1, '12.34.56.78'),
                    (2, '23.45.67.89'),
                    (3, '34.56.78.90')
                    ]
                }

    def retrieve(self, key: str, refresh: bool = False, delay: float=0.0) -> int:
        if delay > 0.0:
            time.sleep(delay)
        if key in self.store and not refresh:
            return self.store[key]
        else:
            return None
