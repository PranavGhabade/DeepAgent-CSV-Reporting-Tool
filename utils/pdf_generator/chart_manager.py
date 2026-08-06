"""
Chart Manager

Responsible for preparing chart information for the PDF renderer.

Responsibilities
----------------
1. Read chart paths from shared memory.
2. Validate chart files.
3. Resolve absolute paths.
4. Preserve chart order.
"""

from __future__ import annotations

import os
from collections import OrderedDict


class ChartManager:

    def __init__(self, chart_paths: dict | None):

        self.chart_paths = chart_paths or {}

    def get_resolved_charts(self):
        """
        Returns an OrderedDict containing only valid chart paths.

        Returns
        -------
        OrderedDict

        {
            chart_key : absolute_path
        }
        """

        resolved = OrderedDict()

        for chart_key, chart_path in self.chart_paths.items():

            if not isinstance(chart_path, str):
                continue

            absolute_path = (
                chart_path
                if os.path.isabs(chart_path)
                else os.path.abspath(chart_path)
            )

            if os.path.exists(absolute_path):

                resolved[chart_key] = absolute_path

            else:

                print(f"[ChartManager] Missing chart : {chart_key}")

        return resolved

    def get_chart_list(self):
        """
        Returns

        [
            ("chart_name", "absolute/path"),
            ...
        ]
        """

        return list(
            self.get_resolved_charts().items()
        )

    def count(self):

        return len(
            self.get_resolved_charts()
        )

    def is_empty(self):

        return self.count() == 0