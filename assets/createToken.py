from random import randint

class createToken():
  def __init__(self):
    self.tokenList = []
    self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    
  def create(self, size):
    token = self.generate(size)
    isNew = self.verifier(token)
    while True:
      if isNew:
        break
      else:
        token = self.generate(size)
        isNew = self.verifier(token)
    
    self.tokenList.append(token)
    return token
      
  def generate(self, size):
    size = int(size/2)
    token = ""
    for _ in range(0, size):
      token += str(randint(0, 9))
      token += self.alpha[randint(0, 51)]
    return token
  

  def verifier(self, token):
    if token not in self.tokenList:
      return True
    else:
      return False
