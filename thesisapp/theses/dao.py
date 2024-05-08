from django.db.models import Count

from .models import Major , Thesis


def load_courses(params={}):
    q = Thesis.objects.all()
    kw = params.get('kw')
    if kw:
        q = q.filter(name__icontains=kw)

    cate = params.get('cate_id')
    if cate:
        q = q.filter(cate_id=cate)


def count_thesis_by_major():
    return Major.objects.annotate(count=Count('thesis__id')).values("id", "name", "count").order_by('id')