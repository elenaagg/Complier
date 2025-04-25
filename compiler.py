#Angelopoulou Elena  AM:4968
#Tsioni Valentina  AM:4929

import string

class Token:
    # properties : recognized_string , family , line_number
    def __init__(self,recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
        
    def __str__(self):
        return f"{self.recognized_string}  family: {self.family}, line: {self.line_number}"
         
    
class Lex:

    def __init__(self,file_name,current_line):
        self.file_name = file_name
        self.current_line = current_line
        self.token = Token('','','')
        
    
    def next_token(self):

        #Alphabet of cpy:
        
        number = [str(num) for num in range(-32767, 32768)]
        letters = set(string.ascii_letters)
        digits = set([str(i) for i in range(10)])
        addOperator = set(['+', '-', '*', '//', '%'])
        relOperator = set(['<', '>', '==', '<=', '>=', '!='])
        assignment = set(['='])
        delimiter = set([',', ':'])
        groupSymbol = set(['(', ')', '#{', '#}'])
        comments = set(['##'])
        whitespace_characters =set(['\t',' ','\n'])
        
        #Reserved words
        keyword = set(['main', 'def', '#def', '#int', 'global', 'if', 'elif', 'else', 'while', 'print', 'return', 'input', 'int', 'and', 'or', 'not'])
        
        
        count =0   #count the occurrences of ##
        for line in file_name:
            self.current_line+=1
            for i, char in enumerate(line):
                recognized_string= self.token.recognized_string + char
                if count % 2==0:                          
                    if len(recognized_string)<=30:   #Only the first 30 characters
                        if recognized_string in keyword:
                                self.token=Token(recognized_string,'keyword',self.current_line)
                                if i + 1 < len(line):
                                    if line[i+1] not in letters:
                                        list.append(Token(recognized_string,'keyword',self.current_line))

                                        self.token.recognized_string=''
                                else:
                                    list.append(Token(recognized_string,'keyword',self.current_line))           #return the object in a list
                                    self.token.recognized_string=''
                                
                        elif char in letters:
                                self.token=Token(recognized_string,'id',self.current_line)
                                if i + 1 < len(line):
                                    if line[i+1] not in letters and line[i+1] not in digits :                        #sneak peek to know when to return the suitable object
                                            list.append(Token(recognized_string,'id',self.current_line))
                                            self.token.recognized_string=''                                          
                                else:
                                    list.append(Token(recognized_string,'id',self.current_line))
                                    self.token.recognized_string=''

                        elif char in digits:
                            self.token=Token(recognized_string,'number',self.current_line)
                            if i + 1 < len(line):
                                if line[i+1] not in digits and line[i+1] not in letters :
                                    if recognized_string[0] in letters:   
                                        list.append(Token(recognized_string,'id',self.current_line))
                                        self.token.recognized_string='' 
                                    else:
                                        if recognized_string in number:
                                                    list.append(Token(recognized_string,'number',self.current_line))
                                                    self.token.recognized_string=''
                                        else:
                                                self.error('Error: Number out of range')            
                                                
                                        
                                elif line[i+1] in letters and recognized_string[0] not in letters :    
                                        self.error('Error: Non supported string')
                                        
                                        
                                
                            else:                                    
                                list.append(Token(recognized_string,'number',self.current_line))
                                self.token.recognized_string=''
                            

                        elif recognized_string in addOperator:
                                self.token=Token(recognized_string,'addOperator',self.current_line)
                                if i + 1 < len(line):
                                    if line[i+1] not in addOperator :
                                        list.append(Token(recognized_string,'addOperator',self.current_line))
                                        self.token.recognized_string=''
                                        
                                else:
                                    list.append(Token(recognized_string,'addOperator',self.current_line))
                                    self.token.recognized_string=''
                                
                        elif recognized_string in groupSymbol:
                                        self.token=Token(recognized_string,'groupSymbol',self.current_line)
                                        list.append(Token(recognized_string,'groupSymbol',self.current_line))
                                        self.token.recognized_string=''
                           
                        elif recognized_string in delimiter:
                                self.token=Token(recognized_string,'delimiter',self.current_line)
                                list.append(Token(recognized_string,'delimiter',self.current_line))
                                self.token.recognized_string=''
                               

                        elif recognized_string in assignment:
                                self.token=Token(recognized_string,'assignment',self.current_line)
                                if i + 1 < len(line):
                                    if line[i+1] not in assignment :
                                        list.append(Token(recognized_string,'assignment',self.current_line))
                                        self.token.recognized_string=''
                                else:
                                    list.append(list.append(Token(recognized_string,'assignment',self.current_line)))
                                    self.token.recognized_string=''
                                

                        elif recognized_string in relOperator:
                                self.token=Token(recognized_string,'relOperator',self.current_line)
                                if i + 1 < len(line):
                                    if line[i+1] not in assignment :
                                        list.append(Token(recognized_string,'relOperator',self.current_line))
                                        self.token.recognized_string=''
                                else:
                                    list.append(self.token)
                                    self.token.recognized_string=''
                                
                        elif recognized_string in whitespace_characters :
                            continue                            

                        elif recognized_string in comments  :
                            count+=1
                            self.token.recognized_string=''


                                                        
                        else:
                            self.token.__init__(recognized_string,'other',self.current_line)
                            #Be patient '#' ... something interesting might appear such as '#{'
                
                    else:
                        self.error('Error: Too many characters')
                        
                    

                #Comments are open , do not return!       
                else:
                        if "##" in recognized_string  :
                            count+=1
                            self.token.recognized_string=''                                
                        else:
                            self.token=Token(recognized_string,'other',self.current_line) 
          
            

        if count%2 != 0:  
            self.error('ERROR : Comments never closed')   #EOF

     
        

    def error(self,error_message):
        print(error_message , ", Line:",self.current_line)
        exit()



class Parser:
    temp_counter = -1      #counts the temporary variables
    index=0

    def __init__(self,lexical_analyzer,generated_program,table):
        self.lexical_analyzer=lexical_analyzer
        self.generated_program=generated_program
        self.quadpointer = QuadPointerList('')
        self.table = table         # Store the symbol table object     

    def get_token(self):
        
        self.lexical_analyzer.next_token()
        if self.index < len(list):
            self.token = list[self.index]
            self.index+=1
            return self.token
        else:
             return

    def syntax_analyzer(self):
        global token
        token = self.get_token()
        table.addScope('Main')     # Add the main scope 
        self.startRule()
        print('"Compilation successfully completed"')


    def error(self,error_message):
        print("Error:" ,error_message , ", Line:" ,token.line_number)
        exit()


    def startRule(self):
        self.defMain()
        self.callMain()

    def defMain(self):
        self.declarations()
        self.functions()
    
    def declarations(self):
        global token
        while token.recognized_string == '#int':
            token = self.get_token()
            self.idList('variable') #identify the id list

    def functions(self):
        global token
        while token.recognized_string == 'def':
            token = self.get_token()
            generated_program.genQuad("begin_block",token.recognized_string,"_","_")   #generates a quadruple representing the beginning of a block in a program
            n = token.recognized_string
            if token.family == 'id':
                token = self.get_token()
                if token.recognized_string == '(':
                    token = self.get_token()
                    self.idList('parameter')    #identifies the kind of entities
                    if token.recognized_string == ')':
                        token = self.get_token()
                        entity = Entity()            # Create and add a new Entity 
                        entity.datatype = 'procedure'  
                        entity.name = n
                        table.addEntity(entity)
                        if token.recognized_string == ':':
                            token = self.get_token()
                            table.addScope(n)       #Add the scope about the function
                            table.startingQuad()    #Store the starting point of the function
                            if token.recognized_string == '#{':
                                token = self.get_token()
                                self.declarations()
                                self.globals()
                                self.functions()
                                self.codeBlock()
                                if token.recognized_string == '#}':
                                    generated_program.genQuad("end_block",n,"_","_")    #generates a quadruple representing the end of a block in a program
                                    token = self.get_token()
                                    self.globals()
                                    self.declarations()
                                    table.framelength()      #Store the length of the record of frame in bytes
                                    table.writetable()        #Store the data for the syntax table
                                    table.deleteScope()      #Level is removed from the symbol table when the translation of a function is completed
                                else:
                                    self.error('You did not close the block of "#}"')
                            else:
                                    self.error(' "#{" was expected')
                        else:
                                    self.error('":" was expected')
                    else:
                        self.error(' ")" was expected')
                else:
                    self.error('"(" was expected')
            else:
                self.error('An ID was expected')
            
                

    def globals(self):
        global token
        while token.recognized_string == 'global':
            token = self.get_token()
            if token.family == 'id':
                token = self.get_token()
                self.globals()
            else:
                self.error('An ID was expected')
                

    def codeBlock(self):
        global token
        if token.family == 'id':
            self.assignmentStat()
            self.codeBlock()
        elif token.recognized_string == 'if':
            self.ifStat()
            self.codeBlock()
        elif token.recognized_string == 'while':
            self.whileStat()
            self.codeBlock()
        elif token.recognized_string == 'print':
            self.printStat()
            self.codeBlock()
        elif token.recognized_string == 'return':
            self.returnStat()
            self.codeBlock()
        elif token.recognized_string == 'int':
             self.inputStat()
             self.codeBlock()
        
             
        
        
        

    def inputStat(self):
        global token
        IDplace = token.recognized_string
        token = self.get_token()
        if token.recognized_string == '(':
            token = self.get_token()
            if token.recognized_string == 'input':
                token = self.get_token()
                if token.recognized_string == '(':
                    token = self.get_token() 
                    if token.recognized_string == ')':
                        token = self.get_token() 
                        generated_program.genQuad("inp",IDplace,"_","_")  #generates a quadruple that represents an input operation
                        if token.recognized_string == ')':
                             token = self.get_token() 
                        else:
                            self.error('You did not close "()"')                          
                    else:
                        self.error('You did not close "()"')
        
                else:
                    self.error('"(" was expected')
            else:
             self.error('invalid syntax')
        else:
             self.error('"(" was expected')


    def assignmentStat(self):
        global token
        IDplace = token.recognized_string
        token = self.get_token()
        if token.recognized_string == '=':
            token = self.get_token()
            Eplace = self.expression()                              #Eplace as the source of the assignment and IDplace as the destination
            generated_program.genQuad('=', Eplace, '_', IDplace)   #generates a quadruple representing the assignment operation
        else:
             self.error('Assignment was expected')
             

    def printStat(self):
        global token
        token = self.get_token()
        if token.recognized_string == '(':
            token = self.get_token()
            Eplace = self.expression()
            generated_program.genQuad('out', Eplace, '_', '_')   #generates a quadruple that represents an input operation
            if token.recognized_string == ')':
                token = self.get_token()
            else:
                self.error( 'You did not close "()"')
                
        else:
                self.error('"(" was expected ')
                

    def returnStat(self):
        global token
        token = self.get_token()
        Eplace = self.expression()
        generated_program.genQuad('retv', Eplace, '_', '_')   # quadruple for return


    def ifStat(self):
        global token
        global ifList
        ifList = []
        token = self.get_token() # consume if               
        B = self.condition()
        B_true = B[0]                  #store the return values from condition
        B_false = B[1]
        generated_program.backPatch(B_true, generated_program.nextQuad())     #modify the quadruple if the condition is true
        if token.recognized_string == ':':
            token = self.get_token()
            self.codeBlock()                              
            eli = generated_program.makeList(generated_program.nextQuad())    
            ifList = generated_program.makeList(generated_program.nextQuad())
            generated_program.genQuad("jump", "_", "_", "_")
            generated_program.backPatch(B_false, generated_program.nextQuad())    # handles the code for the false branch of a conditional statement

        else:
            self.error('":" was expected')

        self.elifpart() 
        self.elsepart()

        generated_program.backPatch(eli, generated_program.nextQuad())              #Represent the right positions of if-elif so we can backpatch after the if-elif-else structure
        generated_program.backPatch(ifList, generated_program.nextQuad())   




            
    def elifpart(self):
        global token
        global ifList
        
        while token.recognized_string == 'elif':               
            token = self.get_token()
            B = self.condition()
            B_true = B[0]
            B_false = B[1]
            generated_program.backPatch(B_true, generated_program.nextQuad())
            if token.recognized_string == ':':
                token = self.get_token()
                self.codeBlock()
                ifList = generated_program.makeList(generated_program.nextQuad())    #handling in an if-elif-else structure and jumps to the right place
                generated_program.genQuad("jump", "_", "_", "_")
                generated_program.backPatch(B_false, generated_program.nextQuad())
                
            else:
                self.error('":" was expected') 
     
            
    def elsepart(self):
        global token
        global ifList
        
        if token.recognized_string == 'else':               
            token = self.get_token()
            if token.recognized_string == ':':
                token = self.get_token()
                self.codeBlock()
            else:
                self.error('":" was expected')
                


    def whileStat(self):
        global token             
        token = self.get_token()
        Bquad = generated_program.nextQuad()
        B = self.condition()
        B_true = B[0]
        B_false = B[1]
        generated_program.backPatch(B_true, generated_program.nextQuad())
        if token.recognized_string == ':':
            token = self.get_token()
            if token.recognized_string == '#{':
                token = self.get_token()
                self.codeBlock()
                generated_program.genQuad("jump","_","_",Bquad)    #return to the beginning of the condition in order to continue the loop.
                generated_program.backPatch(B_false,generated_program.nextQuad())
                if token.recognized_string == '#}':
                    token = self.get_token()
                else:
                    self.error(' You did not close the block of "#}"')
                    
            else:
                self.error(' "{#" was expected')
                
        else:
            self.error('":" was expected')
              
        


    def idList(self,datatype):
        global token
        if token.family == 'id':
            name = token.recognized_string
            token = self.get_token()
            entity = Entity()
            table.offsetAssign(entity,name,datatype,table.offset())    #Calculate and Assign offset to the entity
            table.addEntity(entity) 
            while token.recognized_string == ',':
                token = self.get_token()
                name = token.recognized_string
                if token.family == 'id':  
                        token = self.get_token()
                        entity = Entity()
                        table.offsetAssign(entity,name,datatype,table.offset()) 
                        table.addEntity(entity) 
                else:
                    self.error('An ID was expected')
                    
        else:
            self.error('An ID was expected')
            

    def expression(self):
        global token 
        self.optionalSign()
        T1place = self.term()
        while token.recognized_string == '+' or token.recognized_string == '-':
            op = token.recognized_string
            token = self.get_token()
            T2place = self.term()
            w = self.newTemp()  #new temporal variable
            generated_program.genQuad(op,T1place,T2place,w)   #generates the quadruple to store the result so far
            T1place = w
        Eplace = T1place   #when ther is no other T2 we proceed
        return Eplace

    def term(self):
        global token 
        F1place = self.factor()
        while token.recognized_string == '*' or token.recognized_string == '//' or token.recognized_string == '%':
            op = token.recognized_string
            token = self.get_token()
            F2place = self.factor()
            w = self.newTemp()
            generated_program.genQuad(op,F1place,F2place,w)    #generates the quadruple to store the result so far
            F1place = w
        Tplace = F1place
        return Tplace


    def factor(self):
        global token
        if token.family == 'number': 
            Fplace = token.recognized_string
            token = self.get_token()
            return Fplace
        elif token.recognized_string == '(': 
            token = self.get_token()
            Eplace=self.expression()
            if token.recognized_string == ')':
               Fplace = Eplace
               token = self.get_token() 
               return Fplace
            else:
                self.error('You did not close "()"')
        elif token.family == 'id': 
            fname = token.recognized_string
            token = self.get_token()
            Fplace = self.idTail(fname)    #remember the name for later
            return Fplace


    def idTail(self,fname):
        global token
        if token.recognized_string == '(':
            token = self.get_token()
            self.actualParList()
            w = self.newTemp()
            generated_program.genQuad('par', w, 'RET', '_')     #generate quadruples for passing parameters and making a function call
            generated_program.genQuad('call', fname, '_', '_')
            if token.recognized_string == ')':
                token = self.get_token()
                return w
            else:
                self.error('You did not close "()"')
        else:
            return fname

    def actualParList(self):
        global token
        Eplace = self.expression()
        generated_program.genQuad('par', Eplace, 'CV', '_')     #passed by value
        while token.recognized_string == ',':
            token = self.get_token()
            Eplace = self.expression()
            generated_program.genQuad('par', Eplace, 'CV', '_')

    def optionalSign(self):
        global token
        if token.recognized_string == '+' or token.recognized_string == '-':
             token = self.get_token()

    def condition(self):
        global token
        Q1=self.boolTerm()
        Q1_true = Q1[0]
        Q1_false = Q1[1]
        B_true = Q1_true
        B_false = Q1_false
        while token.recognized_string == 'or':
            generated_program.backPatch(B_false, generated_program.nextQuad())
            token = self.get_token()
            Q2 = self.boolTerm()
            Q2_true = Q2[0]
            Q2_false = Q2[1]
            B_true = self.quadpointer.mergeList(Q1_true,Q2_true)   #updates B_true by merging the true lists of Q1 and Q2 using mergeList()
            B_false = Q2_false
        return B_true,B_false

    def boolTerm(self):
        global token
        B1 = self.boolfactor()
        Q_true = B1[0]
        Q_false = B1[1]
        B_true = Q_true
        B_false = Q_false
        while token.recognized_string == 'and':
            generated_program.backPatch(B_true, generated_program.nextQuad())
            token = self.get_token()
            B2 = self.boolfactor()
            Q2_true = B2[0]
            Q2_false = B2[1]
            Q_false = self.quadpointer.mergeList(Q_false,Q2_false)
            Q_true = Q2_true
            B_true = Q_true
            B_false = Q_false
        return B_true,B_false

    def boolfactor(self):
        global token
        if token.recognized_string == 'not':
            token = self.get_token()
            if token.recognized_string == '(':
                token = self.get_token()
                R = self.condition()
                if token.recognized_string == ')':
                    token = self.get_token()
                    R_true = R[0]
                    R_false = R[1]
                    B_true = R_false    #swaps the true and false lists, considering the not operation
                    B_false = R_true
                else:
                    self.error(' You did not close "()" ')
                    
            else:
                self.error('"(" was expected')
                
                
        elif token.recognized_string == '(':
            token = self.get_token()   
            R = self.condition()
            if token.recognized_string == ')':
                token = self.get_token()
                R_true = R[0]
                R_false = R[1]
                B_true = R_true     #does not swap
                B_false = R_false
            else:
                self.error('You did not close "()"')
                

        else:
            E1_place = self.expression()
            if token.family == 'relOperator':
                op = token.recognized_string
                token = self.get_token()                  
                E2_place = self.expression()
                R_true = generated_program.makeList(generated_program.nextQuad())         #handles the generation of quadruples for relational expressions
                generated_program.genQuad(op, E1_place, E2_place,"_")
                R_false = generated_program.makeList(generated_program.nextQuad())
                generated_program.genQuad("jump","_","_","_")
                B_true = R_true
                B_false = R_false
            else:
                 self.error('Relational operator was expected')
        return B_true,B_false        


    def callMain(self):
        global token
        if token.recognized_string == '#def':
                token = self.get_token()
                name = token.recognized_string
                generated_program.genQuad("begin_block",name,"_","_")    #quadruples for the beginning of the program
                if token.recognized_string == 'main':
                    token = self.get_token()
                    self.globals()
                    self.declarations()
                    self.functions()
                    self.codeBlock()
                    generated_program.genQuad('halt', '_', '_', '_')    #end of the program
                    generated_program.genQuad("end_block",name,"_","_") #quadruples for the end

                else:
                    self.error('"main" was expected')
        else:
            self.error('"#def" was epxected')
        

    def newTemp(self):        #generate new temporary variable names
        global temp_counter 
        entity = TemporaryVariable()
        self.temp_counter += 1
        table.offsetAssign(entity,f"T_{self.temp_counter}","temporary",table.offset())   #Offset Assign for the temporary variables
        table.addEntity(entity)
        return f"T_{self.temp_counter}"


class Quad:    #Start of the intermediate code
    # properties : label , op , op1 , op2 , op3
    def __init__(self,label, op, op1,op2,op3):
        self.label = label
        self.op = op
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        
    def __str__(self):
        return f"{self.label } :   {self.op}, {self.op1} , {self.op2}, {self.op3}"
       
class QuadPointer:
    # properties : label 
    def __init__(self,label):
        self.label = label
        
    def __str__(self):
        return f"{self.label}"

class QuadList:

    # properties : programList, quad_counter
    def __init__(self,programList,quad_counter):
        self.programList=programList
        self.quad_counter=quad_counter

    def __str__(self):
        return f"{self.quad}"

    def backPatch(self, list, label):     #update the last operand of quadruples in the programList based on the provided list of labels and a label value
        for i in list:
            for self.quad in self.programList:
                if self.quad.label == i:
                    self.quad.op3 = label
    
    def genQuad(self, op, op1, op2, op3):                #generates quadruples for the intermediate representation of the program and adds them to the list of quadruples
        self.quad=Quad(self.nextQuad(), op, op1, op2, op3)
        self.programList.append(self.quad)
        self.quad_counter+=1
        return self.quad

    #def empty_list(self):
       # return []

    def nextQuad(self):
        return self.quad_counter      #keeps track of the next available quadruple label 
    
    def makeList(self,label):       #initialize a list that will be used to store labels for backpatching operations
        return [label]
    
    def writetext(self):
        with open("compiler.int", "w") as file:
            for quad in self.programList:
                    # Write each quad's string representation into the file
                file.write(str(quad) + "\n")
                
   
class QuadPointerList:

    # properties : labelList
    def __init__(self,labelList):
        self.labelList=labelList
        

    def __str__(self):
        return f"{self.labelList}"

    def mergeList(self,list1, list2):
        return list1 + list2                      #concatenates two lists


scopeList =[]
class Table():          #Start of the syntax table

    global scopeList
    def __init__(self):
        self.scopeList = []    #Store all the scopes
    
    def addEntity(self,entity):
        global scopeList
        current_scope = scopeList[-1]  #Get the last element and append the entity to the entity list
        current_scope.entityList.append(entity)

    def addScope(self,name):
        global scopeList

        scope = Scope()
        scope.en.name = name
        if len(scopeList) >= 1:
            scope.level = scopeList[-1].level + 1  #If there are existing scopes in scopeList, set the level of the new scope to one higher than the level of the last scope

        scopeList.append(scope)       # Add the new scope to the scopeList

    def offsetAssign(self,entity, name, datatype, offset):   # Check the datatype of the entity and assign offset accordingly
    
        entity.datatype = datatype
        if entity.datatype == 'temporary':
            entity.offset = offset
        elif entity.datatype == 'variable':
            entity.variable.offset = offset
        elif entity.datatype == 'parameter':
            entity.formal.offset = offset
        entity.name = name

    def deleteScope(self):
        global scopeList
        scopeList[-1].entityList.clear()
        del scopeList[-1]   #Delete the last scope from scopeList

    def offset(self):
        global scopeList
        current_scope = scopeList[-1]
        offset = 12    # Initialize offset to 12 cause the first 12 bytes are reserved for the return address, the access link, and the return value
        
        if len(scopeList[-1].entityList) >= 1:
            for i in range( len(current_scope.entityList)):
                if current_scope.entityList[i].datatype in {'variable', 'temporary', 'parameter'}:
                    offset += 4  # Assuming each variable occupies 4 bytes, adjust as needed
        return offset

    def framelength(self):
        global scopeList      # Set the frameLength of the last entity in the entity list of the second-to-last scope
        scopeList[-2].entityList[-1].procedure.frameLength = self.offset()

    def startingQuad(self):      # Set the startingQuad of the last entity in the entity list of the second-to-last scope
        global scopeList
        current_scope = scopeList[-2]
        current_scope.entityList[-1].procedure.startingQuad = generated_program.nextQuad() 

   
        
       
    def writetable(self):            #Write the contents of the symbol table to a file named "Stable.txt"
        global scopeList
        with open("Stable.txt", "a") as file:
            file.write("-------------------------------------------------------------------------------------------------")
            file.write("\n")
            for scope in reversed(scopeList):
                file.write("\n")
                file.write("Level: " + str(scope.level) + " " + "  Scope: " + str(scope.en.name))
                for entity in scope.entityList:
                    file.write("\n")
                    if entity.datatype == "variable":
                        file.write("     Entity <------ " + str(entity.name) + "/"+ str(entity.variable.offset) + "/" + str(entity.datatype))
                    elif entity.datatype == "temporary":
                        file.write("     Entity <------ " + str(entity.name) + "/"+ str(entity.offset) + "/" + str(entity.datatype))
                        file.write("\n")
                    elif entity.datatype == "parameter":
                        file.write("     Entity <------ " + str(entity.name) + "/"+ str(entity.formal.offset) + "/" + str(entity.datatype))
                    elif entity.datatype == "procedure":
                        file.write("     Entity <------ " + str(entity.name) + " Framelength: " + str(entity.procedure.frameLength))
                        file.write("\n")
                        file.write("                    " + str(entity.name) + " StartingQuad: " + str(entity.procedure.startingQuad))
                        file.write("\n")
            file.close()
                     

   
       
     
class Scope():

    def __init__(self):
        self.level = 0
        self.entityList = []
        self.en = Entity()

class Entity():
    def __init__(self):
        self.name = ''
        self.constant = Constant()
        self.variable = Variable()
        self.formal = FormalParameter()
        self.procedure = Procedure()

class Constant(Entity):
    def __init__(self):
        self.name = ''
        self.datatype = ''

class Variable(Entity):
        def __init__(self):
            self.name = ''
            self.datatype = ''
            self.offset = 0 

class FormalParameter(Entity):
        def __init__(self):
            self.datatype = ''


class Procedure(Entity):
        def __init__(self):
            self.name = ''
            self.startingQuad = 0
            self.frameLength = 0
            self.formal_parameters = []
           


class TemporaryVariable(Variable):
     def __init__(self):
            self.name = ''
            self.datatype = ''
            self.offset = 0  

class Parameter(FormalParameter, Variable):
    def __init__(self):
        self.name = ''
        self.datatype = ''
        self.offset = 0 
        self.formal_parameters = FormalParameter()

class Function(Procedure):
    def __init__(self):
        self.name = ''
        self.dataType = " "
        self.startingQuad = 0
        self.frameLength = 0
        self.formalParameters = []
        



file=input('Enter file_name: ')  
with open(file, "r") as file_name:      #Open and read file line to line
    file_name=file_name.readlines()

list=[]
lexical_analyzer = Lex(file_name,0)   #This instance represents the lexical analyzer
generated_program = QuadList([],1)    #This instance represents the intermediate code
table = Table() #This instance represents the syntax table 
parser=Parser(lexical_analyzer,generated_program,table)  #This instance represents the syntax analyzer 
parser.syntax_analyzer()
generated_program.writetext()    #Create the output file for the intermediate code
