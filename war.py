import random 

symbols=[2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
suits=["Clubs","Spades","Hearts","Diamonds"]


class Rank:
	
	__symbol=0

	def __init__(self,symbol):
		self.__symbol=symbol

	def __eq__(self,other):
		return self.__symbol==other.__symbol

	def __lt__(self,other):
		return symbols.index(self.__symbol)<symbols.index(other.__symbol)

	def __gt__(self,other):
		return symbols.index(self.__symbol)>symbols.index(other.__symbol)

	def __str__(self):
		if 1<self.__symbol<11:
			return str(self.__symbol)
		if self.__symbol=="J":
			return "Jack"
		if self.__symbol=="Q":
			return "Queen"
		if self.__symbol=="K":
			return "King"
		if self.__symbol=="A":
			return "Ace"

	def getSymbol(self):
		return self.__symbol

class Card:

	__suit=0
	__symbol=0


	def __init__(self,suit,symbol):
		self.__suit=suit
		self.__rank=Rank(symbol)

	def __eq__(self,other):
		return self.__rank==other.__rank

	def __lt__(self,other):
		return self.__rank<other.__rank

	def __gt__(self,other):
		return self.__rank>other.__rank

	def __str__(self):
		return str(self.__rank)+" of "+self.__suit

	def __hash__(self):
		return symbols.index(self.__rank.getSymbol())*100+suits.index(self.__suit)

def findMaxCardIndex(arr):
	res=[]
	maxCard=max(arr)
	for i in range(len(arr)):
		if arr[i]==maxCard:
			res.append(i)
	return res


class Deck:
	__deck=[]
	__number=52

	def __init__(self,number):
		self.__number=number
		for symbol in symbols:
			for suit in suits:
				self.__deck.append(Card(suit,symbol))
		
		# would use shuffle() here but no forward-declaration in python :(
		self.__deck=self.__deck[:52] #  fix for weird bug here - TODO find out what's wrong
		random.shuffle(self.__deck)
		self.__deck=self.__deck[:self.__number]
	
	def __str__(self):
		arr=[]
		for card in self.__deck:
			arr.append(str(card))
		return "\n".join(arr)

	def shuffle(self):
		random.shuffle(self.__deck)

	def __len__(self):
		return len(self.__deck)

	def __getitem__(self, index):
		if self.__number<index+1:
			return False
		return self.__deck[index]

	def __delitem__(self,index):
		del self.__deck[index]

	def addCard(self,card):
		self.__deck.insert(0,card)
		self.__number+=1

	def addCardLast(self,card):
		self.__deck.append(card)
		self.__number+=1 

	def empty(self):
		self.__deck=[]
		self.__number=0

	def pop(self):
		self.__number-=1
		return self.__deck.pop()

	def __contains__(self, card):
		return card in self.__deck

	def getBiggestCard(self):
		self.__number-=1
		return max(self.__deck)


class Player:

	__deck=0
	__number=0
	__active=True
	__name=""

	def __init__(self,name,number):
		self.__name=name
		self.__number=number
		self.__deck=Deck(self.__number)

	def view(self):
		print("- - - - -")
		print(self.__name)
		print(str(self.__number)+" cards left")
		print(self.__deck)
		print("- - - - -")

	def getCardNumber(self):
		return self.__number

	def getLastCard(self):
		self.__number-=1
		return self.__deck.pop()

	def deactivate(self):
		self.__active=False

	def activate(self):
		self.__active=True

	def addCard(self,card):
		self.__number+=1
		self.__deck.addCard(card)

	def giveNewDeck(self,number,gameDeck):
		self.__number=0
		self.__deck.empty()

		for i in range(number-1,-1,-1):
			self.addCard(gameDeck[i])
		for i in range(number-1,-1,-1):
			del gameDeck[i]


	def isActive(self):
		return self.__active

	def getName(self):
		return self.__name

	def __hash__(self):
		return self.__number+len(self.__name) #TODO FIX

	def getBiggestCard(self):
		self.__number-=1
		return self.__deck.getBiggestCard()


class Game:
	__playerCount=1
	__active=True
	__players=[]
	__cardNumber=0
	__cardsOnTable={}
	__winner=0
	

	def __init__(self,cardNumber,players):
		self.__cardNumber=cardNumber
		self.__players=players
		self.__playerCount=len(self.__players)
		self.__deck=Deck(self.__cardNumber)
		#self.__deck=Deck(52)
		for player in self.__players:
			player.activate()
			player.giveNewDeck(self.__cardNumber//self.__playerCount,self.__deck)

		#for player in self.__players:
			#player.view()

	def getPlayerIndexByName(self,name):
		for i in range (len(self.__players)):
			if self.__players[i].getName()==name:
				return i

	def newHand2(self):
		#self.__cardsOnTable=[Card("Spades",1)]*self.__playerCount
		self.__cardsOnTable={}
		for player in self.__players:
			if player.isActive():
				self.__cardsOnTable[player.getLastCard()]=player

		for card in self.__cardsOnTable.keys():
			##print(card)
			self.__cardsOnTable[max(self.__cardsOnTable.keys())].addCard(card)
		##print(self.__cardsOnTable[max(self.__cardsOnTable.keys())].getName())
		for player in self.__players:
			if player.isActive():
				if player.getCardNumber()==0:
					player.deactivate()
				if player.getCardNumber()==(self.__cardNumber//self.__playerCount)*self.__playerCount:
					self.__active=False
					self.__winner=player
				#print (player.getName()+" "+str(player.getCardNumber()))
		

	def newHand(self):
		self.__cardsOnTable={}
		for player in self.__players:
			if player.isActive():
				if player.getCardNumber()>3:
					self.__cardsOnTable[player.getName()]=player.getLastCard()
				else:
					self.__cardsOnTable[player.getName()]=player.getBiggestCard()


		cardsArray=list(self.__cardsOnTable.values())
		indices=findMaxCardIndex(cardsArray)

		if len(indices)==1:
			for player in self.__cardsOnTable.keys():
				if self.__cardsOnTable[player]==cardsArray[indices[0]]:
					for card in cardsArray:
						self.__players[self.getPlayerIndexByName(player)].addCard(card)
			
		else:
			#print ("BEGINNING WAR")
			lastCardPlayed=0
			flag=1
			while flag:
				newCardsArray=[]
				#starting war between the equal cards
				for player in self.__cardsOnTable.keys():
					if isinstance(self.__cardsOnTable[player],Card):
						newDeck=Deck(0)
						newDeck.addCard(self.__cardsOnTable[player])
						self.__cardsOnTable[player]=newDeck
				minimum=3
				for player in self.__cardsOnTable.keys():	
					cardsOnTable=len(self.__cardsOnTable[player])
					if cardsOnTable>lastCardPlayed and self.__players[self.getPlayerIndexByName(player)].getCardNumber()<minimum:
						minimum=self.__players[self.getPlayerIndexByName(player)].getCardNumber()		
				
				if minimum==0:
					#print("min is zero")
					for player in self.__cardsOnTable.keys():
						for i in range(len(self.__cardsOnTable[player])):
							self.__players[self.getPlayerIndexByName(player)].addCard(self.__cardsOnTable[player][i])
					flag=0
					
				else:
					#print("min is " + str(minimum))
					cardsToGive=minimum
					#print("Last card played is " +str(lastCardPlayed))
					for player in self.__cardsOnTable.keys():
						if len(self.__cardsOnTable[player])>lastCardPlayed:
							if cardsArray.index(self.__cardsOnTable[player][lastCardPlayed]) in indices:
								if self.__players[self.getPlayerIndexByName(player)].getCardNumber()>cardsToGive-1:
									#print(player+ " gives "+str(cardsToGive)+" cards: ")
									for i in range(cardsToGive):
										card=self.__players[self.getPlayerIndexByName(player)].getLastCard()
										#print(card)
										self.__cardsOnTable[player].addCardLast(card)
										if i==cardsToGive-1:

											newCardsArray.append(card)

					lastCardPlayed+=cardsToGive
					#print(newCardsArray)
					indices=findMaxCardIndex(newCardsArray)
					#print(indices)
					if len(indices)==1:
						#print("new index:")
						#print(newCardsArray[indices[0]])
						for player in self.__cardsOnTable.keys():
							if len(self.__cardsOnTable[player])>=lastCardPlayed+1:
								if newCardsArray[indices[0]] == self.__cardsOnTable[player][lastCardPlayed]:
									#print(player + "'s deck:")
									#print(self.__cardsOnTable[player])
									for playerDeck in self.__cardsOnTable.values():
										for i in range(len(playerDeck)):
											self.__players[self.getPlayerIndexByName(player)].addCard(playerDeck[i])
						flag=0
						#print("END OF WAR")
					else:
						cardsArray=newCardsArray

				
		cardSum=0
		for player in self.__players:
			if player.isActive():
				cardSum+=player.getCardNumber()
				if player.getCardNumber()==0:
					player.deactivate()
				if player.getCardNumber()==(self.__cardNumber//self.__playerCount)*self.__playerCount:
					self.__active=False
					self.__winner=player
				#print (player.getName()+" "+str(player.getCardNumber()))
		if cardSum!=51:
			return "Very BAD"
			self.__active=False
	def playGame(self):
		iterations=0
		while(self.__active):
			self.newHand()
			if iterations<5000:
				iterations+=1
			else:
				self.__active=False
				#print("TOO MUCH TIME ALL THE PLAYERS DIED")
		if iterations!=5000:
			#print("Game ended in "+ str(iterations)+ " iterations.")
			return iterations
		else:
			return -1
		#print("Winner is "+self.__winner.getName())





bisi1 = Card("Hearts","J")
bisi2 = Card("Hearts",3)
bisi3 = Card("Hearts",5)
##print(max([bisi1,bisi2,bisi3]))

#bisi2 = Deck(52)
##print(bisi2)

bistra1 = Player("Bistra1",6)
bistra2 = Player("Bistra2",6)
bistra3 = Player("Bistra3",6)
sums=0
fails=0
games=600
minIter=4800
maxIter=0
for i in range(games):
	newg=Game(52,[bistra1,bistra2,bistra3])
	res=newg.playGame()
	if res==-1:
		fails+=1
	else:
		sums+=res
		if minIter>res:
			minIter=res
		if maxIter<res:
			maxIter=res
print("Min hands: "+str(minIter))
print("Max hands: "+str(maxIter))
print(str(fails) + " failed games")
print("RESULT: "+str(sums/(games-fails)))
#i want to implement a graph of the results online
