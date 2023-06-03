from curses.textpad import rectangle
import curses
import pickle
import requests
import math
import sys
import os

#region COMBINATION
class combination:
    def __init__(self):
        self.operators = list('*/+-')
        self.listNumbers = []
        self.listOperators = []
        self.listConcatenate = []
        self.listCombination = []
    
    def permutationNumbers(self, numbers, i=0):
        if i == len(numbers):
            self.listNumbers.append(numbers)	
        
        for j in range(i, len(numbers)):
            numbers = list(numbers)
            numbers[i], numbers[j] = numbers[j], numbers[i] 
            self.permutationNumbers(numbers, i + 1)

    def removeDuplicate(self, temp_list):
        new_list = []
        for i in temp_list:
            if i not in new_list: 
                new_list.append(i)
        return new_list

    def combinationOperators(self):
        operator = self.operators
        for i in operator:
            for j in operator:
                for k in operator:
                    self.listOperators.append([i,j,k])
        
    def concatenate(self):
        for numbers in self.listNumbers: 
            for operators in self.listOperators: 
                temp_list = []
                for i in range(len(numbers)):
                    temp_list.append(numbers[i])
                    if(i != 3):
                        temp_list.append(operators[i])
                self.listConcatenate.append(temp_list)
    
    def addPosibleBracketAndToString(self):
        for i in self.listConcatenate:
            self.listCombination.append("(({} {} {}) {} {}) {} {}".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            self.listCombination.append("({} {} ({} {} {})) {} {}".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            self.listCombination.append("{} {} (({} {} {}) {} {})".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            self.listCombination.append("{} {} ({} {} ({} {} {}))".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            self.listCombination.append("({} {} {}) {} ({} {} {})".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))

    def getCombination(self, numbers):
        self.permutationNumbers(numbers)
        self.listNumbers = self.removeDuplicate(self.listNumbers)
        self.combinationOperators()
        self.concatenate()
        self.addPosibleBracketAndToString()
        return self.listCombination 
#endregion

#region CALCULATE
class calculate:
    def __init__(self):
        self.stack = []
        self.top = -1
        self.operators = set(['+', '-', '*', '/', '(', ')'])
        self.priority = {'+':1, '-':1, '*':2, '/':2}

    def pop(self):
        if self.top ==-1:
            return
        else:
            self.top-= 1
            return self.stack.pop()

    def push(self, i):
        self.top+= 1
        self.stack.append(i)

    def prepareString(self, expression):
        expression = expression.replace(" ","")
        string = ""
        for i in expression:
            if(i not in ["+","-","*","/","(",")"]):
                string += i
            elif(i == "("):
                string += "{} ".format(i)
            elif(i == ")"):
                string += " {}".format(i)
            else:        
                string += " {} ".format(i)
        return string

    def infixToPostfix(self, expression):
        expression = self.prepareString(expression) 
        expression = expression.split(" ")
        stack = [] 
        output = '' 
        for character in expression:
            if character not in self.operators:  
                output+= character + " "
            elif character=='(':  
                stack.append('(')
            elif character==')':
                while stack and stack[-1]!= '(':
                    output+= stack.pop() + " "
                stack.pop()
            else: 
                while stack and stack[-1]!='(' and self.priority[character]<=self.priority[stack[-1]]:
                    output+=stack.pop() + " "
                stack.append(character) 
        while stack:
            output+=stack.pop() + " "
        return output
  
    def postfixCalculation(self, expression):
        for i in expression:
            try:
                self.push(int(i))
            except ValueError:
                val1 = self.pop()
                val2 = self.pop()
                if(i == '/'):
                    if(val1 != 0):
                        self.push(val2 / val1)
                    else:
                        self.push(0)
                elif(i in self.operators):        
                    calculation ={'+':val2 + val1, '-':val2 - val1, '*':val2 * val1}
                    self.push(calculation.get(i))
                elif(val2 == None):
                    self.push(val1)
        return str(round(self.pop(),3))

    def getResult(self, expression):
        postfix = self.infixToPostfix(expression.replace(" ",""))
        charPostfix = postfix.split(" ")
        resultPostfix = self.postfixCalculation(charPostfix)
        return resultPostfix

    def getAllCorrectResultAndExpression(self, listExpression):
        temp_list = []
        for expression in listExpression:
            resultPostfix = self.getResult(expression)
            if(resultPostfix == "24" or resultPostfix == "24.0"):
                temp_list.append(expression + " = 24")
        return temp_list

    def getAllResultAndExpression(self, listExpression):
        temp_list = []
        for expression in listExpression:
            resultPostfix = self.getResult(expression)
            resultPostfix = resultPostfix
            temp_list.append(expression + " = " + resultPostfix)    
        return temp_list
#endregion

#region DATA
class data:
    def __init__(self):
        self.selection_color = 5
        self.enable_color = 254
        self.disable_color = 9 
        self.list_filter_all = []
        self.list_filter_o = []
        self.list_filter_x = []
        self.length_all = 0
        self.length_o = 0
        self.length_x = 0

    def check_data(self):
        if os.path.isfile('data.pin'):
            file = open('data.pin', 'rb')
            o_data = pickle.load(file)
            file.close()
            self.selection_color = o_data.selection_color
            self.enable_color = o_data.enable_color
            self.disable_color = o_data.disable_color
            self.list_filter_all = o_data.list_filter_all
            self.list_filter_o = o_data.list_filter_o
            self.list_filter_x = o_data.list_filter_x
            self.length_all = o_data.length_all
            self.length_o = o_data.length_o
            self.length_x = o_data.length_x
            return True
        else:
            return False

    def save_data(o_data):
        file = open("data.pin","wb")
        pickle.dump(o_data, file)
        file.close()
#endregion

#region INTERFACE
class interface:
    def __init__(self):
            self.version = '1.0'
            self.width = '119'
            self.height = '40'
            self.list_menu = {
                'Home'              : ['Solver', 'Show all numbers', 'Settings', 'Abouts', 'Exit'],
                'Solver'            : ['Input', 'Get all combinations', 'Get all correct combinations', 'Back'],
                'Show all numbers'  : ['All', 'Filter: O', 'Filter: X', 'Back'],
                'Settings'          : ['Selection color', 'Enabled color', 'Disabled color', 'Restore default', 'Back'],
                'Abouts'            : ['Back'],
                'Exit'              : ['Yes', 'No']
                }
            self.text_logo = text = (
                ' ██████╗ █████╗ ██╗     ██╗   ██╗███████╗██████╗   ██████╗   ██╗██╗\n'+
                '██╔════╝██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗  ╚════██╗ ██╔╝██║\n'+
                '╚█████╗ ██║  ██║██║     ╚██╗ ██╔╝█████╗  ██████╔╝    ███╔═╝██╔╝ ██║\n'+
                ' ╚═══██╗██║  ██║██║      ╚████╔╝ ██╔══╝  ██╔══██╗  ██╔══╝  ███████║\n'+
                '██████╔╝╚█████╔╝███████╗  ╚██╔╝  ███████╗██║  ██║  ███████╗╚════██║\n'+
                '╚═════╝  ╚════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ╚══════╝     ╚═╝\n'
            )
            self.data = data()
            self.filter = 'All'
            self.start = 0
            self.stop = 31
            self.max_length = 31
            self.scroll = 0
            self.temp_scroll = 0
            self.current_line = 0
            self.temp_current_line = 0
            self.current_menu = 'Home'
            self.current_display = 'Menu'
            self.status_get = False
            self.number = '____'
            self.result = [[],[]]
            self.list_combination = []
            self.type = 0
            self.length_all_numbers = 0
            self.solver_event = ''
            self.solution = False
            self.exit = False

    def display_welcome(self, screen):
        text = self.text_logo
        listLine = list(text.split("\n"))
        y = 0
        x = 45
        for i, line in enumerate(listLine):
            y = 3 + i
            screen.addstr(y, x, line, self.use_color(self.data.selection_color)) 
        screen.addstr(y + 1, x, 'Welcome to Solver 24, now you can solve all problems in game 24 :v.',  self.use_color(self.data.selection_color)) 

    def background(self, screen):
        text = self.text_logo
        y = 0
        h, w = screen.getmaxyx()
        listLine = list(text.split("\n"))
        for i, line in enumerate(listLine):
            x = w//2 - len(line)//2
            y = h//3 - len(listLine)//2 + 3 + i
            screen.addstr(y, x, line, self.use_color(self.data.selection_color))   

    def intro(self, screen):
        try:  
            text = ['Welcome to Solver 24','Press any key to continue ...']
            
            while True:
                self.background(screen)
                h, w = screen.getmaxyx()
                for i in range(len(text)):
                    x = w//2 - len(text[i])//2
                    y = h//2 + 2 + i
                    screen.addstr(y, x, f" {text[i]} ", self.use_color(self.data.selection_color)) 
                screen.addstr(h-1, w-4, self.version, self.use_color(self.data.selection_color)) 
                
                key = screen.getch()

                if key != 546:
                    break
                else:
                    screen.clear()
                    os.system(f'mode con cols={self.width} lines={self.height}')
        except Exception as e:
            print('Error in intro')

    def color(self):
        for i in range(0,255):
            curses.init_pair(i+1, i, curses.COLOR_BLACK)

    def use_color(self, a):
        if a < 256:
            return curses.color_pair(a)
        if a == 256:
            return curses.COLOR_WHITE

    def print_color(self, screen):
        screen.addstr(3, 41, '─'*75)
        screen.addstr(5, 41, '─'*75)
        r = 6
        c = 44
        for i in range(0,255):
            screen.addstr(r, c, str(i+1), curses.color_pair(i+1))
            r += 1
            if r == 23:
                r = 6
                if len(str(i)) == 2:
                    c += 4
                else:
                    c += 5
    
    def print_abouts(self,screen):
        selection_color = self.use_color(self.data.selection_color)
        enable_color = self.use_color(self.data.enable_color)
        text = ('Credit:Δ\n'+
                'Made by   : Kevin Wijaya\n'+
                'Instagram : _kevinwijaya\n'+
                '\n'+
                'Description:Δ\n'+
                'Solver 24 is a solver for game 24 written using python curses library.\n'+
                'if you find an error, or an idea what feature to add, contact me at   \n'+
                'instagram.com/_kevinwijaya                                            \n'+
                 '\n'+                                    
                'Version 1.0Δ\n'+
                '[-] First release in 22/8/2022\n')
        text = text.split('\n')
        y = 1
        x = 41
        for i in text:
            y += 1
            if('Δ' in list(i)):
                screen.addstr(y, x, i[:-1], selection_color)
            else:
                screen.addstr(y, x, i, enable_color)

    def input(self, screen):
        list_number = ['_','_','_','_']
        screen.addstr(4, 41, 'Enter 4 digit number: ____',self.use_color(self.data.enable_color))
        i = 0
        while True:
            key = screen.getch()
            if i > 0 and key == 8:
                i -= 1 
                list_number[i] = '_'
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
            #developer only :v
            #elif key == 27:
                #break
            try:
                if i < 4 and list_number[i] == '_':
                    list_number[i] = str(int(chr(key)))
                    i += 1 
            except:
                pass
            for j in range(len(list_number)):
                screen.addstr(4, 63 + j, list_number[j],self.use_color(self.data.enable_color))

        string = ''
        for i in list_number:
            string += i

        if '_' not in list(string):
            self.number = string
    
    def input_color(self, screen, old_color):
        screen.addstr(4, 41, 'Enter 1-255 number to change color: ___',self.use_color(self.data.enable_color))
        list_number = ['_','_','_']
        i = 0
        while True:
            key = screen.getch()
            if i > 0 and key == 8:
                i -= 1 
                list_number[i] = '_'
            elif key == curses.KEY_ENTER or key in [10, 13]:
                break
            #developer only :v
            #elif key == 27:
                #break
            try:
                if i < 3 and list_number[i] == '_':
                    number = str(int(chr(key)))
                    list_number[i] = number
                    i += 1 
                
            except:
                pass
            for j in range(len(list_number)):
                screen.addstr(4, 77 + j, list_number[j],self.use_color(self.data.enable_color))

        string = ''
        for i in list_number:
            string += i

        screen.addstr(4, 41, '                                       ')
        if '___' != string and int(string.replace('_','')) < 256 and int(string.replace('_','')) > 0 :
            return int(string.replace('_',''))
        else:
            return old_color

    def get_result(self):
        number = self.number
        if number != '____':
            comb = combination()
            calc = calculate()
            listExpression = comb.getCombination(number)
            self.result = [calc.getAllResultAndExpression(listExpression),calc.getAllCorrectResultAndExpression(listExpression)]
        else:
            self.result = [[],[]]

    def get_list_combination(self):
        type = 0
        k = 0
        string = ''
        temp_list = []
        list_result = self.result
        if self.solver_event == 'All Combinations' : type = 0
        elif self.solver_event == 'Correct Only Combinations': type = 1
        result = list_result[type]
        for i in range(len(result)):
            if i%2==0 and i>0:
                temp_list.append(string)
                string = ''
                k += 1
            elif i>0:
                string += ' '
            expression = result[i].split(' = ')
            string += f"│ {i+1:>4} │ {expression[0]} │ {expression[1]:>6} │"
        if string != '': temp_list.append(string)

        self.type = type
        self.list_combination = temp_list

    def check_filter(self, filter):
        match filter:
            case 'All':
                print(filter)
                return self.data.length_all, self.data.list_filter_all
            case 'Filter: O':
                print(filter)
                return self.data.length_o, self.data.list_filter_o
            case 'Filter: X':
                print(filter)
                return self.data.length_x, self.data.list_filter_x
            case default:
                return 0, []     

    def print_table(self, screen):
        selection_color = self.use_color(self.data.selection_color)
        enable_color = self.use_color(self.data.enable_color)
        k = 1
        type = 0
        result = []
        screen.addstr(3, 41, '─'*75)
        screen.addstr(5, 41, '─'*75)
        if self.current_menu == 'Solver':
            type = self.type
            result = self.list_combination
            screen.addstr(4, 41,f'Result: {len(self.result[type])} ',enable_color)
            screen.addstr(4, 54,f' │ Type: {self.solver_event}',enable_color)
            screen.addstr(6, 41, '│  No  │    Expression     │ Result │ │  No  │     Expression    │ Result │',enable_color)
        
        elif self.current_menu == 'Show all numbers':
            length = self.length_all_numbers
            result = self.list_combination
            type_filter = self.filter
            if type_filter == 'All': type_filter = 'Type: All'
            screen.addstr(4, 41,f'Result: {length} ',enable_color)
            screen.addstr(4, 54,f' │ {type_filter}',enable_color)
            screen.addstr(6, 41, ('│ Number │  O/X  │ '*4)[:-1],enable_color)
        
        for i in range(self.start, self.stop):
            if i == self.scroll and self.current_display == 'Display':
                screen.addstr(6 + k, 41, result[i], selection_color)
            else:
                screen.addstr(6 + k, 41, result[i],enable_color)
            k += 1

    def print_layout_menu(self, screen):
        h, w = screen.getmaxyx()
        game_name = ' Solver 24 '
        output = ' Output '
        current_menu = f' {self.current_menu} '
        selection_color = self.use_color(self.data.selection_color)

        rectangle(screen, 0, 1, h-1, w-2)
        screen.addstr(0, w//2 - len(game_name)//2, game_name, selection_color)
        
        rectangle(screen, 1, 2, h-2, 39)
        screen.addstr(1, 40//2 - len(current_menu)//2, current_menu, selection_color)
    
        rectangle(screen, 1, 40, h-2, w-3)
        screen.addstr(1,(53 + 100)//2 - len(output)//2, output, selection_color)
        
    def preview_used_color(self, screen):
        if self.current_menu == 'Settings':
            screen.addstr(2, 41, '                                    ')
            if self.current_line == 0:
                screen.addstr(2, 41, 'Selection color  :', self.use_color(self.data.enable_color))
                screen.addstr(2, 60, str(self.data.selection_color), self.use_color(self.data.selection_color))
            elif self.current_line == 1:
                screen.addstr(2, 41, 'Enabled color    :', self.use_color(self.data.enable_color))
                screen.addstr(2, 60, str(self.data.enable_color), self.use_color(self.data.enable_color))
            elif self.current_line == 2:
                screen.addstr(2, 41, 'Disabled color   :', self.use_color(self.data.enable_color))
                screen.addstr(2, 60, str(self.data.disable_color), self.use_color(self.data.disable_color))

    def print_menu(self, screen):
        data = self.data
        for i, line in enumerate(self.list_menu[self.current_menu]):
            x = 3
            y = i + 2
            if i == self.current_line:
                line = f"> {line} <"
                screen.addstr(y, x, line, self.use_color(data.selection_color))
                self.preview_used_color(screen)
            elif line in ['Get all combinations', 'Get all correct combinations'] and self.number == '____':
                line = f"  {line}  "
                screen.addstr(y, x, line, self.use_color(data.disable_color))
            else:
                line = f"  {line}  "
                screen.addstr(y, x, line, self.use_color(data.enable_color))

    def print_output(self, screen):
        enable_color = self.use_color(self.data.enable_color)
        if self.current_menu == 'Home':
            self.display_welcome(screen)        
            
        elif self.current_menu == 'Solver':
            screen.addstr(2, 41, f'Number in memory: {self.number}',enable_color)
            screen.addstr(3, 41, '─'*75)   
            if self.solution == False and self.solver_event != '':
                screen.addstr(4, 41, 'Result: 0',enable_color)
                screen.addstr(4, 54,f'│ Type: {self.solver_event}',enable_color)
                screen.addstr(5, 41, '─'*75)
                screen.addstr(6, 41, 'No solution')

            elif self.result != [] and self.status_get == True:
                self.print_table(screen)

        elif self.current_menu == 'Show all numbers':
            if self.result != [] and self.status_get == True and self.list_combination != []:
                self.print_table(screen)
            else:
                screen.addstr(2, 41, 'No solution, Missing file { data.pin }')

        elif self.current_menu == 'Settings':
            self.print_color(screen)

        elif self.current_menu == 'Abouts':
            self.print_abouts(screen) 
  
    def enter_menu(self, screen):
        enable_color = self.use_color(self.data.enable_color)
        current_line = self.current_line
        current_menu = self.current_menu
        number = self.number
        result = self.result
        enter = False
        self.status_get = False
        self.stop = 31
        self.solution = False
        self.solver_event = ''
        
        option = self.list_menu[current_menu]
        if current_menu == 'Home':
            if option[current_line] == 'Solver':
                enter = True
            elif option[current_line] == 'Show all numbers':
                self.status_get = True
                self.solution = True
                enter = True
                self.length_all_numbers, self.list_combination = self.check_filter(self.filter)
            elif option[current_line] == 'Settings':
                screen.clear()
                self.print_layout_menu(screen)
                enter = True
            elif option[current_line] == 'Abouts':
                enter = True
            elif option[current_line] == 'Exit':
                enter = True

        elif current_menu == 'Solver':
            if option[current_line] == 'Input':
                screen.clear()
                self.print_layout_menu(screen)
                self.print_menu(screen)
                screen.addstr(2, 41, f'Number in memory: {number}', enable_color)
                screen.addstr(3, 41, '─'*75)

                self.input(screen)
                self.get_result()

            elif option[current_line] == 'Get all combinations' and result != [[],[]]:
                self.solver_event = 'All Combinations'
                if len(result[0]) > 0:
                    self.get_list_combination()
                    self.status_get = True
                    self.solution = True

                    if math.ceil(len(result[0])/2) < 31:
                        self.stop = math.ceil(len(result[0])/2)
                
                else:
                    self.solution = False

            elif option[current_line] == 'Get all correct combinations' and result != [[],[]]:
                self.solver_event = 'Correct Only Combinations'
                if len(result[1]) > 0:
                    self.get_list_combination()
                    self.status_get = True
                    self.solution = True
                    
                    if math.ceil(len(result[1])/2) < 31:
                        self.stop = math.ceil(len(result[1])/2)

                else:
                    self.solution = False

            elif option[current_line] == 'Back':
                self.current_menu = 'Home'
                self.current_line = 0
                self.solver_event = ''
            
        elif current_menu == 'Show all numbers':
            if option[current_line] == 'Back':
                self.current_menu = 'Home'
                self.current_line = 1
                self.filter = 'All'
            
            else:
                self.filter = option[current_line]
                self.length_all_numbers, self.list_combination = self.check_filter(self.filter)
                self.status_get = True
                self.solution = True

        elif current_menu == 'Settings': 
            if option[current_line] == 'Selection color':
                old_color = self.data.selection_color
                self.data.selection_color = self.input_color(screen, old_color)
                data.save_data(self.data)

            elif option[current_line] == 'Enabled color':
                old_color = self.data.enable_color
                self.data.enable_color = self.input_color(screen, old_color)
                data.save_data(self.data)

            elif option[current_line] == 'Disabled color':
                old_color = self.data.disable_color
                self.data.disable_color = self.input_color(screen, old_color)
                data.save_data(self.data)
            
            elif option[current_line] == 'Restore default':
                self.data.selection_color = 5
                self.data.enable_color = 254
                self.data.disable_color = 9
                data.save_data(self.data)
            
            elif option[current_line] == 'Back':
                self.current_menu = 'Home'
                self.current_line = 2

        elif current_menu == 'Abouts':
            if option[current_line] == 'Back':
                self.current_menu = 'Home'
                self.current_line = 3

        elif current_menu == 'Exit':
            if option[current_line] == 'Yes':
                print("Goodbye :D")
                self.exit = True
            elif option[current_line] == 'No':
                self.current_menu = 'Home'
                self.current_line = 4

        if enter == True:
            self.current_menu = option[current_line]
            self.current_line = 0

    def run(self, screen):
        curses.curs_set(0)
        screen.nodelay(0)
        self.color()
        self.data.check_data()
        self.intro(screen)
        while not self.exit:        
            try:
                curses.curs_set(0)
                screen.nodelay(0)

                if self.current_menu != 'Settings':
                    screen.clear()
            
                self.print_layout_menu(screen)
                self.print_menu(screen)
                self.print_output(screen)

                key = screen.getch()

                #mode_developer = 'ON' 
                #if key == 27 and mode_developer == 'ON': print('Exit') ; self.exit = True

                if key == 546:
                    screen.clear()
                    os.system(f'mode con cols={self.width} lines={self.height}')

                elif key == 304:
                    break
                
                if self.current_display == 'Menu':
                    if  key == curses.KEY_UP and self.current_line > 0:
                        self.current_line -= 1
                    elif key == curses.KEY_DOWN and self.current_line < len(self.list_menu[self.current_menu])-1:     
                        self.current_line += 1
                    elif key == curses.KEY_UP and self.current_line == 0:
                        self.current_line = len(self.list_menu[self.current_menu])-1
                    elif key == curses.KEY_DOWN  and self.current_line == len(self.list_menu[self.current_menu])-1:     
                        self.current_line = 0 
                    elif key == curses.KEY_ENTER or key in [10, 13] :
                        self.start = 0
                        self.scroll = 0
                        self.temp_scroll = 0
                        self.stop = 31  
                        self.enter_menu(screen)   
                        self.max_length = self.stop
                        screen.refresh()
                    elif (key == curses.KEY_LEFT or key == curses.KEY_RIGHT) and (self.current_menu == 'Solver' or self.current_menu == 'Show all numbers') and self.solution == True :
                        self.current_display = 'Display'
                        self.temp_current_line = self.current_line
                        self.current_line = -1
                        self.scroll = self.temp_scroll
                
                elif self.current_display == 'Display':
                    if (key == curses.KEY_LEFT or key == curses.KEY_RIGHT) and (self.current_menu == 'Solver' or self.current_menu == 'Show all numbers') and self.solution == True :
                        self.current_display = 'Menu'
                        self.current_line = self.temp_current_line
                        self.temp_scroll = self.scroll
                        self.scroll = -1

                if self.current_display == 'Display':
                    if  key == curses.KEY_UP:
                        self.scroll -= 1
                    elif key == curses.KEY_DOWN: 
                        self.scroll += 1

                    #check if scroll was in bottom
                    if self.scroll == self.stop:
                        self.start += 1 
                        if self.stop == len(self.list_combination):
                            self.start = 0
                            self.stop = self.max_length
                            self.scroll = 0
                        else:
                            self.stop += 1
                    #check if scroll was in top
                    elif self.scroll == self.start-1:
                        self.start -= 1
                        self.stop -= 1
                        if self.start == -1:
                            self.start = len(self.list_combination) - self.max_length
                            self.stop = len(self.list_combination)
                            self.scroll = len(self.list_combination) - 1

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                if str(e) == 'addwstr() returned ERR':
                    print('Error when resizing screen to small')
                    print('Stop resizing the screen')
                else:
                    print(str(e)+ ' @ ' +str(exc_type)+ str(fname)+ str(exc_tb.tb_lineno))
                self.exit = True
#endregion

#region MAIN
if __name__ == '__main__':
    start_apps = interface()
    if start_apps.data.check_data() == False:
        with open('data.pin', 'wb') as f: f.write((requests.get("https://github.com/kevin-wijaya/Solver-24/raw/main/data.pin")).content)
        print('Download data.pin from repository github.com/kevin-wijaya/solver-24')
    os.system(f'mode con cols={start_apps.width} lines={start_apps.height}')
    curses.wrapper(start_apps.run)
#endregion