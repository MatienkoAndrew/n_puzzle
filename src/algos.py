# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    algos.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: student <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/30 08:08:02 by student           #+#    #+#              #
#    Updated: 2020/12/30 08:09:20 by student          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from .utils.Color import Color
from collections import deque
from math import inf
import numpy as np


class Node:
	def __init__(self, node, action=None, parent=None, args=None, goal=None):
		self.map = node
		self.map_1d = tuple(self.map.reshape(1, -1)[0])
		self.action = action
		self.parent = parent
		self.child = []
		self.goal = goal
		if self.parent is not None:
			self.g_score = parent.g_score + 1
		else:
			self.g_score = 0
		if args.manhattan:
			self.h_score = self.manhattan
		elif args.euclidean:
			self.h_score = self.euclidean
		elif args.hamming:
			self.h_score = self.hamming
		elif args.linear:
			self.h_score = self.linear_conflict
		if args.greedy is False and args.uniform is False:
			self.f_score = self.g_score + self.h_score
		elif args.greedy is True:
			self.f_score = self.h_score
		elif args.uniform is True:
			self.f_score = self.g_score

	@property
	def manhattan(self):
		cur = self.map
		goal = self.goal
		sum_ = 0
		for x in np.squeeze(cur.reshape(1, -1)):
			if x != 0:
				cur_coord = list(zip(*np.where(cur == x)))[0]
				goal_coord = list(zip(*np.where(goal == x)))[0]
				sum_ += np.abs((cur_coord[0] - goal_coord[0])) + np.abs((cur_coord[1] - goal_coord[1]))
		return int(sum_)

	@property
	def euclidean(self):
		cur = self.map
		goal = self.goal
		sum_ = 0
		for x in np.squeeze(cur.reshape(1, -1)):
			if x != 0:
				cur_coord = list(zip(*np.where(cur == x)))[0]
				goal_coord = list(zip(*np.where(goal == x)))[0]
				sum_ += np.square(cur_coord[0] - goal_coord[0]) + np.square(cur_coord[1] - goal_coord[1])
		return int(sum_)

	@property
	def hamming(self):
		cur = self.map
		goal = self.goal
		sum_ = 0
		for x in np.squeeze(cur.reshape(1, -1)):
			if x != 0:
				cur_coord = list(zip(*np.where(cur == x)))[0]
				goal_coord = list(zip(*np.where(goal == x)))[0]
				sum_ += 1 if cur_coord != goal_coord else 0
		return int(sum_)

	@property
	def linear_conflict(self):
		def count_conflicts(map_row, goal_row, size, ans=0):
			counts = [0 for x in range(size)]
			for i, tile_1 in enumerate(map_row):
				if tile_1 in goal_row and tile_1 != 0:
					for j, tile_2 in enumerate(map_row):
						if tile_2 in goal_row and tile_2 != 0:
							if tile_1 != tile_2:
								if list(goal_row).index(tile_1) > list(goal_row).index(tile_2) and i < j:
									counts[i] += 1
								if list(goal_row).index(tile_1) < list(goal_row).index(tile_2) and i > j:
									counts[i] += 1
			if max(counts) == 0:
				return ans * 2
			else:
				idx = counts.index(max(counts))
				map_row[idx] = -1
				ans += 1
				return count_conflicts(map_row, goal_row, size, ans)

		manh_dist = self.manhattan
		map_rows = self.map.copy()
		map_columns = self.map.T.copy()
		goal_rows = self.goal.copy()
		goal_columns = self.goal.T.copy()

		size = len(map_rows)
		sum_conflict = 0
		for i in range(size):
			sum_conflict += count_conflicts(map_rows[i], goal_rows[i], size)
		for i in range(size):
			sum_conflict += count_conflicts(map_columns[i], goal_columns[i], size)
		return manh_dist + sum_conflict

	@property
	def solved(self):
		return list(self.map_1d) == list(np.squeeze(self.goal.reshape(1, -1)))

	@property
	def path(self):
		node = self
		p = []
		while node:
			p.append(node)
			node = node.parent
		p.reverse()
		return p

	def __repr__(self):
		return f'{self.map_1d} .action: {self.action} .g:{self.g_score} .h:{self.h_score} .f: {self.f_score}'


class A_star:
	def __init__(self, puzzle, args):
		self.size = puzzle.size
		self.start = puzzle.map
		self.goal = puzzle.goal_2d
		self.args = args
		self.node = Node(self.start, args=self.args, goal=self.goal)
		self.start_node = self.node
		self.path = []
		self.space = 0
		self.time = 0
		self.ft_algos()
		self.print_path()

	def ft_algos(self):
		openset = set()
		closeset = set()
		queue = deque([self.node])
		openset.add(tuple(queue[0].map_1d))
		while queue:
			queue = deque(sorted(queue, key=lambda node: node.f_score))
			node = queue.popleft()
			self.node = node
			if node.solved:
				self.path = node.path
				self.space = len(openset)
				self.time = len(closeset)
				return
			closeset.add(node.map_1d)
			for move, action in self.actions():
				child = Node(move, action, node, args=self.args, goal=self.goal)
				if child.map_1d in closeset:
					continue
				if child.map_1d not in openset:
					queue.appendleft(child)
					openset.add(child.map_1d)
					self.node.child.append(child)
		raise BaseException(f"{Color.RED}This puzzle is unsolvable{Color.END}")

	def actions(self):
		moves = []
		i, j = list(zip(*np.where(self.node.map == 0)))[0]
		directions = {'R': (i, j + 1),
					  'L': (i, j - 1),
					  'D': (i + 1, j),
					  'U': (i - 1, j)}
		for action, (k, l) in directions.items():
			if (0 <= k < self.size) and (0 <= l < self.size):
				move = self.create_move((i, j), (k, l)), action
				moves.append(move)
		return moves

	def create_move(self, from_, to):
		puzzle_2d_copy = self.node.map.copy()
		i, j = from_
		k, l = to
		puzzle_2d_copy[i][j], puzzle_2d_copy[k][l] = puzzle_2d_copy[k][l], puzzle_2d_copy[i][j]
		return puzzle_2d_copy

	def print_path(self):
		for track in self.path:
			if self.args.matrix:
				print(track.map, end="\n\n")
			else:
				print(track.map_1d)
		print("Total number of steps:", self.path.__len__() - 1)
		print("Space complexity: {} nodes in memory".format(self.space))
		print("Time complexity: {} evaluated nodes".format(self.time))


class IDA_star(A_star):
	def ft_algos(self):
		def search(queue: deque, g: int, bound: int, evaluated: int):
			evaluated += 1
			node = queue[0]
			self.node = node
			f = g + node.h_score
			if f > bound:
				return f, evaluated
			if node.solved:
				return node, evaluated
			min_ = inf
			for move, action in self.actions():
				child = Node(move, action, node, args=self.args, goal=self.goal)
				if child.map_1d not in [node.map_1d for node in queue]:
					queue.appendleft(child)
					t, evaluated = search(queue, g + 1, bound, evaluated)
					if isinstance(t, Node):
						return t, evaluated
					if t < min_:
						min_ = t
					queue.popleft()
			return min_, evaluated


		queue = deque([self.node])
		bound = self.node.h_score
		evaluated = 0
		while 1:
			t, evaluated = search(queue, 0, bound, evaluated)
			if isinstance(t, Node):
				self.path = t.path
				self.space = len(queue)
				self.time = evaluated
				return
			if t == inf:
				raise BaseException(f'This puzzle is unsolvable')
			bound = t





