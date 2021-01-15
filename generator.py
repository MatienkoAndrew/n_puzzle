import sys
import random
import numpy as np


# http://stackoverflow.com/questions/306400/how-do-i-randomly-select-an-item-from-a-list-using-python
# http://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
# http://stackoverflow.com/questions/7701345/how-to-programatically-create-a-valid-15-puzzle-in-code
# https://mail.python.org/pipermail/tutor/2005-March/036777.html
# http://www.tutorialspoint.com/python/list_pop.htm
# http://stackoverflow.com/questions/3282823/get-key-with-the-least-value-from-a-dictionary
# http://pythonforbiologists.com/index.php/measuring-memory-usage-in-python/
# http://www.decalage.info/en/python/print_list
# http://www.tutorialspoint.com/python/number_sqrt.htm
# http://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int


def puzzle_generator(n, complexity):
	# x=n^2
	n = int(n)
	x = n**2
	l = list(range(x))

	cur_pos = 0

	for i in range(1, int(complexity) * 3):

		# up,down,left.right
		y = random.randint(1, 4)

		if y == 1:
			up_pos = cur_pos - n

			# is legal to move up, swap
			if (up_pos) >= 0:
				tmp = l[up_pos]
				l[up_pos] = 0
				l[cur_pos] = tmp
				cur_pos = up_pos

		elif y == 2:
			down_pos = cur_pos + n

			# is legal to move down, swap
			if (down_pos) < x:
				tmp = l[down_pos]
				l[down_pos] = 0
				l[cur_pos] = tmp
				cur_pos = down_pos



		elif y == 3:
			left_pos = cur_pos - 1

			# is legal to move left, swap
			if (cur_pos % n) != 0:
				tmp = l[left_pos]
				l[left_pos] = 0
				l[cur_pos] = tmp
				cur_pos = left_pos


		else:
			right_pos = cur_pos + 1

			# is legal to move right, swap
			if (cur_pos % n) != n - 1:
				tmp = l[right_pos]
				l[right_pos] = 0
				l[cur_pos] = tmp
				cur_pos = right_pos

	with open("test_1.txt", "w") as f:
		f.write(str(n)+'\n')
		l = np.array(l).reshape(n,n)
		for line in l:
			line = str(line).strip("[]")
			f.write(line+'\n')
	# print(' '.join(map(str, l)))


def main(arg):
	if len(arg) != 3:
		print("Usage python %s %s %s" % (arg[0], "dim", "complexity"))
		sys.exit(0)

	puzzle_generator(arg[1], arg[2])


main(sys.argv)
