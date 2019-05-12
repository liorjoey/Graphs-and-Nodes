class Node: #a dictionary of the nodes that are paired with the node:{...,neighbor name:edge weight,...)

    def __init__(self,name):
        self.name=name
        self.adjacents={}

    def __str__(self): #returns a string with the node name, his neighbors name and their edges weight
        neigbors_details=""
        for key in self.adjacents:
            neigbors_details+="%s with edge weight of %d\n"%(key,self.adjacents[key])
        return "Node %s has %d neighbors:\n%s"%(self.name,len(self.adjacents),neigbors_details)

    def __eq__(self, other): #checks if two nodes have the same name
        return self.name == other.name

    def __ne__(self, other): #checks if two nodes have different names
        return self.name != other.name

    def neighbors(self): #returns a list of the names of the adjacent nodes (the node neighbors names)
        return self.adjacents.keys()

    def is_neighbor(self, name): #check if a node is a neighbor by his name
        return name in self.neighbors()

    def add_neighbor(self, name, weight=1): #adds a new neighbor to a node including his weight
        return self.adjacents.update({name:weight})

    def remove_neighbor(self, name): #removes one of the node neighbors by giving the neighbors name
        return self.adjacents.pop(name)

    def is_isolated(self): #checks if a node has no neighbors at all
        return len(self.neighbors())==0

###################################################################################################################################

class Graph(Node): #Creates a dict of:{...,node_name:node_object,...)
    def __init__(self,*nodes):
        self.nodes={}
        for node in nodes:
           self.nodes[node]=Node(node)

    def __str__(self): #returns a string explaining how many nodes are in the graph and their names
        a=""
        for node in self.nodes:
            a+="%s, "%node
        return "the graph has %d nodes:"%(len(self.nodes))+a[:-2]+"."

    def __len__(self): #returns the no. of nodes in the graph
        return len(self.nodes)

    def __contains__(self, name): #checks if a node is in the graph by his name
        return name in self.nodes

    def __getitem__(self, name): #returns a node object by his name
        return self.nodes[name]

    def __add__(self, other): # create a new graph from all the nodes of two other graphs
        all_names=list(self.names())+list(other.names())
        a=Graph(*all_names)
        for edge in self.edges():
            a.add_edge(edge[0],edge[1],self.get_edge_weight(edge[0],edge[1]))
        for edge in other.edges():
            a.add_edge(edge[0],edge[1],other.get_edge_weight(edge[0],edge[1]))
        return a

    def names(self): #returns a list of the names of all the nodes in the graph
        return self.nodes.keys()

    def edges(self):  # returns a list of all the edges(tuples) in the graph (without the opposites- if there is (a,b) and (b,a) only one of them will enter
        list1 = []
        list2 = []
        for name in self.names():
            list2.extend(self.__getitem__(name).neighbors())
            a = 0
            while a < len(self.__getitem__(name).neighbors()):
                list1.append(name)
                a += 1
        list3=list(zip(list1, list2))
        list4=[]
        for i in range(len(list3)):
            if (list3[i][1],list3[i][0]) not in list4:
                list4.append((list3[i][0], list3[i][1]))
        return list4

    def is_edge(self,frm_name,to_name):#checks if there is such edge in the Graph
        return self.__getitem__(frm_name).is_neighbor(to_name) or self.__getitem__(to_name).is_neighbor(frm_name)

    def add_edge(self, frm_name, to_name, weight=1): #adds a new edge to the Graph
        self.__getitem__(frm_name).add_neighbor(to_name, weight)
        self.__getitem__(to_name).add_neighbor(frm_name, weight) # no direction

    def remove_edge(self, frm_name, to_name): #removes a specific edge from the Graph
        self.__getitem__(frm_name).remove_neighbor(to_name)
        self.__getitem__(to_name).remove_neighbor(frm_name) # no direction

    def get_edge_weight(self, frm_name, to_name): #return the edge weight
        return self.__getitem__(frm_name).adjacents[to_name]

    def get_path_weight(self, path): #return a path weight
        t_weight=0
        for i in range(len(path)-1):
            t_weight+=self.get_edge_weight(path[i], path[i+1])
        return t_weight

    def find_path (self, frm_name, to_name): #returns all possible paths between frm_name and to_name
        possible_paths=[[frm_name,neighbor] for neighbor in self.__getitem__(frm_name).neighbors()]
        good_paths=[]

        for path in possible_paths:
            if path[-1] == to_name:
                good_paths.append(path)
            elif path[-1]!=frm_name:
                for neighbor in self.__getitem__(path[-1]).neighbors():
                    if neighbor not in path: # no direction
                        possible_paths.append(path+[neighbor])
        return good_paths

    def find_shortest_path(self, frm_name, to_name): #returns the possible paths between frm_name and to_name with the lowest weight
        weights=[self.get_path_weight(path) for path in self.find_path(frm_name, to_name)]
        paths=self.find_path (frm_name, to_name)
        return paths[weights.index(min(weights))]

