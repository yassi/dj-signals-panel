from __future__ import annotations

from .data import (
    DiscoveredSignal,
    SignalDetail,
    SignalStats,
    SignalSummary,
    SignalUtils,
)


class SignalListInterface:
    """
    Interface for the signal list (index) page.

    Thin orchestration layer: delegates discovery and stats to SignalUtils,
    then applies view-level filtering and grouping.
    """

    def __init__(self):
        self._signals: list[SignalSummary] | None = None

    def get_signal_list(self) -> list[SignalSummary]:
        """All discovered signals with summary metadata."""
        if self._signals is None:
            self._signals = [s.to_summary() for s in SignalUtils.discover_all()]
        return self._signals

    def get_grouped_signals(self) -> dict[str, list[SignalSummary]]:
        """Signals grouped by category."""
        grouped: dict[str, list[SignalSummary]] = {}
        for sig in self.get_signal_list():
            grouped.setdefault(sig.category, []).append(sig)
        return grouped

    def search_signals(self, query: str) -> list[SignalSummary]:
        """Filter signals by name, module, or category."""
        q = query.lower()
        return [
            s
            for s in self.get_signal_list()
            if (
                q in s.name.lower()
                or q in s.module.lower()
                or q in s.signal_id.lower()
                or q in s.category.lower()
            )
        ]

    def get_stats(self) -> SignalStats:
        """Aggregate statistics for the stats card."""
        return SignalUtils.compute_stats(self.get_signal_list())


class SignalDetailInterface:
    """
    Interface for the signal detail page.

    Given a signal_id, resolves the signal and extracts full receiver
    information including source locations.
    """

    def __init__(self, signal_id: str):
        self.signal_id = signal_id

    def get_signal_detail(self) -> SignalDetail | None:
        """Full signal info with all receivers. Returns None if not found."""
        signal = DiscoveredSignal.from_id(self.signal_id)
        if signal is None:
            return None
        return signal.to_detail()
