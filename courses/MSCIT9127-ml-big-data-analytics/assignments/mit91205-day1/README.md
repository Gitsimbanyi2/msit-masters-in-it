# MIT 91205 Day 1 practical — From raw data to insight

Completed 1 November 2026. Jupyter notebook matches the lecture (`Day One.ipynb`). `.py` scripts are the same labs for Command Prompt.

## Files

| File | What it is |
|------|------------|
| `generate_dataset.py` | Builds `sample-sales.csv` with seed 42 (1014 orders) |
| `lab1.py` … `lab7.py` | Meet the data → lifecycle pipeline |
| `Day One.ipynb` | Lecture-style notebook (run top to bottom) |
| `sample-sales.csv` | Generated dataset |
| `revenue_by_region.png` | Lab 2 chart |
| `revenue_forecast.png` | Lab 4 chart |
| `top_combinations.png` | Lab 7 chart |
| `requirements.txt` | pandas, matplotlib, duckdb |

Do not commit `day1env/` (virtual environment). Lecturer PDFs stay local, same policy as MSCIT9128.

## Quick start (Windows)

```text
python -m venv day1env
day1env\Scripts\activate
python -m pip install -r requirements.txt
python generate_dataset.py
python lab1.py
```

Study notes: `../../day1-study-notes.md`
