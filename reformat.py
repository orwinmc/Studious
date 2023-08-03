import pandas as pd
import numpy as np

def format_output(q, a):
	return f'------------\n-1.) {q}\n\t1.) {a}\n-----------'

if __name__ == '__main__':
	df = pd.read_csv("samples/inputs/csvs/test.csv")
	x = df.to_numpy()
	x = np.swapaxes(x,0,1)

	questions = [q for q in x[1]]
	answers = [a for a in x[2]]

	questions = [q.replace('\n', '') for q in questions]
	answers = [a.replace('\n', '') for a in answers]

	with open('samples/outputs/test.txt', 'w') as output:
		for i,q in enumerate(questions):
			output.write(format_output(q, answers[i]))


