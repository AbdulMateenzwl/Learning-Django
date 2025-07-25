# myapp/middleware.py

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Request path: {request.path}, User: {request.user}")
        
        response = self.get_response(request)
        
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Called just before the view is called
        pass

    def process_exception(self, request, exception):
        # Called if the view raises an exception
        pass

    def process_template_response(self, request, response):
        # Called if response has a render() method (like TemplateResponse)
        return response

