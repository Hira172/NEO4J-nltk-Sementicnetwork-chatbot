import aiml
from sementicNetwork import network
from search import game
kernel = aiml.Kernel()
kernel.learn("chatbot/udc.aiml")
graph = network()
g = game()
while True:
    sentence = input("You>> ")

    res = kernel.getPredicate('res')
    add = kernel.getPredicate('add')
    game = kernel.getPredicate('game')
    if add == '1' and sentence != "I want to play now" :
        graph.create(sentence) 
    if game == '1':
        result = g.search(sentence)
        if len(result)>=1:
            kernel.setPredicate("gameres", "1")
            kernel.setPredicate("res", str(result[0]))
        else:
            kernel.setPredicate("gameres", "0")
    print("Flora>>", kernel.respond(sentence))