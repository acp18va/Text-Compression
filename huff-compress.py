##Student UI: Vijeta Agrawal_180127667
import re, operator, array, pickle, sys, getopt, time, os #importing various modules
          
#Createing NodeMaker Class to make node data structure 
class NodeMaker: 
    def __init__(self, Frequency, StringLabel): #NodeMaker Constructor
        self.Frequency = Frequency   #value
        self.Left_leaf = None  #child Node 1
        self.Right_leaf = None  #child Node 2
        self.Root = None    #Parent Node
        self.StringLabel = StringLabel #LabelElement
        
class CodeForHuffman:   #Creating Huffman Code Class
    def __init__(self, name):   #Huffman Code Class Constructor
        self.name = name
        self.infile = open(name)    #Taking file input to compress
        self.infile = self.infile.read()    #Reading file
         
    def CountWord(self):    #creating Symbol Model For Words
        infile = self.infile
        listofWords = re.findall(r"[a-zA-Z]+|[^A-Za-z]", infile)
        Dictword = {}
        for w in listofWords:
            if w in Dictword:   #Counting Words
                Dictword[w] += 1
            else:
                Dictword[w] = 1
        WordDictionary = {}
        for w, f in Dictword.items():
            WordDictionary[w] = f
            self.WordDictionary = WordDictionary
            self.WordDictionary["EOF"] = 1
        self.listofWords = listofWords
        return self.WordDictionary, self.listofWords  #returning words and words with Count

    def CountSymChar(self): #creating Symbol Model For Char
        infile = self.infile
        listofWords = re.findall(r"[a-zA-Z]|[^A-Za-z]", infile)
        Dictofchar = {}
        for c in listofWords:
            if c in Dictofchar:
                Dictofchar[c] += 1  #Counting Char
            else:
                Dictofchar[c] = 1
        WordDictionary = {}
        for c, f in Dictofchar.items():
            WordDictionary[c] = f
            self.WordDictionary = WordDictionary
            self.WordDictionary["EOF"] = 1
        self.listofWords = listofWords
        return self.WordDictionary, self.listofWords  #returning char and char with Count
    
    def Sorter(self):   #Sorting in pre-order
        self.sorted_WordDictionary = dict(sorted(self.WordDictionary.items(), key=operator.itemgetter(1)))
        self.sorted_WordDictionary = [(k, v/sum(self.sorted_WordDictionary.values())) for k, v in self.sorted_WordDictionary.items()]   #calculating probability // swapping keys & value position
        return self.sorted_WordDictionary
    
    def Make_Huffman_Tree(self): #making huffman tree
        huff_tree = []
        for item in self.sorted_WordDictionary: #
            huff_tree.append(NodeMaker(item[1],item[0]))    #making nodes and adding in list
        self.leaf = []
        while(len(huff_tree)!=1):
            element1 = huff_tree.pop(0) #Following Huffman Method
            element2 = huff_tree.pop(0) #popping elements
            element3 = NodeMaker(element1.Frequency + element2.Frequency, 'Root')#creating new element by adding previous two
            element1.Root = element3
            element2.Root = element3
            element3.Left_leaf = element1 #setting child node
            element3.Right_leaf = element2
            huff_tree.append(element3)  #appending in tree
           
            self.sorted_tree = sorted(huff_tree, key = operator.attrgetter('Frequency'))    #sorting again to repeat process
            if (element1.StringLabel != 'Root'):
                self.leaf.append(element1)
            if (element2.StringLabel != 'Root'):    #setting parent
                self.leaf.append(element2)
        return self.leaf
                
    def TreeTraverse(self):  #traversing the tree and making binary code for every symbol in tree
        Final_dict = {}
        for element in self.leaf: #leaf is tree
            Binary=''
            ele=element.StringLabel
            while(True):
                if element.Root == None:
                    break
                else:
                    if element.Root.Left_leaf == element: #Adding 0 for right and 1 for left
                        Binary += '1'
                    else:
                        Binary += '0'
                    element=element.Root
            
            Final_dict[ele] = Binary[::-1]
        self.filename, self.file_extension = os.path.splitext(self.name) #separating name from extension
        print(self.filename)
        Createdfile = open('{}-symbol-model.pkl'.format(self.filename), 'wb') #using pickle to save file
        pickle.dump(Final_dict, Createdfile)
        Createdfile.close()
        self.Final_dict = Final_dict
        return(self.Final_dict)
        
    def Encoder(self): #Encoding the Binary dictionary to a Binary string for the symbols
        Final_string = ''
        for Symbol in self.listofWords:
            Final_string += self.Final_dict[Symbol]
        Final_string += self.Final_dict["EOF"]
        self.Final_string = Final_string
        return self.Final_string #Returning encoded string
            
    def CreatingBitArray(self): #Removing padding from String
        Code = array.array('B')
        size = (8 - len(self.Final_string)%8)
        for everybit in range(0, size):
            self.Final_string += '0'
        for everybit in range(0, len(self.Final_string), 8):
            a = self.Final_string[everybit:everybit+8]
            Code.append(int(a,2))   #creating compressed string
        self.Code = Code
        CreateFile = open('{}.bin'.format(self.filename), 'wb') #Storing compressed string to file
        Code.tofile(CreateFile)
        CreateFile.close()


class CommandLine:  #for cmd arguments / no use with test.harness.py
    def __init__(self):
        options, args = getopt.getopt(sys.argv[1:], 'sw')
        options = dict(options)
        self.exit = True   
        if '-s' in options: self.model = 'char'
        elif '-w' in options: self.model = 'word'
        else: self.model = 'word'
           
if __name__ == '__main__':  #calling each functions
    Configuration = CommandLine()
    model = sys.argv[2] #for test harness
    file = sys.argv[3]  #for test harness
    StartTimeTotal = time.clock()   #Using time module to check performance
    InstanceForHuffman = CodeForHuffman(file)
    if Configuration.model == model:
        characterdict, wordcounted = InstanceForHuffman.CountSymChar()
    else:
        worddict, wordcounted = InstanceForHuffman.CountWord()
    
    sort = InstanceForHuffman.Sorter()
    Tree = InstanceForHuffman.Make_Huffman_Tree()
    Traverse = InstanceForHuffman.TreeTraverse()
    StopTime = time.clock()
    print("Time taken to build Model",StopTime-StartTimeTotal)
    StartTime = time.clock()
    Encoding = InstanceForHuffman.Encoder()
    BitArray = InstanceForHuffman.CreatingBitArray()
    StopTime = time.clock()
    print("Time taken to Encode", StopTime-StartTime)
    StopTimeTotal = time.clock()      
    print("Total Time taken for Compression", StopTimeTotal-StartTimeTotal)