from py2neo import Graph,Node,Relationship
from nlp_part import nlp_part
class network:
    def __init__(self):
        self.nlp = nlp_part()
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "123"))
        # self.graph.delete_all()
     
    def create(self,sentence):
        nouns, verb, adjective,count,In,CC = self.nlp.processData(sentence)
        if len(verb)>1:
            verb[0] = verb[-1]
        if CC != []:
            w1, t1 = nouns[0]
            i = 1
            # print(len(nouns))
            while i < len(nouns):
                w2, t2 = nouns[i]
                cypher = """
                                    MERGE (n:""" + t1 + """ { name: '""" + str(w1) + """'})
                                    MERGE (m:""" + t2 + """{name: '""" + str(w2) + """'})  
                """
                if verb !=[]:
                    cypher = cypher +"""MERGE (n)-[:""" + str(verb[0]) + """]->(m) """
                else:
                    cypher = cypher + """MERGE (n)-[:""" + str(In[0]) + """]->(m) """
                # print(cypher)
                self.graph.run(cypher)
                i=i+1
            return
        else:
            if verb ==[] and In!=[]:
                w1, t1 = nouns[0]
                w2, t2 = nouns[1]
                cypher = """
                        MERGE (n:""" + t1 + """ { name: '""" + str(w1) + """'})
                        MERGE (m:""" + t2 + """{name: '""" + str(w2) + """'})
                        MERGE (n)-[:""" + str(In[0]) + """]->(m) 
                    """
            else:
                if In != [] and len(nouns) == 3:
                    w1, t1 = nouns[0]
                    w2, t2 = nouns[1]
                    w3, t3 = nouns[2]
                    cypher = \
                        """
                        MERGE (n:"""+t1+""" { name: '""" + str(w1) + """'})
                        MERGE (m:"""+t2+""" {name: '""" + str(w2) + """'})
                        MERGE (o:"""+t3+""" {name: '""" + str(w3) + """'})
                        MERGE (n)-[:""" + verb[0] + """]->(m) 
                        MERGE (m)-[:""" + In[0] + """]->(o) 
                        """
                else:
                    if adjective == [] and count == 0 and len(nouns)>1:
                        w1, t1 = nouns[0]
                        w2, t2 = nouns[1]
                        cypher = """
                                    MERGE (n:"""+t1+""" { name: '"""+str(w1)+"""'})
                                    MERGE (m:"""+t2+"""{name: '"""+str(w2)+"""'})
                                    MERGE (n)-[:"""+verb[0]+"""]->(m) 
                                """
                    else:
                        if len(nouns) ==1 and len(verb) == 1 and len(adjective)==1:
                            w1, t1 = nouns[0]
                            a1,at1 = adjective[0]
                            cypher = """
                                    MERGE (n:""" + str(t1) + """  { name: '""" + str(w1) + """'})
                                    MERGE (m:""" + str(at1) + """ {name: '""" + str(a1) + """'})
                                    MERGE (n)-[:""" + verb[0] + """]->(m) 
                                """
                        else:
                            if len(nouns)>1:
                                # verb[0] = verb[-1]
                                w1, t1 = nouns[0]
                                w2, t2 = nouns[1]
                                if adjective != []:
                                    a1, at1 = adjective[0]
                                else:
                                    a1, at1 = count
                                if len(verb) >1:
                                    cypher = """
                                            MERGE (n:""" +str(t1)+ """  { name: '"""+str(w1)+"""'})
                                            MERGE (m:"""+str(t2)+""" {name: '"""+str(w2)+""" '})
                                            MERGE (o:"""+str(at1)+""" {name: '"""+str(a1)+""" '})
                                            MERGE (n)-[:"""+verb[1]+"""]->(m) 
                                            MERGE (m)-[:"""+verb[0]+"""]->(o) 
                                        """
                                else:
                                    if len(In) ==1:
                                        cypher = """
                                                MERGE (n:""" + str(t1) + """  { name: '""" + str(w1) + """'})
                                                MERGE (m:""" + str(t2) + """ {name: '""" + str(w2) + """ '})
                                                MERGE (o:""" + str(at1) + """ {name: '""" + str(a1) + """ '})
                                                MERGE (n)-[:""" + verb[0] + """]->(m) 
                                                MERGE (m)-[:""" + In[0] + """]->(o) 
                                            """
                                    else:
                                        cypher = """
                                                MERGE (n:""" + str(t1) + """  { name: '""" + str(w1) + """'})
                                                MERGE (m:""" + str(t2) + """ {name: '""" + str(w2) + """ '})
                                                MERGE (o:""" + str(at1) + """ {name: '""" + str(a1) + """ '})
                                                MERGE (n)-[:""" + verb[0] + """]->(m) 
                                                MERGE (m)-[:is]->(o) 
                                            """


                            else:
                                w1, t1 = nouns[0]
                                if adjective !=[]:
                                    a1, at1 = adjective[0]
                                else:
                                    if len(verb)>1 and len(verb)>0:
                                        a1, ct1 = count
                                        at1 = verb[1]
                                    else:
                                        a1, at1 = count

                                cypher = """
                                        MERGE (n:""" + str(t1) + """  { name: '""" + str(w1) + """'})
                                        MERGE (m:""" + str(ct1) + """{ name: '""" + str(a1) + """'})
                                        MERGE (n)-[:"""+verb[0]+"""]->(m) 
                                    """

        print(cypher)
        self.graph.run(cypher)
test = network()
test.create("Books are in Bag. Ahmad picked cpp book with ISBN Number 12345. Ahmad bought the book from Bilal. Ahmad shared the book with Saira and Bilal. Saira like reading the book.")
