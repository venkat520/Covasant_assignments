 # Converts like below 
                    # input = [[[ '(0,1,2)' , '(3,4,5)'], ['(5,6,7)' , '(9,4,2)']]]
                    # output = [[[[0,1,2],[3,4,5]],[[5,6,7],[9,4,2]]]]
                    
                    

input = [[[ '(0,1,2)' , '(3,4,5)'], ['(5,6,7)' , '(9,4,2)']]]

def converts(input):
    if isinstance(input,str):
        return [int(y) for y in input.strip('()').split(',')]
    elif isinstance(input,list):
        return [converts(item) for item in input]
    else:
        return input
        
        
op=converts(input)
print(op)


