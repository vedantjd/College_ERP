#check string in
#in state A
def checkStateA(n):
	
	#if length of
	#string is one
	#print not accepted
	if(len(n)==1):
		print("string not accepted")
	else:
		if(n.count("a")+n.count("b")==len(n)):
			if(n[0]=='a' or n[0]=='b'):
				stateB(n[1:])
		else:
			print("string not accepted")	
			
def stateB(n):
	
	#here if length 
	#is less than 1 
	#printstring not accepted
	if(len(n)<1):
		print("string not accepted")
	else:
		
		#else pass string 
		#to state c
		stateC(n[1:])
		
		
def stateC(n):
	#here if length of string 
	#is greater than equal to zero
	#print accepted
	#else not accepted
	if (len(n)>=0):
		print("string accepted")
	else:
		print("string not accepted")
	
	
#take input 
n=input("Enter Input")
checkStateA(n)
