#Bryan Herrera, Bryant Tran
#COMP_141 Group 15
#Project Phase 3.1
#Evaluator for expressions

import sys
import re

listCounter = 0
memory = {}
  
  
def parseStatement(tokenList):
  global listCounter
  
  tree = parseBaseStatement(tokenList)

  if(listCounter == len(tokenList)):
    return tree
  
  while(tokenList[listCounter].tokenValue == ";"):
    listCounter += 1
    tree = Node(tokenList[listCounter - 1], tree, None , parseBaseStatement(tokenList))
    if(listCounter == len(tokenList)):
      break
  return tree  

#---------------------------------------------------------------#

def parseBaseStatement(tokenList):
  global listCounter
  
  if(tokenList[listCounter].tokenValue == "if"):
    return parseIfStatement(tokenList)
    
  elif(tokenList[listCounter].tokenValue == "while"):
    return parseWhileStatement(tokenList)
    
  elif(tokenList[listCounter].tokenValue == "skip"):
    listCounter += 1
    tree = Node(tokenList[listCounter - 1], None, None , None)
    return tree
    
  elif(tokenList[listCounter].tokenType == "IDENTIFIER"):
    tree = parseAssignment(tokenList)
    return tree
    
  else:
    print("ERROR 1! " + str(tokenList[listCounter].tokenValue) +  " Does Not Match Grammar!\n")
    quit()
    
#---------------------------------------------------------------#

def parseAssignment(tokenList):
  global listCounter
  
  tree = parseElement(tokenList)
    
  if(tokenList[listCounter].tokenValue == ":="):
    currentToken = listCounter
    listCounter += 1
    expression = parseExpression(tokenList)
    tree = Node(tokenList[currentToken], tree, None, expression)
    return tree

#---------------------------------------------------------------#

def parseIfStatement(tokenList):
  global listCounter
  
  currentToken = listCounter
  listCounter += 1
  tree = parseExpression(tokenList)
  
  if(tokenList[listCounter].tokenValue == "then"):
    listCounter += 1
    tree2 = parseStatement(tokenList)

    if(tokenList[listCounter].tokenValue == "else"):
      listCounter += 1
      tree3 = parseStatement(tokenList)

      if(tokenList[listCounter].tokenValue == "endif"):
        listCounter += 1
        return Node(tokenList[currentToken], tree, tree2, tree3)
        
  else:
    print("ERROR 2! " + str(tokenList[listCounter].tokenValue) +  " Does Not Match Grammar!\n")
    quit()
    
#---------------------------------------------------------------#

def parseWhileStatement(tokenList):
  global listCounter
  
  currentToken = listCounter
  listCounter += 1
  tree = parseExpression(tokenList)
  
  if(tokenList[listCounter].tokenValue == "do"):
    listCounter += 1
    tree2 = parseStatement(tokenList)

    if(tokenList[listCounter].tokenValue == "endwhile"):
      listCounter += 1
    return Node(tokenList[currentToken], tree, None, tree2)
    
  else:
    print("ERROR 3! " + str(tokenList[listCounter].tokenValue) +  " Does Not Match Grammar!\n")
    quit()

  
#---------------------------------------------------------------#

def isLeaf (node):
  return node.left is None and node.right is None

#---------------------------------------------------------------#

def evaluateAssignment(node):
  key = node.left.data.tokenValue
  value = evaluateExpression(node.right)
  memory[key] = value
  
def evaluateStatement(node):
  if node.data.tokenValue == ";":
    evaluateStatement(node.left)
    evaluateStatement(node.right)
  elif node.data.tokenValue == ":=":
    evaluateAssignment(node)
  elif node.data.tokenValue == "if":
    evaluateIf(node)
  elif node.data.tokenValue == "while":
    evaluateWhile(node)
  elif node.data.tokenValue == "skip":
    return
  else:
    print("Error statement")

def evaluateWhile(node):
  v = evaluateExpression(node.left)
  while v != 0:
    evaluateStatement(node.right)
    v = evaluateExpression(node.left)
  
def evaluateIf(node):
  if evaluateExpression(node.left) != 0:
    evaluateStatement(node.middle)
  else:
    evaluateStatement(node.right)
    
  
def evaluateExpression (node):
  if node is None:
    return 0
  if node.data.tokenType == "IDENTIFIER":
    if node.data.tokenValue not in memory:
      print("Error missing parentheses")
      quit()
    return memory[node.data.tokenValue]
  if node.data.tokenType == "NUMBER":
    return int(node.data.tokenValue)    
  left = evaluateExpression(node.left)
  right = evaluateExpression(node.right)
  return solve(node.data, left , right)

#---------------------------------------------------------------#

def solve(op, left , right):
  if op.tokenValue == '+':
    return left + right
  if op.tokenValue == '-':
    return max(0, left - right)
  if op.tokenValue == '*':
    return left * right
  if op.tokenValue == '/':
    return left // right
  
#---------------------------------------------------------------#

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
    if(listCounter < len(tokenList) - 1):
      listCounter += 1
    return tree
  
  if tokenList[listCounter].tokenType == "IDENTIFIER":
    tree = Node(tokenList[listCounter] , None , None, None)
    if(listCounter < len(tokenList) - 1):
      listCounter += 1
    return tree
  
  if tokenList[listCounter].tokenValue == "(":
    
    listCounter += 1
    tree = parseExpression(tokenList)
    if tokenList[listCounter].tokenValue == ")":
      if(listCounter < len(tokenList) - 1):
        listCounter += 1
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
  symbol = re.compile(r'\+|\-|\*|/|\(|\)|:=|;')
  keyword = re.compile(r'if|then|else|endif|while|do|endwhile|skip')

  tokens = []
  for word in words:
    i = 0
    while(i < len(word)):
      longesttoken = None

      for j in range (i, len(word)):

        if keyword.fullmatch(word[i : j + 1]) != None:
          longesttoken = (Token("KEYWORD", word[i : j + 1]))

        elif identifier.fullmatch(word[i : j + 1]) != None:
          longesttoken = (Token("IDENTIFIER" , word[i : j + 1]))
      
        elif number.fullmatch(word[i : j + 1]) != None:
          longesttoken =(Token("NUMBER", word[i : j + 1]))
      
        elif symbol.fullmatch(word[i : j + 1]) != None:
          longesttoken =(Token("SYMBOL" , word[i : j + 1]))
          
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
  with open(fileIn, 'r') as fIn, open(fileOut, 'w') as fOut:  #Opens input file to read
    for line in fIn:  #Iterate thorugh input file line by line
      line = line.strip()
      print("Line: " + line)
      fOut.write("Line: " + line + "\n")  #Writes current line to be scanned to output file
    
      tokenList = scanner(line)  
      for token in tokenList: #Iterates through tokens in current list
        fullTokenList.append(token)
        print(token) #prints token
        fOut.write(token.tokenType + " : " + token.tokenValue + "\n") #Writes token to output file

      fOut.write("\n")
      print("\n")
        
    fOut.write("\nAST:\n")
    print("\nAST:\n")
    tree = parseStatement(fullTokenList)
    printTree(tree, 0, fOut)
    evaluateStatement(tree)
    print("\nOutput: \n")
    fOut.write("\nOutput\n")
    
    for key, value in memory.items():
      print(str(key) + "=" + str(value) + "\n")
      fOut.write(str(key) + "=" + str(value) + "\n")
  fIn.close()
  fOut.close()

main()

#---------------------------------------------------------------#
