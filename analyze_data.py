
import pandas as pd
from pathlib import Path

folder = Path(__file__).parent
csv_file = folder / "sample_dataset.csv"
report_file = folder / "summary_report.txt"

df = pd.read_csv(csv_file)

with open(report_file, "w", encoding="utf-8") as report:
    report.write("WEB DATA EXTRACTOR - SUMMARY REPORT\n")
    report.write("=" * 40 + "\n")
    report.write(f"Total books: {len(df)}\n")
    report.write(
        f"Average price: GBP {df['Price_GBP'].mean():.2f}\n"
    )
    report.write(
        f"Minimum price: GBP {df['Price_GBP'].min():.2f}\n"
    )
    report.write(
        f"Maximum price: GBP {df['Price_GBP'].max():.2f}\n"
    )

    report.write("\nRating distribution:\n")
    report.write(df["Rating"].value_counts().to_string())
    report.write("\n")

print(f"Summary report saved to: {report_file}")
