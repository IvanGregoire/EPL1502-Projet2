R = [217, 500, 227, 510]
V_P = [0.543, 0.947, 0.5878, 0.9473]
V_0 = 1.081 * 2
def Rth(V_0, V):
    n = []
    m = 0
    for i in range(len(V)):
        n.append((V_0*R[i]-V[i]*R[i])/V[i])
    print(n)
    for i in n:
        m+=i
    return m/len(n)

        

print(f"{Rth(V_0, V_P)} ohms")