from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import admin

from .conf import get_css_context


@staff_member_required
def index(request):
    """
    Display panel dashboard.
    """
    context = admin.site.each_context(request)
    context.update(get_css_context())
    context.update(
        {
            "title": "Dj Signals Panel",
        }
    )
    return render(request, "admin/dj_signals_panel/index.html", context)
