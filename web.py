from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
import aiml
from sementicNetwork import network
from search import game

kernel = aiml.Kernel()
kernel.learn("chatbot/udc.aiml")
graph = network()
g = game()


app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/graphPage")
def graphPage():
    return render_template("Graph.html")
@app.route("/get")
def get_bot_response():
    sentence = request.args.get('msg')
    if sentence.find("?") != -1:
        result = g.search(sentence)
        print(result)
        if len(result)==0:
            return "I don't know such person"
        print(len(result))
        if len(result)== 1:
            return "The person in question is "+str(result[0])
        else:
            reponse = "The people with this property are: "
            for r in result[:-1]:
                reponse = reponse +str(r)+", "
            print(reponse[-2])
            reponse = reponse +" and " + result[-1]
            return reponse
    add = kernel.getPredicate('add')
    print(add)
    if add == '1':
        graph.create(sentence)
    return kernel.respond(sentence)
if __name__ == "__main__":
    app.run()