


class Token:
                
    def __init__(self, name:str, lexim:str):
        self.Tok = str((name, lexim))


class Inputs:
    # alphabet leters except n & t
    letters = {'a','b','c','d','e','d','e','f','g','h','i','j','k','l','m','o','p','q','r','s','u','v','w','x','y','z',
               'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}
    
    numbers = {'0','1','2','3','4','5','6','7','8','9'}
    signs = {'+','-'}
    operators = {'/','=','<', '>','!'}
    star = '*'
    bakslah = '\\'
    semicolon = ';'
    underline = '_'
    double_qoutation ='"'
    space = ' '
    seperators = {'(',')','{','}'}
    



class Lexical_analyser:
    
    def __init__(self, code_file:str):
        self.state = 0
        self.start_index = 0
        self.next_index = -1
        self.next = None
        self.code = str(code_file)
        self.tokens = open('tokens.txt','w+')
        self.next_type= None
        self.valid = True
        self.get_next_char()
    
    def run(self):
        while self.valid and (self.next_index < len(self.code)):
            self.get_type()

    # a method that gets next character of the code and then sets its type
    def get_next_char(self):
        self.next_index += 1
        if self.next_index < len(self.code) :
            self.next = self.code[self.next_index]
            self.input_type()
            

    # this method sets the type of the next character of code
    def input_type(self):
        if self.next in Inputs().letters:
            self.next_type = 'letter'
        elif self.next == 't':
            self.next_type = 't'
        elif self.next == 'n':
            self.next_type = 'n'
        elif self.next == '.':
            self.next_type = 'point'
        elif self.next == Inputs().bakslah:
            self.next_type = 'bakslash'
        elif self.next == Inputs().double_qoutation:
            self.next_type = 'double_qoutation'
        elif self.next in Inputs().numbers:
            self.next_type = 'number'
        elif self.next in Inputs().operators:
            self.next_type = 'operators'
        elif self.next == Inputs().semicolon:
            self.next_type = 'semicolon'
        elif self.next in Inputs().seperators:
            self.next_type = 'seperator'
        elif self.next in Inputs().signs:
            self.next_type = 'signs'
        elif self.next == Inputs().star:
            self.next_type = 'star'
        elif self.next == Inputs().underline:
            self.next_type = 'underline'
        elif self.next == Inputs().space:
            self.next_type = 'space'
        elif self.next in Inputs().seperators:
            self.next_type = 'seperator'
        elif self.next == ';':
            self.next_type == 'semicolon'
        else:
            self.error(f'Invalid input! {self.next} is not a valid input for simple language')

    def reset(self):
        self.start_index = self.next_index + 0
        self.state = 0

    # this method saves the token in a file 
    def save_token(self,typ):
        lxm = self.code[self.start_index:self.next_index]
        token = Token(typ, lxm)
        self.tokens.write('\n'+token.Tok)
        self.reset()

    def error(self,error_massege):
        self.tokens.write('\nError: '+error_massege)
        self.valid = False

    # this method is the implemantation of the DFA of token classes of language
    def get_type(self):
        # state 0
        if self.state == 0:
            if self.next_type == 'letter' or self.next_type == 't' or self.next_type == 'n' or self.next_type == 'underline':
                self.state = 1
                self.get_next_char()
            elif self.next_type == 'number' :
                self.state = 2
                self.get_next_char()
            elif self.next_type == 'operators' or self.next_type == 'star':
                self.state = 6
                self.get_next_char()
            elif self.next_type == 'signs':
                self.state = 5
                self.get_next_char()
            elif self.next_type == 'double_qoutation':
                self.state = 10
                self.get_next_char()
            elif self.next_type == 'bakslash':
                self.state = 7
                self.get_next_char()
            elif self.next_type == 'space':
                self.reset()
                self.get_next_char()
                
            elif self.next_type == 'seperator':
                if self.next == '(':
                    self.get_next_char()
                    self.save_token('PARANTES OPEN')
                elif self.next == ')':
                    self.get_next_char()
                    self.save_token('PARANTES CLOSE')
                elif self.next == '{':
                    self.get_next_char()
                    self.save_token('BRACKET OPEN')
                elif self.next == '}':
                    self.get_next_char()
                    self.save_token('BRACKET CLOSE')
            elif self.next_type == 'semicolon':
                self.get_next_char()
                self.save_token('SEMICOLON')
            else:
                self.error('Invalid Input!')
            
        
        # state 1
        elif self.state == 1:
            if self.next_type == 'letter' or self.next_type == 'n' or self.next_type == 't' or self.next_type == 'number':
                self.state = 1
                self.get_next_char()
            else:
                lexim = self.code[self.start_index:self.next_index]
                if lexim in {'if', 'else', 'while', 'print', 'scan','int', 'float', 'string'}:
                    self.save_token(lexim.upper())
                else:
                    self.save_token('ID')

        # state 2
        elif self.state == 2:
            if self.next_type == 'number':
                self.state = 2
                self.get_next_char()
            elif self.next_type == 'point':
                self.state = 3
                self.get_next_char()
            else:
                self.save_token('INT')

        # state 3
        elif self.state == 3:
            if self.next_type == 'number':
                self.state = 4
                self.get_next_char()
            else:
                self.error(f'compiler expect a number after "." but got{self.next}')
        
        # state 4
        elif self.state == 4:
            if self.next_type == 'number':
                self.state = 4
                self.get_next_char()
            else:
                self.save_token('FLOAT')
        
        # state 5
        elif self.state == 5:
            if self.next_type == 'number':
                self.state = 2
                self.get_next_char()
            else:
                self.save_token('OP')

        # state 6
        elif self.state == 6:
            logicop = {'!=', '==','<=', '>='}
            self.get_next_char()
            x = self.code[self.start_index:self.next_index]
            if x in logicop:
                self.save_token('OP')
                self.get_next_char()
            elif self.code[self.start_index] == '!' and self.next != '=':
                self.error(f'compiler expect "=" after "!" but got {self.next}')
            else:
                self.next_index -= 1
                self.save_token('OP')
                self.next_index += 1
            
        # state 7 
        elif self.state == 7:
            
            # this method can recognize multiple line comments
            def longcomment():
                while self.next != '*':
                    self.get_next_char()
        
                self.get_next_char()    
                if self.next == '\\':
                    self.get_next_char()
                    self.reset()
                else:
                    longcomment()
            
            # this method recognize short comments
            def shortcomment():
                while self.next != '\\':
                    self.get_next_char()

                self.get_next_char()
                if self.next == 'n':
                    self.get_next_char()
                    self.reset()
                else:
                    shortcomment()

            
            if self.next_type == 'star':
                self.get_next_char()
                longcomment()
            elif self.next == '\\':
                self.get_next_char()
                shortcomment()
            elif self.next_type == 'n' or self.next_type == 't':
                # space
                self.reset()
                self.get_next_char()
            else:
                self.error('Invalid input')
        
        # state 10
        elif self.state == 10:
                
            while self.next_type != 'double_qoutation':
                self.get_next_char()
            self.save_token('STRING')
            self.get_next_char()
