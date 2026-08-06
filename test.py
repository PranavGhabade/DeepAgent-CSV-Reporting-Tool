from utils.pdf_report_generator import generate_pdf_report


class DummyMemory:

    def get_report(self, key):

        return """
# Dataset Analysis Report

## Executive Summary

This is a summary.

## Dataset Overview

Rows : 100

Columns : 10

## Statistical Findings

### Statistics

| Metric | Value |
|--------|-------|
| Mean | 20 |

## Visual Analysis

### Figure 1. Sales Trend

Description:
Monthly sales trend.

Analysis:
Sales increased steadily.

### Figure 2. Product Distribution

Description:
Product categories.

Analysis:
Category A dominates.

## Business Insights

### Revenue Growth

Revenue improved significantly.

* High customer retention
* Strong sales performance

## Recommendations

1. Improve monitoring

2. Reduce duplicates

3. Increase automation

## Conclusion

Dataset successfully analyzed.
"""

    def get_analysis(self, key):

        if key == "visualizations":

            return {

                "line_Timestamp_total_bytes":
                "outputs/charts/Timestamp_total_bytes_line.png",

                "pie_action":
                "outputs/charts/action_pie.png",

            }

        if key == "profile":

            return {

                "rows": 100,
                "columns": 10,
                "duplicate_rows": 5,
            }

        return {}


memory = DummyMemory()

pdf = generate_pdf_report(memory)

print(pdf)