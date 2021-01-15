# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Arguments.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: student <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/30 08:08:02 by student           #+#    #+#              #
#    Updated: 2020/12/30 08:09:20 by student          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Arguments:
	def __init__(self, args):
		args.manhattan = False
		args.euclidean = False
		args.hamming = False
		args.linear = False
		if args.f == 'manhattan':
			args.manhattan = True
		elif args.f == 'euclidean':
			args.euclidean = True
		elif args.f == 'hamming':
			args.hamming = True
		elif args.f == 'linear':
			args.linear = True

		args.greedy = False
		args.uniform = False
		args.IDA = False
		if args.a == 'greedy':
			args.greedy = True
		elif args.a == 'uniform':
			args.uniform = True
		elif args.a == 'IDA':
			args.IDA = True

