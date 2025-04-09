# flatten(lst)        Flattens the list 
                    # ie input = [1,2,3, [1,2,3,[3,4],2]]
                    # output = [1,2,3,1,2,3,3,4,2]
                    


nested=[1,2,3, [1,2,3,[3,4],2]]

def flatten_list(nested):
    flat=[]
    for sublist in nested:
        if isinstance(sublist,list):
            flat.extend(flatten_list(sublist))
        else:
            flat.append(sublist)
    return flat


final_output=flatten_list(nested)
print(final_output)