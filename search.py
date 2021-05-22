from py2neo import Graph, Node, Relationship
import numpy as np
from nlp_part import nlp_part


class game:
    def __init__(self):
        self.nlp = nlp_part()
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
        self.res = np.array([])

    def search(self, sentence, game=False):
        nouns, verb, adjective, count,In,CC = self.nlp.processData(sentence)
        if CC != []:
            w1, t1 = nouns[0]
            i = 1
            # print(len(nouns))
            r =[]
            while i < len(nouns):
                w2, t2 = nouns[i]
                cypher = """
                                    MATCH (n:Person)
                                    MATCH (m:""" + t2 + """{name: '""" + str(w2) + """'})  
                """
                if verb !=[]:
                    cypher = cypher +"""MATCH (n)-[:""" + str(verb[0]) + """]->(m)  RETURN n.name"""
                else:
                    cypher = cypher + """MATCH (n)-[:""" + str(In[0]) + """]->(m)  RETURN n.name"""
                print(cypher)
                temp = self.graph.run(cypher).data()  # return list of dictionaries
                temp = [d['n.name'] for d in temp]
                print(temp)
                if r == []:
                    r = temp
                else:
                    r = set(r).intersection(temp)
                i=i+1
            return r
        else:
            if len(verb) > 1:
                verb[0] = verb[-1]
            if verb ==[] and In!=[]:
                w2, t2 = nouns[0]
                cypher = """
                        MATCH (n:Person)
                        MATCH (m:""" + t2 + """{name: '""" + str(w2) + """'})
                        MATCH (n)-[:""" + str(In[0]) + """]->(m) 
                        RETURN n.name
                    """
            else:
                if In != [] and len(nouns) == 2:
                    w2, t2 = nouns[0]
                    w3, t3 = nouns[1]
                    cypher = \
                        """
                        MATCH (n:Person)
                        MATCH (m:"""+t2+""" {name: '""" + str(w2) + """'})
                        MATCH (o:"""+t3+""" {name: '""" + str(w3) + """'})
                        MATCH (n)-[:""" + verb[0] + """]->(m) 
                        MATCH (m)-[:""" + In[0] + """]->(o) 
                        RETURN n.name
                        """
                else:
                    if adjective == [] and count == 0 and len(nouns)==1:
                        w2, t2 = nouns[0]
                        cypher = """
                                    MATCH (n:Person)
                                    MATCH (m:"""+t2+"""{name: '"""+str(w2)+"""'})
                                    MATCH (n)-[:"""+verb[0]+"""]->(m) 
                                    RETURN n.name
                                """
                    else:
                        if len(nouns) ==1 and len(verb) == 1 and len(adjective)==1:
                            w1, t1 = nouns[0]
                            a1,at1 = adjective[0]
                            cypher = """
                                    MATCH (n:Person)
                                    MATCH (m:""" + str(at1) + """ {name: '""" + str(a1) + """'})
                                    MATCH (n)-[:""" + verb[0] + """]->(m) 
                                    RETURN n.name
                                """
                        else:
                            if len(nouns)==1:
                                w2, t2 = nouns[0]
                                if adjective != []:
                                    a1, at1 = adjective[0]
                                else:
                                    a1, at1 = count
                                if len(verb) >1:
                                    cypher = """
                                            MATCH (n:Person)
                                            MATCH (m:"""+str(t2)+""" {name: '"""+str(w2)+""" '})
                                            MATCH (o:"""+str(at1)+""" {name: '"""+str(a1)+""" '})
                                            MATCH (n)-[:"""+verb[1]+"""]->(m) 
                                            MATCH (m)-[:"""+verb[0]+"""]->(o) 
                                            RETURN n.name
                                        """
                                else:
                                    if len(In) ==1:
                                        cypher = """
                                                MATCH (n:Person)
                                                MATCH (m:""" + str(t2) + """ {name: '""" + str(w2) + """ '})
                                                MATCH (o:""" + str(at1) + """ {name: '""" + str(a1) + """ '})
                                                MATCH (n)-[:""" + verb[0] + """]->(m) 
                                                MATCH (m)-[:""" + In[0] + """]->(o) 
                                                RETURN n.name
                                            """
                                    else:
                                        cypher = """
                                                MATCH (n:Person)
                                                MATCH (m:""" + str(t2) + """ {name: '""" + str(w2) + """ '})
                                                MATCH (o:""" + str(at1) + """ {name: '""" + str(a1) + """ '})
                                                MATCH (n)-[:""" + verb[0] + """]->(m) 
                                                MATCH (m)-[:is]->(o) 
                                                RETURN n.name
                                            """


                            else:
                                if adjective !=[]:
                                    a1, at1 = adjective[0]
                                else:
                                    a1, at1 = count
                                cypher = """
                                        MATCH (n:Person)
                                        MATCH (m:""" + str(at1) + """{ name: '""" + str(a1) + """'})
                                        MATCH (n)-[:""" + verb[0] + """]->(m) 
                                        RETURN n.name
                                    """

        print(cypher)
        r = self.graph.run(cypher).data()           #return list of dictionaries
        r =[d['n.name'] for d in r]             #getting just names from the result
        # print(r)
        if game == True:
            if self.res.size == 0:
                self.res = np.append(self.res,r)
            else:
                self.res = np.intersect1d(self.res,r)
            return self.res
        else:
            return r
# test = game()
# while True:
#     s = input(">>>")
#     print(test.search(s))