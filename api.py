from itertools import combinations_with_replacement
from comb import comb

#w = 1500  # πλάτος ρολού σε mm
#total_weight = 2000  # συνολικό βάρος σε kg
# weight_factor = total_weight / w  # kg/mm

#possible_cuts = [145, 165, 185, 250, 280]  # όλα τα δυνατά μήκη κομματιών σε mm

# dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
# for cut in possible_cuts:
#     dic[cut] = cut * weight_factor  # kg of its cut


def valid_combinations(width, possible_cuts, k_results=100):
    min_cut = min(possible_cuts)
    valid_solutions = [[] for _ in range(min_cut)]  # create min_cut buckets --> a cut cannot have a remaining length greater or equal than the minimum cut length
    for i in range(1, 15):  # δεν ειναι δυνατο να εχει πανω απο 15 κομματια
        for combination in combinations_with_replacement(possible_cuts, i):  # r-μεταθεσεις οπου r=1, 2, ..., 14
            temp_sum = sum(combination)
            remaining_length = width - temp_sum
            if temp_sum <= width and remaining_length < min_cut:  # combinations should have a sum less than or equal to the width and the remaining length should be less than the minimum cut length
                temp_comb = comb(combination, remaining_length)  # combination object
                valid_solutions[temp_comb.remaining_length].append(temp_comb)  # add the combination to the corresponding bucket
    
    # flatten the buckets until we get k_results valid solutions
    flattened_solutions = []
    for bucket in valid_solutions:
        flattened_solutions.extend(bucket)
        if len(flattened_solutions) >= k_results:
            break

    return flattened_solutions[:k_results]  # return the first k_results valid solutions


def get_number_of_single_cut(solution, cut):  # πλήθος των κομματιων που εχουν το μηκος cut
    return solution.count(cut)


def mother_func(w, total_weight, possible_cuts, n: int):
    '''
    w: int, πλάτος ρολού σε mm
    total_weight: int, συνολικό βάρος κυλίνδρου σε kg
    possible_cuts: list[int], όλα τα δυνατά μήκη κομματιών σε mm
    n: int, ο αριθμός των πρώτων λύσεων που θέλουμε να εξάγουμε
    '''
    weight_factor = total_weight / w  # kg/mm
    dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
    for cut in possible_cuts:
        dic[cut] = cut * weight_factor  # kg of each cut

    solutions = valid_combinations(w, possible_cuts, k_results=n)  # πρώτες n λύσεις με λιγότερο χαμένο χαρτί

    for solution in solutions:  # υπολογισμός βάρους όλων των κομματιών του εκάστοτε μήκους στον εκάστοτε συνδυασμό
        weights_dic = {}
        for cut in possible_cuts:
            num = get_number_of_single_cut(solution.combination, cut)
            cut_weight = dic[cut] * num
            weights_dic[cut] = round(cut_weight)  # στρογγυλοποίηση στον πλησιέστερο ακέραιο
        solution.set_weights(weights_dic)

    return solutions


# Εξαγωγή σε αρχείο excel
# import csv
import time
from pandas import DataFrame

def excel_export(solutions: list[comb], possible_cuts, filename):
    # Create a DataFrame to store the data
    data = {'Combination': [], 'Remaining Length': []}
    for cut in possible_cuts:
        data[cut] = []

    # Populate the DataFrame with the solution data
    for solution in solutions:
        data['Combination'].append(solution.combination)
        data['Remaining Length'].append(solution.remaining_length)
        weights = solution.weights
        for cut in possible_cuts:
            data[cut].append(weights[cut])

    # Create a Pandas DataFrame from the data
    df = DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)

# Call the excel_export function in the main function
def main(w, total_weight, possible_cuts, n):
    start_time = time.time()

    solutions = mother_func(w, total_weight, possible_cuts, n)  # n πρώτες λύσεις
    excel_export(solutions, possible_cuts, 'for_dad.xlsx')  # εξαγωγή σε αρχείο Excel

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


# def main(w, total_weight, possible_cuts, n):
#     start_time = time.time()

#     solutions = mother_func(w, total_weight, possible_cuts, n)  # n πρώτες λύσεις
#     csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv

#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Execution time: {execution_time} seconds")
    

# solutions = mother_func(w, total_weight, possible_cuts, 10)  # 10 πρώτες λύσεις
# csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv