from .models import Library

def get_libraries(request):
    return {'all_libraries': Library.objects.all()}