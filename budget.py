def personal_allowance(model, income):
    reduction = 0.0
    
    if income > 100000:
        reduction += (income - 100000) / 2
        
    return max(model["base_allowance"] - reduction, 0)

def income_tax(model, income, personal_allowance):
    
    basic_rate_band = model["basic_rate_band"]
    higher_rate_band = model["higher_rate_band"]
    
    income_above_allowance = max(income - personal_allowance, 0)
    
    basic_rate_amount = min(income_above_allowance, basic_rate_band)
    higher_rate_amount = max(min(income_above_allowance, higher_rate_band) - basic_rate_band, 0)
    additional_rate_amount = max(income_above_allowance - higher_rate_band, 0)
    
    tax_amount = basic_rate_amount * 0.2 + higher_rate_amount * 0.4 + additional_rate_amount * 0.45
    
    return tax_amount

def ni(model, income):
    
    ni_threshold = model["ni_threshold"]
    ni_reduced = model["ni_reduced"]
    
    ni_amount = max(min(income, ni_reduced) - ni_threshold, 0)
    ni_reduced_amount = max(income - ni_reduced, 0)
    
    return ni_amount * 0.12 + ni_reduced_amount * 0.02
    
def total_tax(model, income):
    return income_tax(model, income, personal_allowance(model, income)) + ni(model, income)
    
def take_home(income):
    return income - total_tax(income)
    
def after_tax_incomes():
    incomes = range(1, 200000, 5)
    after = [i - total_tax(i) for i in incomes]
    
    plt.plot(incomes, after)
    plt.show()
    
def effective_rate():
    incomes = range(1, 200000, 5)
    after = [(total_tax(i) / i) * 100.0 for i in incomes]

    plt.plot(incomes, after)
    plt.show()

def percentiles_calc():
    percentiles = [8370,8670,8970,9260,9570,9880,10200,10500,10700,10900,11100,11300,11600,11800,12000,12200,12400,12700,12900,13100,13300,13500,13800,14000,14200,14500,14700,14900,15200,15400,15700,15900,16100,16400,16700,16900,17200,17500,17700,18000,18300,18600,18800,19100,19400,19700,20000,20400,20700,21000,21400,21700,22100,22400,22800,23200,23500,23900,24300,24800,25200,25600,26100,26500,27000,27500,28100,28600,29100,29700,30300,30900,31500,32200,32900,33600,34300,35100,35900,36700,37700,38700,39700,40700,41800,42800,44100,45600,47200,49200,51500,54300,57700,62000,67900,76100,88000,106000,150000]

    import numpy as np
    from scipy.optimize import curve_fit
    from scipy.integrate import quad

    x = np.array(range(1, len(percentiles)+1))
    y = np.array(percentiles)

    z = np.polyfit(x,y,100)
    f = np.poly1d(z)

    plt.plot(range(0, 101), [f(i) for i in range(0, 101)])
    plt.plot(range(0, 101), [net(f(i)) for i in range(0, 101)])

    print f(0)
    print f(50)
    print f(100)

    def fn(x):
        return f(x) - net(f(x))

    result = quad(fn, 0.0, 100.0)
    print result[0] * (29300000 / 100)
    
def income_change():
    incomes = [8370,8670,8970,9260,9570,9880,10200,10500,10700,10900,11100,11300,11600,11800,12000,12200,12400,12700,12900,13100,13300,13500,13800,14000,14200,14500,14700,14900,15200,15400,15700,15900,16100,16400,16700,16900,17200,17500,17700,18000,18300,18600,18800,19100,19400,19700,20000,20400,20700,21000,21400,21700,22100,22400,22800,23200,23500,23900,24300,24800,25200,25600,26100,26500,27000,27500,28100,28600,29100,29700,30300,30900,31500,32200,32900,33600,34300,35100,35900,36700,37700,38700,39700,40700,41800,42800,44100,45600,47200,49200,51500,54300,57700,62000,67900,76100,88000,106000,150000]
    
    model15 = {"base_allowance": 10600.0, "basic_rate_band": 31785.0, "higher_rate_band" : 150000.0, "ni_threshold" : 7956.0, "ni_reduced": 41865.0}
    model17 = {"base_allowance": 11500.0, "basic_rate_band": 33500.0, "higher_rate_band" : 150000.0, "ni_threshold" : 7956.0, "ni_reduced": 41865.0}
    
    tax15 = [total_tax(model15, i) for i in incomes]
    tax17 = [total_tax(model17, i) for i in incomes]
    
    print tax15
    print tax17
    
    change = []
    change_percent = []

    for i in range(0, len(incomes)):
        change.append(tax15[i] - tax17[i])
        percent_change = (change[i] / (incomes[i]-tax15[i]) * 100.0)
        change_percent.append(percent_change)
        
    plt.plot(range(1,len(incomes)+1), change)
    plt.show()
    plt.plot(range(1,len(incomes)+1), change_percent)
    plt.show()
    
income_change()

        