#Question4
    def suggest_friend(self, node_name): #return the name of the friend with the most common friends who is not friends of the node_name
        best_suggestion = ["", 0]
        for other_node in self.names():
            if node_name not in self.__getitem__(other_node).neighbors() and node_name!=other_node:
                common_friends = set(self.__getitem__(other_node).neighbors()).intersection(set(self.__getitem__(node_name).neighbors()))
                if len(common_friends)>best_suggestion[1]:
                    best_suggestion = [other_node, len(common_friends)]
            else:
                continue
        return best_suggestion[0]

###################################################################################################################################
#Question1
with open("social.txt","r") as f:
    users=set([line.split()[0] for line in f])
with open("social.txt", "r") as f:
    users2 =set([line.split()[3] for line in f])
    users=users.union(users2)
    users_graph=Graph(*users)
#def add_edge(self, frm_name, to_name, weight=1)
with open("social.txt", "r") as f:
    num_friends=[]
    for line in f:
        frm_name=line.split()[0]
        to_name = line.split()[2]
        line_num=1
        if line.split()[-1]=='friends.':
            users_graph.add_edge(line.split()[0],line.split()[2])
            #print ("%s:%s"% (line.split()[0],users_graph.__getitem__(line.split()[0]).neighbors()))
            num_friends.append(len(users_graph.edges()))
        else:
            if users_graph.is_edge(line.split()[0],line.split()[2]):
                users_graph.remove_edge(line.split()[0], line.split()[2])
                num_friends.append(len(users_graph.edges()))
            if users_graph.is_edge(line.split()[2],line.split()[0]):
                users_graph.remove_edge(line.split()[2], line.split()[0])
                num_friends.append(len(users_graph.edges()))
    print ("Question1 Answer is:",max(num_friends))

#Benjamin and Levi became friends.
#Ephraim and Benjamin cancelled their friendship.

#Question2
with open("social.txt","r") as f:
    users=set([line.split()[0] for line in f])
with open("social.txt", "r") as f:
    users2 =set([line.split()[3] for line in f])
    users=users.union(users2)
    users_graph=Graph(*users)

with open("social.txt", "r") as f:
    num_friends=[]
    for line in f:
        frm_name=line.split()[0]
        to_name = line.split()[2]
        line_num=1
        if line.split()[-1]=='friends.' and 'Reuben' in line.split():
            users_graph.add_edge(line.split()[0],line.split()[2])
            #print "%s:%s"% (line.split()[0],users_graph.__getitem__(line.split()[0]).neighbors())
            num_friends.append(len(users_graph.edges()))
        elif 'Reuben' in line.split():
            if users_graph.is_edge(line.split()[0],line.split()[2]):
                users_graph.remove_edge(line.split()[0], line.split()[2])
                num_friends.append(len(users_graph.edges()))
            if users_graph.is_edge(line.split()[2],line.split()[0]):
                users_graph.remove_edge(line.split()[2], line.split()[0])
                num_friends.append(len(users_graph.edges()))
    print ("Question2 Answer is:",max(num_friends))

# Question3
paths=[]
for frm_name in users:
    for to_name in users:
        paths.extend(users_graph.find_path(frm_name, to_name))
longest_path=paths[0]
for path in paths:
    if len(path)>len(longest_path):
        longest_path=path
print ("Question3 Answer is:",longest_path)

###################################################################################################################################
#Part2-task1

class DirectedGraph(Graph): #Creates a dict of:{...,node_name:node_object,...)
    def __init__(self,*nodes):
        self.nodes={}
        for node in nodes:
           self.nodes[node]=Node(node)

    def __add__(self, other): # create a new graph from all the nodes of two other graphs
        all_names = list(self.names()) + list(other.names())
        a=DirectedGraph(*all_names)
        for edge in self.edges():
            a.add_edge(edge[0],edge[1],self.get_edge_weight(edge[0],edge[1]))
        for edge in other.edges():
            a.add_edge(edge[0],edge[1],other.get_edge_weight(edge[0],edge[1]))
        return a

    def edges(self):  # returns a list of all the edges(tuples) in the graph (without the opposites- if there is (a,b) and (b,a) only one of them will enter
        list1 = []
        list2 = []
        for name in self.names():
            list2.extend(self.__getitem__(name).neighbors())
            a = 0
            while a < len(self.__getitem__(name).neighbors()):
                list1.append(name)
                a += 1
        list3=list(zip(list1, list2))
        list4=[]
        for i in range(len(list3)):
            list4.append((list3[i][0], list3[i][1]))
        return list4

    def is_edge(self,frm_name,to_name):
        return self.__getitem__(frm_name).is_neighbor(to_name)

    def add_edge(self, frm_name, to_name, weight=1):
        self.__getitem__(frm_name).add_neighbor(to_name, weight)

    def remove_edge(self, frm_name, to_name):
        self.__getitem__(frm_name).remove_neighbor(to_name)


