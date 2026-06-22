from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "processed_custom_sales.csv"


def process_retail_inventory():
    df = pd.read_csv(DATA_DIR / "retail_store_inventory.csv")

    df["Sales"] = df["Units Sold"] * df["Price"]

    output = df[["Sales", "Date", "Region"]].copy()
    return output


def process_fmcg():
    df = pd.read_csv(DATA_DIR / "FMCG_2022_2024.csv")

    df["Sales"] = df["units_sold"] * df["price_unit"]

    output = df[["Sales", "date", "region"]].copy()
    output = output.rename(
        columns={
            "date": "Date",
            "region": "Region",
        }
    )

    return output


def process_coffee_sales():
    df = pd.read_csv(DATA_DIR / "index_1.csv")

    output = pd.DataFrame()
    output["Sales"] = df["money"]
    output["Date"] = df["date"]
    output["Region"] = "Unknown"

    return output


def main():
    retail_df = process_retail_inventory()
    fmcg_df = process_fmcg()
    coffee_df = process_coffee_sales()

    final_df = pd.concat(
        [retail_df, fmcg_df, coffee_df],
        ignore_index=True
    )

    final_df["Date"] = pd.to_datetime(final_df["Date"], errors="coerce")
    final_df = final_df.dropna(subset=["Date", "Sales"])
    final_df["Date"] = final_df["Date"].dt.strftime("%Y-%m-%d")

    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Processed file created successfully!")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total rows: {len(final_df)}")
    print(final_df.head())


if __name__ == "__main__":
    main()