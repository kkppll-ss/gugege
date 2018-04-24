import itertools
import glob
import os
import csv

import pandas as pd
import tqdm

INPUT_DIR = "data423"
OUTPUT_DIR = "output"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename_list = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    filename_pairs = list(itertools.combinations(filename_list, 2))
    for i, (left_filename, right_filename) in enumerate(filename_pairs):
        left_df = pd.read_csv(left_filename)
        right_df = pd.read_csv(right_filename)
        left_df = left_df.iloc[:, 1:]
        right_df = right_df.iloc[:, 1:]
        *_, left_basename = os.path.split(left_filename)
        *_, right_basename = os.path.split(right_filename)
        left_basename, _ = os.path.splitext(left_basename)
        right_basename, _ = os.path.splitext(right_basename)
        print("processing {} and {}, {} / {}".format(left_basename, right_basename, i+1, len(filename_pairs)))
        with open(os.path.join(OUTPUT_DIR, "{}-{}.csv".format(left_basename, right_basename)), "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow([left_basename, right_basename, "cov"])
            for left_column in tqdm.tqdm(left_df, total=left_df.shape[1], desc=left_basename, ascii=True):
                for right_column in tqdm.tqdm(right_df, total=right_df.shape[1], desc=right_basename, ascii=True):
                    cov = left_df[left_column].cov(right_df[right_column])
                    writer.writerow([left_column, right_column, cov])



if __name__ == "__main__":
    main()