# DeepAgent CSV Reporting Tool

An AI-powered CSV analysis and reporting tool built using a **Deep Agent architecture**. It automatically analyzes datasets, generates visualizations, extracts insights, and produces structured reports.

## 🚀 Features

- 📊 Automated CSV profiling and analysis
- 🤖 Multi-agent data analysis workflow
- 📈 Statistical analysis and visualizations
- 💡 Automated business insights
- 📝 Markdown and PDF report generation
- 💬 Natural-language queries over datasets

## 🏗️ Architecture

```text
CSV Dataset
     │
     ▼
  Planner
     │
     ├──► Profiler
     ├──► Statistics
     ├──► Visualization
     └──► Business Insights
              │
              ▼
       Report Generator
              │
              ▼
       Markdown / PDF
```

The system uses specialized agents for different stages of the analysis pipeline, making the workflow modular and extensible.

## 📁 Project Structure

```text
├── agents/          # Specialized analysis agents
├── core/            # Agent orchestration and workflow
├── llm/             # LLM integration
├── memory/          # Agent memory
├── models/          # Data models
├── prompts/         # Agent prompts
├── tools/           # Data analysis tools
├── utils/           # Utility functions
├── outputs/         # Generated reports and visualizations
├── app.py           # Application entry point
└── requirements.txt # Project dependencies
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/PranavGhabade/DeepAgent-CSV-Reporting-Tool.git
cd DeepAgent-CSV-Reporting-Tool
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your LLM API credentials as required by the project.

## ▶️ Usage

Run the application:

```bash
python app.py
```

The application provides two primary workflows:

```text
1. Generate Complete Report
2. Ask Dataset Query
```

Generated reports, charts, and other outputs are stored in the `outputs/` directory.

## 🛠️ Tech Stack

- **Python**
- **Deep Agent Architecture**
- **LLMs**
- **Pandas**
- **Matplotlib**
- **ReportLab**

## 🔮 Future Scope

- Support for additional data formats
- Interactive dashboards
- Advanced data quality analysis
- Additional specialized agents
- Customizable report generation
