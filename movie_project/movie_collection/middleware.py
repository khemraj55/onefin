import threading

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.lock = threading.Lock()

    def __call__(self, request):
        with self.lock:
            self.request_count += 1

        response = self.get_response(request)
        return response

    def process_response(self, request, response):
        pass

    def get_request_count(self):
        with self.lock:
            return self.request_count

    def reset_request_count(self):
        with self.lock:
            self.request_count = 0