#g=Graph('a','b','c','d','e')
#d=DirectedGraph('a','b','c','d','e')

###################################################################################################################################

#Part2-task2: travelEW

#weight= the average time all the travels took from one region to the other

with open('travelsEW.csv') as ew: #making a list out of the file
    ew_list=[line.replace(","," ").strip("\n").split() for line in ew][1:]

#getting the nodes of travelsEW ready to be entered to a graph:
    #I had to remove bad lines from the file. the code i used in order to track the bad lines::
        #for line in ew_list:
        #   if line[0]=='W' or line[3]=='Sou':
        #      print (ew_list.index(line))
nodes_ew_frm=set([line[0] for line in ew_list])
nodes_ew_to=set([line[3] for line in ew_list])
nodes_ew=nodes_ew_to.union(nodes_ew_frm)

#creating travelsEW graph:
travelsEW=DirectedGraph(*nodes_ew)

from datetime import *
#setting the travelsEW datetimes to match a known format:
for line in ew_list:
    line[1]=line[1]+" "+line[2]
    line[1].replace('h',':').strip('m')
    line[4]=line[4]+" "+line[5]
    line.pop(2)
    line.pop(-1)
    line[1]=line[1].replace('h', ':').strip('m')
    line[-1]=line[-1].replace('h', ':').strip('m')
# adding the time (seconds) each travel took to ew_list:
    st_time=datetime.strptime(line[1], '%d/%m/%Y %H:%M')
    en_time=datetime.strptime(line[-1], '%d/%m/%Y %H:%M')
    travel_weight=en_time-st_time
    line.append(float(travel_weight.seconds))

# calculating the average weight for each track:
routes_ew=[]
for line in ew_list:
    if [line[0],line[2],0,0] not in routes_ew:
        routes_ew.append([line[0], line[2],0,0]) #[start,end,total_time,num_travels]
for line in ew_list:
    for route in routes_ew:
        if line[0]==route[0] and line[2]==route[1]:
            route[2]+=line[-1]
            route[3]+=1

for route in routes_ew: #[start,end,average_seconds_per_travel]
    route.append((route[2]/route[3]))
    route.pop(2)
    route.pop(2)

for route in routes_ew:
    travelsEW.add_edge(route[0],route[1],route[2])

###################################################################################################################################

#Part2-task2: travelWE

with open('travelsWE.csv') as we: #making a list out of the file
    we_list=[line.replace(" ; ",",").replace(",","-").strip("\n").split("-") for line in we][1:]

for line in we_list: #changing the we file list so that it the dates will be before the hours (to use with datetime later)
#I had to remove bad lines from the file.
    line.insert(3,line[1])
    line.pop(1)
    line.insert(6, line[4])
    line.pop(4)
print ("after",we_list)

#getting the nodes of travelsWE ready to be entered to a graph:
nodes_we_frm=set([line[0] for line in we_list])
nodes_we_to=set([line[3] for line in we_list])
nodes_we=nodes_we_to.union(nodes_we_frm)

#creating travelsWE graph:
travelsWE=DirectedGraph(*nodes_we)
print (travelsWE.names(),"2")

#preparing for adding edges to travelsWE:

#setting the travelsWE datetimes to match a known format:
print (we_list)
for line in we_list:
    line[1]=line[1]+" "+line[2]
    line[4]=line[4]+" "+line[5]
    line.pop(2)
    line.pop(-1)
# adding the time (seconds) each travel took to we_list:
    # had to manualy fix:
        # changed Jam to Jan> ValueError: time data 'Jam 25 16 05:55:00PM' does not match format '%b %d %y %I:%M:%S%p
        # changed 00 to 28> ValueError: time data 'Feb 00 16 02:43:00AM' does not match format '%b %d %y %I:%M:%S%p'
    st_time=datetime.strptime(line[1], '%b %d %y %I:%M:%S%p')
    en_time=datetime.strptime(line[-1], '%b %d %y %I:%M:%S%p')
    travel_weight=en_time-st_time
    line.append(float(travel_weight.seconds))

# calculating the average weight for each track:
routes_we=[]
for line in we_list:
    if [line[0],line[2],0,0] not in routes_we:
        routes_we.append([line[0], line[2],0,0]) #[start,end,total_time,num_travels]
for line in we_list:
    for route in routes_we:
        if line[0]==route[0] and line[2]==route[1]:
            route[2]+=line[-1]
            route[3]+=1

for route in routes_we: #[start,end,average_seconds_per_travel]
    route.append((route[2]/route[3]))
    route.pop(2)
    route.pop(2)
for route in routes_we:
    travelsWE.add_edge(route[0],route[1],route[2])
print (travelsWE.edges(),"45")
#adding both graphs together
all_travels=travelsEW.__add__(travelsWE)
print (travelsWE.edges(),"1")
print (travelsEW.edges(),"2")
print (all_travels.edges(),"4")






























