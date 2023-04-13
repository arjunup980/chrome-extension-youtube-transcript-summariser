from django.core.cache import cache
from django.views.decorators.cache import cache_page

def cache_view(timeout=86400, *, key_prefix=None):
    def decorator(view_func):
        cache_decorator = cache_page(timeout=timeout, key_prefix=key_prefix)
        def decorated(request, *args, **kwargs):
            try:
                refresh = dict(request.request.query_params).get('refresh')[0] in ['true', 'True', True]
            except Exception as e:
                refresh = False
                
            if refresh:
                cache.clear(key_prefix)
            return cache_decorator(view_func)(request, *args, **kwargs)
        return decorated
    return decorator
