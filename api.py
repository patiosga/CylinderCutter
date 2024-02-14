import itertools

#w = 1500  # πλάτος ρολού σε mm
#total_weight = 2000  # συνολικό βάρος σε kg
# weight_factor = total_weight / w  # kg/mm

#possible_cuts = [145, 165, 185, 250, 280]  # όλα τα δυνατά μήκη κομματιών σε mm

# dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
# for cut in possible_cuts:
#     dic[cut] = cut * weight_factor  # kg of its cut


def valid_combinations(w, possible_cuts):
    valid_solutions = []
    for i in range(1, 20):  # δεν ειναι δυνατο να εχει πανω απο 20 κομματια
        for combination in itertools.combinations_with_replacement(possible_cuts, i):  # r-μεταθεσεις οπου r=1, 2, ..., 14
            temp_sum = sum(combination)
            if temp_sum <= w:  # οι συνδυασμοι που εχουν μήκος μικροτερο ή ισο με το w
                valid_solutions.append([combination, w - temp_sum])

    return valid_solutions


def get_number_of_single_cut(solution, cut):  # πλήθος των κομματιων που εχουν το μηκος cut
    return solution.count(cut)


def mother_func(w, total_weight, possible_cuts, n):
    weight_factor = total_weight / w  # kg/mm
    dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
    for cut in possible_cuts:
        dic[cut] = cut * weight_factor  # kg of each cut

    solutions = valid_combinations(w, possible_cuts)

    solutions = sorted(solutions, key=lambda x: x[1])  # ταξινόμηση με βάση το μήκος που απομένει

    solutions = solutions[:n]  # πρώτες n λύσεις

    for solution in solutions:  # υπολογισμός βάρους όλων των κομματιών του εκάστοτε μήκους στον εκάστοτε συνδυασμό
        weights_dic = {}
        for cut in possible_cuts:
            num = get_number_of_single_cut(solution[0], cut)
            cut_weight = dic[cut] * num
            weights_dic[cut] = round(cut_weight)  # στρογγυλοποίηση στον πλησιέστερο ακέραιο
        solution.append(weights_dic)

    return solutions


# Εξαγωγή σε αρχείο csv
import csv

def csv_export(solutions, possible_cuts, filename):
    #filename = 'for_dad.csv'  # αμα θες να αλλάξεις το όνομα του αρχείου αλλάξε το εδώ (πριν την τελεία, το .csv είναι απαραίτητο)

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='/')  # '/' για να διαχωρίζονται οι τιμές στο excel

        # columns
        columns = ['Combination']
        for cut in possible_cuts:
            columns.append(cut)
        columns.append('Remaining Length')  # remaining length στο τελος
        writer.writerow(columns)
        
        # rows
        for solution in solutions:
            final_row = []

            combination = solution[0]
            final_row.append(combination)

            weights = solution[2]
            for cut in possible_cuts:
                final_row.append(weights[cut])  # συνολικό βάρος κάθε κομματιού - μπαίνει με τη σωστή σειρά

            remaining_length = solution[1]
            final_row.append(remaining_length)

            writer.writerow(final_row)


def main(w, total_weight, possible_cuts, n):
    solutions = mother_func(w, total_weight, possible_cuts, n)  # n πρώτες λύσεις
    csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv


# solutions = mother_func(w, total_weight, possible_cuts, 10)  # 10 πρώτες λύσεις
# csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv