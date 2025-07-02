import argparse

import matplotlib

matplotlib.use('QtAgg')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="PZEM-004T log plot tool")
    parser.add_argument(
        "-f", "--file", type=str, default=f'{os.getenv("HOME")}/logs/pzem_log.csv',
        help="csv file"
    )
    args = parser.parse_args()
    csv_file_path = args.file

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found at '{csv_file_path}'")
        sys.exit(1)
    try:
        # Load the data from the specified CSV file
        df = pd.read_csv(csv_file_path)

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', errors='coerce')
            if df['timestamp'].isnull().any():
                print("Warning: Some timestamps could not be parsed and were converted to NaT.")
                print("Rows with unparsed timestamps (first 5):")
                print(df[df['timestamp'].isnull()].head())
                df.dropna(subset=['timestamp'], inplace=True)
                print("Rows with unparsed timestamps have been dropped.")
                if df.empty:
                    print("Error: No valid timestamp data remaining after dropping unparsed rows. Exiting.")
                    sys.exit(1)
        else:
            print("Warning: 'timestamp' column not found. Time-series plots might not behave as expected.")

        print("DataFrame Head (after timestamp parsing):")
        print(df.head())
        print("\n")
        print("DataFrame Info (after timestamp parsing):")
        print(df.info())

        plot_columns = ['voltage', 'current', 'frequency']
        available_plot_columns = [col for col in plot_columns if col in df.columns]

        if not available_plot_columns:
            print("No 'voltage', 'current', or 'frequency' columns found for plotting.")
        else:
            if df['timestamp'].nunique() < 2:
                print(
                    "Not enough unique timestamp data points to create a line plot after processing. Need at least 2.")
                sys.exit(0)

            fig, axes = plt.subplots(len(available_plot_columns), 1, figsize=(10, 5 * len(available_plot_columns)),
                                     sharex=True)

            if len(available_plot_columns) == 1:
                axes = [axes]

            for i, col_name in enumerate(available_plot_columns):
                sns.lineplot(data=df, x='timestamp', y=col_name, marker=',', markersize=1, ax=axes[i])
                axes[i].set_title(f'{col_name.capitalize()} Over Time')
                unit = ""
                if col_name == "voltage":
                    unit = "(V)"
                elif col_name == "current":
                    unit = "(A)"
                elif col_name == "frequency":
                    unit = "(Hz)"
                axes[i].set_ylabel(f'{col_name.capitalize()} {unit}')
                axes[i].grid(True, linestyle='--', alpha=0.7)

            plt.xticks(rotation=45)
            plt.xlabel('Timestamp')
            plt.tight_layout()

            # --- Change: Instead of saving, show the plot ---
            print("\nDisplaying interactive plot...")
            plt.show()  # This will open an interactive window or display in a notebook environment


    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file_path}' is empty.")
    except pd.errors.ParserError:
        print(f"Error: Could not parse '{csv_file_path}'. Make sure it's a valid CSV.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
