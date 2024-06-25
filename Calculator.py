from tkinter import * 

class Node:
    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None
    pass
    # END def __init__
# END class Node


class ExpressionTree:
    
    def __init__(self, levels):
        self.root = None
        self.levels = levels
    # END def __init__
    
    def add(self, value):
        self.root = self._add(self.root, value)
        
    # END def add
    
    def _add(self, node: Node, value):
        
        if node is None:
            return Node(value)
        else:
            levels = self.levels
            
            if levels.get(value, 0) >= levels.get(node.value, 0):
                
                newNode = Node(value)
                newNode.left = node
                
                return newNode
            else:
                
                node.right = self._add(node.right, value) 
                
                return node
    # END def _add()
    
    def calc(self):
        return self._calc(self.root)
    # END def calc
    
    def _calc(self, node):
        
        if node.left is None and node.right is None:
            return int(node.value)
        else:
            
            result = 0
            
            if node.value == '/':
                result = self._calc(node.left) / self._calc(node.right)
            elif node.value == 'x':
                result = self._calc(node.left) * self._calc(node.right)
            elif node.value == '+':
                result = self._calc(node.left) + self._calc(node.right)        
            elif node.value == '-':
                result = self._calc(node.left) - self._calc(node.right)        
            return result
        
        
    # END of def _calc()

# END class ExpressionTree

