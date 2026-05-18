class AA:
    pass 

class BB(AA):
    pass 

class CC(BB):
    pass 

print(isinstance(CC(), AA))