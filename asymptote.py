# Python module to feed Asymptote with commands
# (modified from gnuplot.py)
from subprocess import *
class asy:
	closed = False

	def __init__(self):
		self.session = Popen(['asy','-quiet','-inpipe=0','-outpipe=2'],stdin=PIPE)
		#self.help()
	def send(self, cmd):
		self.session.stdin.write((cmd+'\n').encode())
		self.session.stdin.flush()
	def size(self, size):
		self.send("size(%d);" % size)
	def draw(self, str):
		self.send("draw(%s);" % str)
	def fill(self, str):
		self.send("fill(%s);" % str)
	def clip(self, str):
		self.send("clip(%s);" % str)
	def label(self, str):
		self.send("label(%s);" % str)
	def shipout(self, str):
		self.send("shipout(\"%s\");" % str)
	def erase(self):
		self.send("erase();")
	def help(self):
		print ("Asymptote session is open.  Available methods are:")
		print ("    help(), size(int), draw(str), fill(str), clip(str), label(str), shipout(str), send(str), erase()")

	def finish(self):
		print ("closing Asymptote session...")
		self.send('quit');
		self.session.stdin.close();
		self.session.wait()
		self.closed = True

	def __del__(self):
		if self.closed == False:
			print ("closing Asymptote session...")
			self.send('quit');
			self.session.stdin.close();
			self.session.wait()
		




# if __name__=="__main__":
# 	g = asy()
# 	g.size(200)
# 	g.draw("unitcircle")
# 	g.send("draw(unitsquare)")
# 	g.fill("unitsquare, blue")
# 	g.clip("unitcircle")
# 	g.label("\"$O$\", (0,0), SW")
# 	if sys.version_info >= (3, 0):
# 		input ("press ENTER to continue")
# 	else:
# 		raw_input ("press ENTER to continue")
# 	g.erase()
# 	del g
