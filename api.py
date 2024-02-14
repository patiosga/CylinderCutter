import itertools

# w = 2000  # πλάτος ρολού σε mm
# total_weight = 2000  # συνολικό βάρος σε kg
all_cylinders = ((1500, 2000), (900, 1200))  # όλοι οι ρόλοι σε μορφή (width, total_weight)

# weight_factor = total_weight / w  # kg/mm

possible_cuts = [145, 165, 185, 250, 280]  # όλα τα δυνατά μήκη κομματιών σε mm

# dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
# for cut in possible_cuts:
#     dic[cut] = cut * weight_factor  # kg of its cut


def valid_combinations(w, possible_cuts):
    valid_solutions = []
    for i in range(1, 18):  # δεν ειναι δυνατο να εχει πανω απο 18 κομματια
        for combination in itertools.combinations_with_replacement(possible_cuts, i):  # r-μεταθεσεις οπου r=1, 2, ..., 14
            temp_sum = sum(combination)
            if w - temp_sum <= 20 and w - temp_sum >= 0:  # οι συνδυασμοι που εχουν φύρα το πολύ 20 (!!!!!!!!!!!!!!!!! οχι πλεον)
                valid_solutions.append([combination, w - temp_sum])

    return valid_solutions


def get_number_of_single_cut(solution, cut):  # πλήθος των κομματιων που εχουν το μηκος cut
    return solution.count(cut)


def child_func(w, total_weight, possible_cuts):
     # Το λεξικό dic πρέπει να υπολογιστεί μια φορά για κάθε ρολό	
    weight_factor = total_weight / w  # kg/mm
    dic = {}  # λεξικό με τα μήκη των κομματιών και το βάρος τους
    for cut in possible_cuts:
        dic[cut] = cut * weight_factor  # kg of each cut

    temp_solutions = valid_combinations(w, possible_cuts)

    temp_solutions = sorted(temp_solutions, key=lambda x: x[1])  # ταξινόμηση με βάση το μήκος που απομένει

    # solutions = solutions[:n]  # πρώτες n λύσεις

    for solution in temp_solutions:  # υπολογισμός βάρους όλων των κομματιών του εκάστοτε μήκους στον εκάστοτε συνδυασμό
        weights_dic = {}
        for cut in possible_cuts:
            num = get_number_of_single_cut(solution[0], cut)
            cut_weight = dic[cut] * num
            weights_dic[cut] = round(cut_weight)  # στρογγυλοποίηση στον πλησιέστερο ακέραιο
        solution.append(weights_dic)

    return temp_solutions  # Λύσεις για έναν μοναδικό κύλινδρο


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


# def main(w, total_weight, possible_cuts):
#     solutions = child_func(w, possible_cuts)  # n πρώτες λύσεις
#     csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv

    
solutions = []
cylinders_dic = {}
for cylinder in all_cylinders:
    w, total_weight = cylinder
    cylinders_dic[cylinder] = child_func(w, total_weight, possible_cuts)
    solutions.append((child_func(w, total_weight, possible_cuts), cylinder))  # προσθέτω ένα tuple για κάθε ρόλο
    # Στην πρώτη θέση για κάθε ρολό έχω μια λίστα από λίστες με:
    # 1. Λίστα συνδιασμών
    # 2. Μήκος που απομένει
    # 3. Λεξικό με τα βάρη των κομματιών - συνολικά τρίτο στοιχειο της λίστας

# solutions[i][1] --> (w, total_weight) του i-οστού ρόλου
# solutions[i][0] --> λίστα με λίστες συνδυασμών για τον i-οστό ρόλο

# print(solutions, len(solutions[0][0][0]))
# print(len(all_cylinders))

for combination in itertools.combinations(solutions, len(all_cylinders)):
    print(combination)
    break




#csv_export(solutions, possible_cuts, 'for_dad.csv')  # εξαγωγή σε αρχείο csv