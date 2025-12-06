import argparse
import csv
import sys
import os
import re

def clean_csv(input_file, output_file, remove_duplicates, strip_whitespace, remove_empty):
    """
    Reads a CSV, applies cleanup rules, and writes to a new file.
    """
    try:
        seen_rows = set()
        cleaned_data = []
        
        # For opening and reading the input file
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            try:
                header = next(reader)
                cleaned_data.append(header)
            except StopIteration:
                print(f"Error: The file '{input_file}' is empty.")
                return

            rows_processed = 0
            rows_removed_empty = 0
            rows_removed_dup = 0

            for row in reader:
                rows_processed += 1
                
                # Striping Whitespace
                if strip_whitespace:
                    row = [cell.strip() for cell in row]

                # Remove Empty Rows
                if remove_empty:
                    if not any(cell for cell in row):
                        rows_removed_empty += 1
                        continue

                # 3. Remove Duplicates
                if remove_duplicates:
                    row_tuple = tuple(row)
                    if row_tuple in seen_rows:
                        rows_removed_dup += 1
                        continue
                    seen_rows.add(row_tuple)

                cleaned_data.append(row)

        # Writing to the output file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_data)

        print(f"Success! Cleaned data saved to '{output_file}'")
        print(f"Stats:")
        print(f" - Total rows processed: {rows_processed}")
        if remove_duplicates:
            print(f" - Duplicates removed:   {rows_removed_dup}")
        if remove_empty:
            print(f" - Empty rows removed:   {rows_removed_empty}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{input_file}' or writing '{output_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="A simple tool to clean CSV files.",
        epilog="Example: python csv_cleanup.py input.csv -o clean.csv --remove-duplicates"
    )

    parser.add_argument(
        'input_file', 
        help="Path to the source CSV file."
    )

    parser.add_argument(
        '-o', '--output', 
        help="Path to the destination file. Defaults to 'cleaned_<input_file>'.",
        default=None
    )

    # Remove Duplicates
    parser.add_argument(
        '-d', '--remove-duplicates', 
        action='store_true', 
        help="Remove duplicate rows from the file."
    )

    # Flag: Regex Filter
    parser.add_argument(
        '-f', '--filter-regex', 
        type=str,
        default=None,
        help="Filter and remove rows where any cell matches the provided Python regular expression pattern."
    )

    # Strip Whitespace
    parser.add_argument(
        '-s', '--strip-whitespace', 
        action='store_true', 
        help="Strip leading/trailing whitespace from all cells."
    )

    # Remove Empty Rows
    parser.add_argument(
        '-e', '--remove-empty', 
        action='store_true', 
        help="Remove rows that contain no data."
    )

    # Parse arguments
    args = parser.parse_args()

    # Determine output filename if not provided
    if not args.output:
        base, ext = os.path.splitext(args.input_file)
        args.output = f"{base}_cleaned{ext}"

    # Check if input file exists before proceeding
    if not os.path.exists(args.input_file):
        parser.error(f"The file '{args.input_file}' does not exist.")

    clean_csv(
        args.input_file, 
        args.output, 
        args.remove_duplicates, 
        args.strip_whitespace, 
        args.remove_empty
    )

if __name__ == "__main__":
    main()