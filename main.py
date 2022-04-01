#Bryan Herrera, Bryant Tran
#COMP_141 Group 15
#Project Phase 2.1

# expression ::=term { + term }
# term ::=factor { - factor }
# factor ::=piece { / piece }
# piece ::=element { * element }
# element ::=( expression ) | NUMBER | IDENTIFIER

import sys
import re

listCounter = 0

def printTree(tree, n, file):
  if tree == None:
    return 
  print(("\t" * n) + tree.data.tokenValue + " : " + tree.data.tokenType)
  file.write(("\t" * n) + tree.data.tokenValue + " : " + tree.data.tokenType + "\n")
  printTree(tree.left, n+1, file)
  printTree(tree.right, n+1, file)

#---------------------------------------------------------------#

def parseExpression(tokenList):
  global listCounter
  tree = parseTerm(tokenList)
  while(tokenList[listCounter].tokenValue == "+"):
    
    listCounter += 1
    tree = Node(tokenList[listCounter - 1], tree, None , parseTerm(tokenList))
  return tree

#---------------------------------------------------------------#

def parseTerm(tokenList):
  global listCounter
  tree = parseFactor(tokenList)
  while(tokenList[listCounter].tokenValue == "-"):
    
    listCounter += 1
    tree = Node(tokenList[listCounter - 1], tree, None , parseFactor(tokenList))
  return tree
  
#---------------------------------------------------------------#

def parseFactor(tokenList):
  global listCounter
  tree = parsePiece(tokenList)
  while(tokenList[listCounter].tokenValue == "/"):
    
    listCounter += 1
    tree = Node(tokenList[listCounter - 1], tree, None , parsePiece(tokenList))
  return tree
  
#---------------------------------------------------------------#

def parsePiece(tokenList):
  global listCounter
  tree = parseElement(tokenList)
  while(tokenList[listCounter].tokenValue == "*"):

    listCounter += 1
    tree = Node(tokenList[listCounter - 1], tree, None , parseElement(tokenList))
  return tree

#---------------------------------------------------------------#

def parseElement(tokenList):
  global listCounter
    
  if tokenList[listCounter].tokenType == "NUMBER":
    tree = Node(tokenList[listCounter] , None , None, None)
    listCounter += 1
    if(listCounter == len(tokenList)):
      listCounter -= 1
    return tree
  
  if tokenList[listCounter].tokenType == "IDENTIFIER":
    tree = Node(tokenList[listCounter] , None , None, None)
    listCounter += 1
    if(listCounter == len(tokenList)):
      listCounter -= 1
    return tree
  
  if tokenList[listCounter].tokenValue == "(":
    
    listCounter += 1
    tree = parseExpression(tokenList)
    if tokenList[listCounter].tokenValue == ")":
      return tree
    else :
      print("Error missing parentheses")
      quit()

#---------------------------------------------------------------#

class Node:
  def __init__(self, data, left, middle, right):
    self.data = data
    self.left = left
    self.middle = middle
    self.right = right

#---------------------------------------------------------------#

def split(word): #Function to split words into chars
  return [char for char in word]

#---------------------------------------------------------------#  
class Token:
  def __init__(self , tokenType , tokenValue):
    self.tokenType = tokenType
    self.tokenValue = tokenValue

  def __str__(self):
    return self.tokenType + " : " + self.tokenValue

#---------------------------------------------------------------#

def scanner(line):
  words = line.split()
  identifier = re.compile(r'^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*')
  number = re.compile(r'^[0-9]+')
  symbol = re.compile(r'\+|\-|\*|/|\(|\)')

  tokens = []
  for word in words:
    i = 0
    while(i < len(word)):
      longesttoken = None

      for j in range (i, len(word)):

        if identifier.fullmatch(word[i : j + 1]) != None:
          longesttoken = (Token("IDENTIFIER" , word[i : j + 1]))
      
        elif number.fullmatch(word[i : j + 1]) != None:
          longesttoken =(Token("NUMBER", word[i : j + 1]))
      
        elif symbol.fullmatch(word[i : j + 1]) != None:
          longesttoken =(Token("SYMBOL" , word[i : j + 1]))
          
        #tokens.append(Token("ERROR" , word))
      if longesttoken is None:
        tokens.append(Token("ERROR" , word[i]))
        return tokens
        
      i += len(longesttoken.tokenValue)
      tokens.append(longesttoken)
  return tokens

#---------------------------------------------------------------#
  
def main():
  
  if len(sys.argv) != 3:
    print("Error! Not enough arguements!")  #Error if there is not 3 sys arguements
    sys.exit(1)
    
  fileIn = sys.argv[1]  #Input file system arguement for command line
  fileOut = sys.argv[2] #Output file system arguement for command line

  fullTokenList = []
  
  fIn = open(fileIn, 'r')
  fOut = open(fileOut, 'w')
  #with open(fileIn, 'r') as fIn, open(fileOut, 'w') as fOut:  #Opens input file to read
  for line in fIn:  #Iterate thorugh input file line by line
    line = line.strip()
    print("Line: " + line)
    fOut.write("Line: " + line + "\n")  #Writes current line to be scanned to output file
    tokenList = scanner(line)
      
    for token in tokenList: #Iterates through tokens in current list
      fullTokenList.append(token)
      print(token) #prints token
      fOut.write(token.tokenType + " : " + token.tokenValue + "\n") #Writes token to output file
        
  fOut.write("\nAST:\n")
  print("\nAST:\n")
  tree = parseExpression(fullTokenList)
  printTree(tree, 0, fOut)

  fIn.close()
  fOut.close()

main()

#---------------------------------------------------------------#