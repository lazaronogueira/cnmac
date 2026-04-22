# -*- coding: utf-8 -*-
"""
Created : 22/01/206

@author: Lazaro Nogueira Pena Neto
"""

import math

# ==============================
# Função para simular base e precisão
# ==============================
def round_base(x, base, t):
    if x == 0:
        return 0.0
    sign = 1 if x > 0 else -1
    x = abs(x)
    
    exp = int(math.floor(math.log(x, base)))
    mant = x / (base ** exp)
    
    mant_scaled = mant * (base ** (t - 1))
    mant_rounded = round(mant_scaled)
    mant_final = mant_rounded / (base ** (t - 1))
    
    return sign * mant_final * (base ** exp)

# ==============================
# Newton-Raphson com erro
# ==============================
def newton_base(f, df, x0, base, t, tol=1e-6, max_iter=20):
    x = round_base(x0, base, t)
    
    for k in range(max_iter):
        fx = round_base(f(x), base, t)
        dfx = round_base(df(x), base, t)
        
        if dfx == 0:
            break
        
        x_new = round_base(x - fx/dfx, base, t)
        
        if abs(x_new - x) < tol:
            return x_new, k+1
        
        x = x_new
    
    return x, max_iter

# ==============================
# Função teste: sqrt(2)
# ==============================
def f(x):
    return x**2 - 2

def df(x):
    return 2*x

true_value = math.sqrt(2)

# ==============================
# Parâmetros
# ==============================
bases = [2, 8, 10, 16]
t = 10
x0 = 1.0

# ==============================
# Execução
# ==============================
print("Base | Aproximação | Iterações | Erro absoluto")
print("--------------------------------------------------")

results = []

for base in bases:
    x_approx, it = newton_base(f, df, x0, base, t)
    error = abs(x_approx - true_value)
    
    print(f"{base:>4} | {x_approx:.10f} | {it:>10} | {error:.2e}")
    
    results.append((base, x_approx, it, error))
    
    
import matplotlib.pyplot as plt

def newton_history(f, df, x0, base, t, max_iter=10):
    x = round_base(x0, base, t)
    history = []
    
    for _ in range(max_iter):
        error = abs(x - true_value)
        history.append(error)
        
        fx = round_base(f(x), base, t)
        dfx = round_base(df(x), base, t)
        x = round_base(x - fx/dfx, base, t)
    
    return history

plt.figure()

for base in bases:
    hist = newton_history(f, df, x0, base, t)
    plt.plot(hist, label=f'Base {base}')

plt.yscale('log')
plt.xlabel('Iteração')
plt.ylabel('Erro absoluto')
plt.title('Convergência do método de Newton')
plt.legend()
plt.grid()

plt.show()