class Calculator:
    
    def __init__(self):
        
        #Configurations/Variables
        MIN_WIDTH = 300
        MIN_HEIGHT = 400
        
        MAX_WIDTH  = int(MIN_WIDTH * 1.3) #MIN_WIDTH + 30% of MIN_WIDTH
        MAX_HEIGHT = int(MIN_HEIGHT * 1.3)
        
        TOP_RATIO = 1
        MIDDLE_RATIO = 7
        BOTTOM_RATIO = 2
        
        TOP_HEIGHT = int(MIN_HEIGHT * .1) #10% of MIN_HEIGHT
        MIDDLE_HEIGHT = int(MIN_HEIGHT * .7) #70% of MIN_HEIGHT        
        BOTTOM_HEIGHT = int(MIN_HEIGHT * .2) #20% of MIN_HEIGHT       
         
        TOP_FRAME_FONT = 'Courier 22 bold'
        MIDDLE_FRAME_FONT = 'Courier 20 bold'
        BOTTOM_FRAME_FONT = 'Courier 22 bold'
        
        self.currentNumber = '0'
        self.OPERATORS_LEVEL = {
            'x' : 1,
            '/' : 1,
            '+' : 2,
            '-' : 2,
        }
        #WINDOW Code
        self.window = Tk()
        
        root = self.window
        
        root.title('Mi Calculadora')
        root.minsize(width = MIN_WIDTH, height = MIN_HEIGHT)
        root.maxsize(width = MAX_WIDTH, height = MAX_HEIGHT)
        
        
        #FRAMES - TOP, MIDDLE, and BOTTOM
        topFrame = Frame(
            root,
            width = MIN_HEIGHT,
            height = TOP_HEIGHT,
            # bg = 'red'
        )
        middleFrame = Frame(
            root,
            width = MIN_HEIGHT,
            height = MIDDLE_HEIGHT,
            #bg = 'green'
        )
        bottomFrame = Frame(
            root,
            width = MIN_HEIGHT,
            height = BOTTOM_HEIGHT,
            bg = 'blue'
        )
        # n - North   => top
        # e - East    => right
        # w - West    => left
        # s - South   => bottom
        topFrame.grid(row = 0, column = 0, sticky = 'news')
        middleFrame.grid(row = 1, column = 0, sticky = 'news')
        bottomFrame.grid(row = 2, column = 0, sticky = 'news')
        
        root.columnconfigure(0, weight = 1)
        root.rowconfigure(0, weight = TOP_RATIO) # growth ratio
        root.rowconfigure(1, weight = MIDDLE_RATIO)
        root.rowconfigure(2, weight = BOTTOM_RATIO)                
        
        #BUILD FRAMES CONTENT
        self._BuildTopFrameContent(topFrame, TOP_FRAME_FONT)
        self._BuildMiddleFrameContent(middleFrame, MIDDLE_FRAME_FONT)
        self._BuildBottomFrameContent(bottomFrame, BOTTOM_FRAME_FONT)
        #START calculator
        self.window.mainloop()
    #END def__init__
    
    def _BuildTopFrameContent(self, frame : Frame, fontConfig):
        
        self.lbl_display = Label(
            frame,
            text = '0',
            anchor = 'e', #anchor to East => right
            font = fontConfig
        )
        
        self.lbl_display.grid(row = 0, column = 0, sticky = 'e')
        
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
    #END def _BuildTopFrameContent(topFrame)
    
    def _BuildMiddleFrameContent(self, frame : Frame, fontConfig):
        
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', 'x'],
            ['1', '2', '3', '-'],
            [' ', '0', ' ', '+'],
        ]
        
        for ridx, row in enumerate(buttons):
            
            frame.rowconfigure(ridx, weight = 1)
            
            for cidx, col in enumerate(row):
                
                frame.columnconfigure(cidx, weight= 1)
                
                if col!= ' ':
                    btn = Button(
                        frame,
                        text = col,
                        font = fontConfig,
                        #command= self._ifNoLambdaWasAvailableInPython(col)
                        command= lambda x = col: self._btn_NoOp_action(x)
                    )
                    btn.grid(row = ridx, column= cidx, sticky = 'news')
            #END for cidx...
        #END for ridx...
    # END def _BuildMiddleFrameContent
    
    def _ifNoLambdaWasAvailableInPython(self, value):
        
        def _():
            print(f'Button {value} was clicked \o/')
            
        return _
        # END def _ifNoLambdaWasAvailableInPython(col)
    
    def _btn_NoOp_action(self, value):
        
        if self.lbl_display['text'] == 'Division Error':
            self.lbl_display['text'] = '0'
        
        if value.isdigit(): # number
            
            if self.currentNumber.startswith('0'): # Doesnt let number start with 0
                self.currentNumber = value
                self.lbl_display['text'] = self.lbl_display['text'][:-1]
            else:
                self.currentNumber += value
        else: # operator
            
            if not self.lbl_display['text'][-1].isdigit():
                self.lbl_display['text'] = self.lbl_display['text'][:-1]
            
            self.currentNumber = ''
            pass
        
        
        self.lbl_display['text'] += value
        
        #END of def _btn_NoOp_action
    
    def _BuildBottomFrameContent(self, frame: Frame, fontConfig):
        
        btn_clr = Button(
            frame,
            text = 'clear',
            font = fontConfig,
            command = self._btn_clr_action
        )
        btn_eq = Button(
            frame,
            text = '=',
            font = fontConfig,
            command = self._btn_eq_action
        )
        
        btn_clr.grid(row = 0, column = 0, sticky = 'news')
        btn_eq.grid(row = 0, column = 1, sticky = 'news')
        
        frame.columnconfigure(0, weight = 1)
        frame.columnconfigure(1, weight = 1)
        frame.rowconfigure(0, weight = 1)
    #END def _BuildBottomFrameContent(bottomFrame)
    
    def _btn_clr_action(self):
        
        self.lbl_display['text'] = '0'
        self.currentNumber = '0'
    # END of def _btn_clr_action
        
    def _btn_eq_action(self):
        expTree = self._BuildExpressionTree()
        
        try:
            result = str(expTree.calc())
        except ZeroDivisionError:
            result = 'Division Error'
            
        self.lbl_display['text'] = result
        self.currentNumber       = result
        
        if not result.isnumeric():
            self.currentNumber = '0'
        
        
    # END of _btn_eq_action
        
    def _BuildExpressionTree(self):
        expTree = ExpressionTree(self.OPERATORS_LEVEL)
        
        # TODO
        
        
        # get the numbers and operators from display and add to the tree
        displayExp = self.lbl_display['text']
        
        # Example: 78x2+1/23
        if not displayExp[-1].isdigit():
            displayExp = displayExp[:-1]
        
         # Example: 78x2+1/23
        numberStr = ''
        for char in displayExp:
            
            if char.isdigit():
                numberStr += char
            else:
                expTree.add(numberStr)
                numberStr = ''
                
                expTree.add(char)
                
            # END for char...
        expTree.add(numberStr)
            
        return expTree
    # END def _BuildExpressionTree
#END class Calculator

Calculator()
