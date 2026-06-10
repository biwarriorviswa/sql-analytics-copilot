# SQL Analytics Copilot

An AI-powered SQL Analytics Copilot built using multi-agent architecture, LangGraph workflows, forecasting models, human-in-the-loop approvals, and interactive Streamlit dashboards.

## Overview

SQL Analytics Copilot enables users to:

* Convert natural language questions into SQL queries
* Validate and optimize generated SQL
* Execute queries against enterprise databases
* Generate analytical insights automatically
* Detect and perform forecasting tasks
* Support human approval workflows
* Generate charts and visualizations
* Deliver results through a Streamlit dashboard

---

## Architecture Roadmap

### Phase 1 – SQL Generation Pipeline

Components:

* SQL Agent
* Validator Agent
* Query Optimizer
* SQL Executor

Workflow:

```text
User Query
    ↓
SQL Agent
    ↓
Validator
    ↓
Optimizer
    ↓
Execute SQL
    ↓
Result Set
```

### Phase 2 – Analytics & Insights

Components:

* Analytics Agent
* Insight Agent

Capabilities:

* KPI calculations
* Trend analysis
* Business insights generation
* Automated commentary

---

### Phase 3 – Forecasting

Components:

* Forecast Agent
* Forecast Detector
* Prophet Forecasting
* XGBoost Forecasting

Capabilities:

* Time-series forecasting
* Demand prediction
* Revenue forecasting
* Automatic forecast detection

---

### Phase 4 – LangGraph Workflow

Components:

* Workflow Graph
* State Management
* Supervisor Agent

Capabilities:

* Agent orchestration
* State tracking
* Multi-step execution flows

---

### Phase 5 – Human Approval

Components:

* Approval Agent

Capabilities:

* Human-in-the-loop validation
* Approval checkpoints
* Query review workflow

---

### Phase 6 – Chart Generation

Components:

* Chart Agent

Capabilities:

* Automatic chart recommendations
* Visualization generation
* Dashboard-ready outputs

---

### Phase 7 – Streamlit Dashboard

Components:

* Interactive Dashboard
* Reports Module
* Charts Module

Capabilities:

* Natural language analytics
* Interactive visualizations
* Forecast reports
* Business intelligence dashboard

---

## Project Structure

```text
sql-analytics-copilot/
│
├── config.py
├── main.py
│
├── agents/
│   ├── analytics_agent.py
│   ├── approval_agent.py
│   ├── chart_agent.py
│   ├── forecast_agent.py
│   ├── forecast_detector.py
│   ├── insight_agent.py
│   ├── optimizer.py
│   ├── sql_agent.py
│   ├── supervisor.py
│   └── validator.py
│
├── dashboard/
│   ├── charts.py
│   ├── reports.py
│   └── streamlit_app.py
│
├── database/
│   ├── mysql.py
│   └── schema_loader.py
│
├── forecasting/
│   ├── model_registry.py
│   ├── prophet_forecaster.py
│   └── xgboost_forecaster.py
│
├── graph/
│   ├── state.py
│   └── workflow.py
│
├── monitoring/
│   ├── logger.py
│   └── metrics.py
│
├── tests/
│   ├── test_analytics_pipeline.py
│   ├── test_db.py
│   ├── test_forecast_agent.py
│   ├── test_forecast_detector.py
│   ├── test_model_registry.py
│   ├── test_optimizer.py
│   ├── test_prophet_forecaster.py
│   ├── test_schema.py
│   ├── test_sql_agent.py
│   ├── test_sql_pipeline.py
│   ├── test_validator.py
│   └── test_xgboost_forecaster.py
│
└── utils/
    └── sql_parser.py
```

---

## Core Agents

### SQL Agent

Converts natural language questions into SQL queries.

### Validator Agent

Validates generated SQL syntax and schema compatibility.

### Optimizer Agent

Improves query performance before execution.

### Analytics Agent

Performs aggregations and business metric calculations.

### Insight Agent

Generates human-readable insights from query results.

### Forecast Agent

Builds forecasts using supported forecasting models.

### Chart Agent

Creates chart specifications and visualizations.

### Approval Agent

Handles human approval workflows.

### Supervisor Agent

Coordinates agent execution within LangGraph.

---

## Forecasting Models

Supported forecasting engines:

* Prophet
* XGBoost

The Model Registry automatically selects and manages forecasting models.

---

## Monitoring

Monitoring framework includes:

* Structured logging
* Performance metrics
* Pipeline observability
* Execution tracking

---

## Testing

Run all tests:

```bash
pytest
```

Run specific tests:

```bash
pytest tests/test_sql_agent.py
```

---

## Future Enhancements

* Multi-database support (PostgreSQL, Snowflake, SQL Server)
* Vector database integration
* Semantic caching
* RAG-based schema understanding
* Advanced forecasting models
* Role-based approvals
* Enterprise authentication
* Dashboard export to PDF and PowerPoint

---

## Technology Stack

* Python
* LangGraph
* Streamlit
* MySQL
* Prophet
* XGBoost
* PyTest
* Pandas
* SQLAlchemy

---

## Author

SQL Analytics Copilot Project
