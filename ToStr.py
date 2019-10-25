#	converts things to strings -- even tuples, lists, and dicts
def tostr(x):
	t = type(x)
	if t == dict:
		return '{' + ", ".join( \
			list(map( lambda k,d=x: tostr(k)+": "+tostr(d[k]), \
			list(x.keys()) ))) + "}"
		

	if t == list:
		return '[' + ", ".join( \
			[tostr(i) for i in x], \
			) + "]"

	return str(x)
