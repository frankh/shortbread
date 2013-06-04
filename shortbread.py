import string
import itertools
from optparse import OptionParser

def shortbread(short, bread, word_list, letters, depth_first):
	lpaths = {}
	rpaths = {}

	def mutate_word(word, path, word_list):
		# For each letter in the word, replace it with
		# each valid letter and check if it's a word.
		for i, unused in enumerate(word):
			for letter in letters:
				new_word = word[:i] + letter + word[i+1:]
				if new_word in word_list:
					# If it is a word, remove it from the dictionary 
					# so we don't visit it twice.
					word_list.remove(new_word)
					yield new_word, path + [new_word]

	def words_gen(starting_word, word_list, depth_first):
		# defensive copy of word list
		word_list = set(word_list)
		word_list.remove(starting_word)

		new_words = iter([(starting_word, [starting_word])])

		# The function will return when new_words throws StopIteration
		# Loop forever until that happens.
		while True:
			next_word, path = new_words.next()
			
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

			yield next_word, path

	# Double ended search.
	for (lword, lpath), (rword, rpath) in \
	itertools.izip(words_gen(short, word_list, depth_first), 
				   words_gen(bread, word_list, depth_first)):
		# check if we have a common word.
		# If we do, reverse the right path (it started from the end)
		# and strip the common word.
		if lword in rpaths:
			return lpath + rpaths[lword][::-1][1:]
		if rword in lpaths:
			return lpaths[rword] + rpath[::-1][1:]

		lpaths[lword] = lpath
		rpaths[rword] = rpath

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

	words_content = open('words').read()
	word_list = set(word for word in words_content.split() 
		                          if len(word) == len(bread))

	print "path is", shortbread(short, bread, word_list, options.letters, options.depth_first)
