from django.http import JsonResponse



class CommonResponse(JsonResponse):
    def __init__(self, data, code=None, *args, **kwargs):
        self.data = data
        curent_code = 200 if code is None else code
        kwargs['json_dumps_params'] = {'ensure_ascii': False}
        super().__init__(data, status=curent_code, *args, **kwargs)
