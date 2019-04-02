# UID: 180128022

# Importing Pickle module
import pickle, time, sys, os

class HuffmanDecompress:
    def __init__(self, Dictionary, Code): 
        self.Dictionary = Dictionary
        self.Code = Code
    
    def Convert(self): 
        Binary = ""
        for b in self.CodeDecompressed:
            Str = bin(b)
            Str = Str[2:] 
            Padding = ""
            for zero in range(0, 8 - len(Str)):
                Padding += "0" 
            Str = Padding + Str
            Binary += Str
        self.Binary = Binary
        
    def CodeReader_ReaderDict(self): # Reading the compressed file
        CodeDecompressed = open(self.Code, "rb")
        CodeDecompressed = CodeDecompressed.read()
        self.CodeDecompressed = CodeDecompressed
        DictDecompressed = open(self.Dictionary, "rb")
        DictDecompressed = pickle.load(DictDecompressed)
        self.DictDecompressed = DictDecompressed
    
    def Decoder(self): 
        FinalStr = dict((value, key) for key, value in self.DictDecompressed.items())
        StrDecoded = ""
        ToCheck = ""
        for element in self.Binary:
            ToCheck += element
            try:
                char = FinalStr[ToCheck]
                StrDecoded += char
                ToCheck = ""
            except KeyError: continue
        OriginalStr = StrDecoded.replace("EOF","")
        filename, file_extension = os.path.splitext(self.Code)
        infile = open("{}-decompressed.txt".format(filename), "w")
        infile.write(OriginalStr) 
        infile.close()
        
StartTimeTotal = time.clock()
symbol = sys.argv[1]
filename, file_extension = os.path.splitext(symbol)
InstanceofHuffman = HuffmanDecompress('{}-symbol-model.pkl'.format(filename), symbol)
readerdict_codereader = InstanceofHuffman.CodeReader_ReaderDict()
binaryconvert = InstanceofHuffman.Convert()
StartTime = time.clock()
todecode = InstanceofHuffman.Decoder()
StopTime = time.clock()
print("Time taken to decode", StopTime-StartTime)
StopTimeTotal = time.clock()
print("Total Time taken for Decompression", StopTimeTotal-StartTimeTotal)