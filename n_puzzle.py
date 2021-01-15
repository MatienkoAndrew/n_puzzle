# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    n_puzzle.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: student <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/30 08:08:02 by student           #+#    #+#              #
#    Updated: 2020/12/30 08:09:20 by student          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from src.Parser import Parser
from src.algos import A_star, IDA_star
from src.utils.Arguments import Arguments
import argparse
import ctypes
import time

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if __name__ == '__main__':
	parser_arg = argparse.ArgumentParser(description="N-Puzzle project")
	parser_arg.add_argument("file", type=argparse.FileType('r'), help="The file of N-Puzzle")
	parser_arg.add_argument("-s", "--snail", action='store_true', help="The goal puzzle is snail matrix")
	parser_arg.add_argument("-m", "--matrix", action='store_true', help="The output is matrix")
	parser_arg.add_argument("-f", help="Heuristic function",
							choices=['manhattan', 'euclidean', 'hamming', 'linear'], default='manhattan')
	parser_arg.add_argument("-a", help="Algorithm choice",
							choices=['A_star', 'IDA', 'greedy', 'uniform'], default='A_star')
	args = parser_arg.parse_args()

	try:
		Arguments(args)
		with open(args.file.name) as file:
			lines = file.readlines()
		parser = Parser(lines, args)

		start_time = time.time()
		if args.IDA is True:
			ida_star = IDA_star(parser, args)
		else:
			a_star = A_star(parser, args)
		print("--- {:.3f} sec ---".format(time.time() - start_time))
		pass
	except (Exception, BaseException) as e:
		print(e)
		exit(1)
