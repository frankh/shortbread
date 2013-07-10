import string
import itertools
from optparse import OptionParser

def shortbread(short, bread, word_list, letters, depth_first):
	lpaths = {}
	rpaths = {}

	def mutate_word(word, path, word_list):
		# For each letter in the word, replace it with
		# each valid letter and check if it's a word.
		for i in range(len(word)):
			for letter in letters:
				new_word = word[:i] + letter + word[i+1:]
				if new_word in word_list:
					# If it is a word, remove it from the dictionary 
					# so we don't visit it twice.
					word_list.remove(new_word)
					yield new_word, path + [new_word]

	def words_gen(starting_word, word_list, depth_first, results_queue):
		# defensive copy of word list
		word_list = set(word_list)
		word_list.remove(starting_word)

		new_words = iter([(starting_word, [starting_word])])

		# The function will return when new_words throws StopIteration
		while True:
			try:
				next_word, path = new_words.next()
			except StopIteration:
				results_queue.close()
				return

			if depth_first:
				new_words = itertools.chain(
					mutate_word(next_word, path, word_list), 
					new_words
				)
			else:
				new_words = itertools.chain(
					new_words, 
					mutate_word(next_word, path, word_list)
				)

			results_queue.put((next_word, path), False)

	from multiprocessing import Process, Queue
	start_results_queue = Queue()
	end_results_queue = Queue()
	start_proc = Process(target=words_gen, args=(short, word_list, depth_first, start_results_queue))
	end_proc = Process(target=words_gen, args=(bread, word_list, depth_first, end_results_queue))

	start_proc.start()
	end_proc.start()

	while start_proc.is_alive() and end_proc.is_alive():
		(lword, lpath), (rword, rpath) = start_results_queue.get(), end_results_queue.get()

		if lword in rpaths:
			start_proc.terminate()
			end_proc.terminate()
			return lpath + rpaths[lword][::-1][1:]
		if rword in lpaths:
			start_proc.terminate()
			end_proc.terminate()
			return lpaths[rword] + rpath[::-1][1:]

		lpaths[lword] = lpath
		rpaths[rword] = rpath

	start_proc.terminate()
	end_proc.terminate()

if __name__ == '__main__':
	"""
	Usage: shortbread.py [options] short bread

	Options:
	  -h, --help            show this help message and exit
	  -l LETTERS, --letters=LETTERS
							valid letters - default is abcdef...xyz
	  -d                    use depth first search
	  -b                    use breadth first search. This is the default

	e.g.
		shortbread.py short bread

		shortbread.py cheese steaks

		shortbread.py frank\'s farmers -l abcdefghijklmnopqrstuvwxyz\'
	"""
	parser = OptionParser(usage='Usage: %prog [options] short bread') 
	parser.add_option(
		"-l",  "--letters", 
		dest = "letters",
		help = "valid letters - default is abcdef...xyz",
		default = string.ascii_lowercase)

	parser.add_option(
		"-d", 
		action = "store_true", 
		dest   = "depth_first",
		help   = "use depth first search")
	parser.add_option(
		"-p", "--precache", 
		action = "store_true", 
		dest   = "precache",
		help   = "precache adjacent words graph")
	parser.add_option(
		"-b", 
		action = "store_false",
		dest   = "depth_first", 
		help   = "use breadth first search. This is the default",
		default= False)
	(options, args) = parser.parse_args()

	try:
		short, bread = args
	except ValueError:
		parser.print_help()
		exit(0)

	assert(len(short) == len(bread)), "Both words must be the same length"
	word_len = len(short)

	words_content = open('/usr/share/dict/british-english').read()
	word_list = list(w for w in words_content.split() if len(w) == word_len)

	print "path is", shortbread(short, bread, word_list, options.letters, options.depth_first)