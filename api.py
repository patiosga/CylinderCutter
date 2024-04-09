import itertools
import heapq
from comb import comb

#w = 1500  # πλάτος ρολού σε mm
#total_weight = 2000  # συνολικό βάρος σε kg
# weight_factor = total_weight / w  # kg/mm

#possible_cuts = [145, 165, 185, 250, 280]  # όλα τα δυνατά μήκη κομματιών σε mm

# dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
# for cut in possible_cuts:
#     dic[cut] = cut * weight_factor  # kg of its cut


def add_to_heap(heap, item: comb, max_size): # min heap that has the negative remaining_lenght of the combinations and hence is used as a max heap
    if len(heap) < max_size: # If the heap is not full, add the item
        heapq.heappush(heap, item)
    elif heap[0].__lt__(item):
        # If the negative weight of the worst (junk-wise) combination (top element)
        # is smaller (larger by abs) replace it with the new item
        heapq.heappushpop(heap, item)


def heap_sort(heap):  # but alternative (redoes the weights to be positive and reverses the list)
    # Initialize an empty list to store the sorted elements
    sorted_arr = []
    # Loop through the heap, extracting the smallest element and appending it to the sorted list
    while True:
        try:
            popped: comb = heapq.heappop(heap)
            popped.remaining_length *= (-1)  # multiply with (-1) to reverse the damage done by the necessity of max heap
            sorted_arr.append(popped)

        except IndexError:  # empty heap
            break

    # Reverse the list to get the elements in ascending order
    sorted_arr.reverse()
    # Return the sorted list
    return sorted_arr


def valid_combinations(width, possible_cuts, max_size):
    valid_solutions = []
    heapq.heapify(valid_solutions)  # binary heap
    for i in range(1, 20):  # δεν ειναι δυνατο να εχει πανω απο 20 κομματια
        for combination in itertools.combinations_with_replacement(possible_cuts, i):  # r-μεταθεσεις οπου r=1, 2, ..., 14
            temp_sum = sum(combination)
            if temp_sum <= width:  # οι συνδυασμοι που εχουν μήκος μικροτερο ή ισο με το width
                # Heap implementation
                temp_comb = comb(combination, (-1) * (width - temp_sum))  # combination object
                add_to_heap(valid_solutions, temp_comb, max_size)
                # multiply with (-1) to have it work as a max heap

                # Implementation without heap
                # valid_solutions.append(comb(combination, width - temp_sum))
    return valid_solutions


def get_number_of_single_cut(solution, cut):  # πλήθος των κομματιων που εχουν το μηκος cut
    return solution.count(cut)


def mother_func(w, total_weight, possible_cuts, n: int):
    weight_factor = total_weight / w  # kg/mm
    dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
    for cut in possible_cuts:
        dic[cut] = cut * weight_factor  # kg of each cut

    solutions = valid_combinations(w, possible_cuts, n)


    # Heap implementation
    solutions: list[comb] = heap_sort(solutions)  # sort the top-k elements heap

    # Implementation without heap
    # solutions = sorted(solutions, key=lambda x: x.remaining_length)  # ταξινόμηση με βάση το μήκος που απομένει

    # solutions = solutions[:n]  # πρώτες n λύσεις

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
import pandas as pd

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
    df = pd.DataFrame(data)

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