# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: student <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/30 08:08:02 by student           #+#    #+#              #
#    Updated: 2020/12/30 08:09:20 by student          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from .utils.Color import Color
import numpy as np


class Parser:
	def __init__(self, lines: list, args):
		self.lines = lines
		self.line = []
		self.map = []
		self.size = None
		self.ft_parser()
		if args.snail is False:
			self.goal_1d, self.goal_2d = self.ft_goal()
		else:
			self.goal_1d, self.goal_2d = self.snail_goal()
		if not self.is_solvable():
			raise BaseException(f'{Color.RED}This puzzle is unsolvable{Color.END}')

	def ft_parser(self):
		if self.lines[-1][-1] != '\n':
			raise BaseException(f'{Color.WARNING}File must end to "\\n"{Color.END}')
		lines = [x.strip() for x in self.lines]
		lines = list(filter(None, lines))
		count_line = 0
		comment_line = 0
		index_line = 0
		n_rows = 0
		for line1 in lines:
			line = line1.split("#", maxsplit=1)[0].strip()
			if line == '':
				comment_line += 1
				continue
			if count_line == 0:
				if line.isdigit() is False or (int(line) == 0 or int(line) == 1):
					raise BaseException(f'{Color.WARNING}[ERROR]: N-puzzle size must be integer and > 1{Color.END}')
				self.size = int(line)
			else:
				n_rows += 1
				if n_rows > self.size:
					raise BaseException(f'{Color.WARNING}[ERROR]: n-puzzle size not equal count of lines{Color.END}')

				line = line.split()
				num_list = [int(x) for x in filter(lambda x: x.isdigit(), line)]
				if len(line) != len(num_list):
					raise BaseException(f'{Color.WARNING}[ERROR]: At line <{index_line}> '
										f'"{line1}" something wrong{Color.END}')
				if len(num_list) != self.size:
					raise BaseException(f'{Color.WARNING}[ERROR]: At line <{index_line}> "{line1}" '
										f'n-puzzle size not equal row size{Color.END}')

				self.line.extend(num_list)
			count_line += 1
			index_line = count_line + comment_line

		if n_rows != self.size:
			raise BaseException(f'{Color.WARNING}[ERROR]: n-puzzle size not equal count of lines{Color.END}')
		if len(set(self.line)) != len(self.line):
			raise BaseException(f'{Color.WARNING}[ERROR]: n-puzzle contains duplicates{Color.END}')
		if any(elem not in self.line for elem in range(self.size**2)):
			raise BaseException(f'{Color.WARNING}[ERROR]: n-puzzle contains bad digits{Color.END}')

		self.map = np.array(self.line).reshape(-1, self.size)

	def ft_goal(self):
		goal = list(range(1, self.size ** 2))
		goal.append(0)
		return goal, np.array(goal).reshape(-1, self.size)

	def snail_goal(self):
		lst = np.zeros((self.size, self.size), dtype=int)
		moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
		row = 0
		col = 0
		i = 1
		final = self.size ** 2
		size = self.size
		size -= 1
		while i is not final and size > 0:
			for move in moves:
				if i is final: break
				for _ in range(size):
					lst[row][col] = i
					row += move[0]
					col += move[1]
					i += 1
					if i is final: break
			row += 1
			col += 1
			size -= 2
		goal_1d = list(np.squeeze(lst.reshape(1, -1)))
		return goal_1d, lst

	def is_solvable(self):
		inversions = self.count_inversions()
		zero_index_i_goal, zero_index_j_goal = list(zip(*np.where(np.array(self.goal_2d) == 0)))[0]
		zero_index_i_puzzle, zero_index_j_puzzle = list(zip(*np.where(np.array(self.map) == 0)))[0]
		manhattan_dist = abs(zero_index_i_puzzle - zero_index_i_goal) + abs(zero_index_j_puzzle - zero_index_j_goal)
		if (manhattan_dist % 2 == 0 and inversions % 2 == 0) or \
				(manhattan_dist % 2 == 1 and inversions % 2 == 1):
			return True
		return False

	def count_inversions(self):
		res = 0
		for i in range(self.size ** 2 - 1):
			for j in range(i + 1, self.size ** 2):
				vi = self.line[i]
				vj = self.line[j]
				if self.goal_1d.index(vi) > self.goal_1d.index(vj):
					res += 1
		return res

	def __repr__(self):
		return f'.size {self.size} .elements {self.line}'
