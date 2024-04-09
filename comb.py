from functools import total_ordering

@total_ordering
class comb: 
  
  # constructor 
    def __init__(self, combination: tuple, remaining_length: float): 
        self.combination = combination 
        self.remaining_length = remaining_length  # multiply with (-1) to have it work as a max heap
  
   # override the comparison operator 
    def __lt__(self, nxt): 
        return self.remaining_length < nxt.remaining_length 
    
    def __eq__(self, other):
        return self.remaining_length == other.remaining_length
    
    def set_weights(self, weights: dict):
        self.weights = weights

    def __str__(self) -> str:
        return f"Combination: {self.combination}, Remaining Length: {self.remaining_length}"