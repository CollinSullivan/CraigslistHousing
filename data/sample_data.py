import pandas as pd
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Randomly sample rows from provided csv')
  parser.add_argument('csv', help='the csv to sample from')
  parser.add_argument('num_rows', type=int, help='number of rows to sample')
  args = parser.parse_args()

  data = pd.read_csv(args.csv, index_col=0)
  sample = data.sample(n=args.num_rows if args.num_rows < len(data) else len(data), axis=0)
  sample.reset_index(inplace=True)
  sample.drop('index', axis=1, inplace=True)

  sample.to_csv(args.csv[:-4] + '_' + str(args.num_rows) + '.csv')


  

