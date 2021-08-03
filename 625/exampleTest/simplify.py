from sympy import symbols, Or, Not, And, srepr

x, y = symbols('x y')
f = Or(Not(y), And(y, Not(x))) # or f = ~y | (y & ~x)

print(f) # ~y | (y & ~x)
print(f.simplify()) # ~x | ~y
print(srepr(f)) # Or(Not(Symbol('y')), And(Symbol('y'), Not(Symbol('x'))))
print(srepr(f.simplify())) # Or(Not(Symbol('x')), Not(Symbol('y')))




