1. get all named urls in django
```python
from django.urls import get_resolver
res = get_resolver(None)
url_patterns = res.url_patterns
[one if not hasattr(one, 'url_patterns') else [child for child in one.url_patterns]  for one in res.url_patterns]
```