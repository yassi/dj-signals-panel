from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import admin
from django.http import Http404

from .conf import get_css_context
from .interfaces import SignalListInterface, SignalDetailInterface


@staff_member_required
def index(request):
    """Display panel dashboard with signal list."""
    interface = SignalListInterface()

    search_query = request.GET.get("q", "").strip()
    app_filter = request.GET.get("app", "").strip()

    if search_query:
        signals = interface.search_signals(search_query)
    else:
        signals = interface.get_signal_list()

    if app_filter:
        signals = [s for s in signals if s.app_label == app_filter]

    stats = interface.get_stats()
    grouped = interface.get_grouped_signals()
    available_apps = sorted(grouped.keys())

    context = admin.site.each_context(request)
    context.update(get_css_context())
    context.update(
        {
            "title": "Dj Signals Panel",
            "signals": signals,
            "stats": stats,
            "grouped_signals": grouped,
            "search_query": search_query,
            "app_filter": app_filter,
            "available_apps": available_apps,
            "total_displayed": len(signals),
        }
    )
    return render(request, "admin/dj_signals_panel/index.html", context)


@staff_member_required
def signal_detail(request, signal_id):
    """Display detailed information about a specific signal."""
    interface = SignalDetailInterface(signal_id)
    detail = interface.get_signal_detail()

    if detail is None:
        raise Http404("Signal not found")

    context = admin.site.each_context(request)
    context.update(get_css_context())
    context.update(
        {
            "title": f"Signal: {detail.name}",
            "signal": detail,
            "receivers": detail.receivers,
        }
    )
    return render(request, "admin/dj_signals_panel/detail.html", context)
