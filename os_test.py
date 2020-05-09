import os 
os.system("echo \"Hello World\"")
#val = os.system("dir ")
#print(val)
class Ptest:
	def __init__(self):
		self.word="ec"
class TestHandle(Ptest):
	def test(self,word):
		print(self.word+word)

test=TestHandle()
test.test('ok')