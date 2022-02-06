'''
- Author: Zhengxiang (Jack) Wang 
- Date: 2022-02-06
- GitHub: https://github.com/jaaack-wang 
- About: A simple and easy-to-use program to help you 
find candidate words for Wordle-like word games.   
'''
from os.path import exists
from random import sample


class Guesser:
    
    def __init__(self, words=None, words_path='wordle_wl.txt'):
        if words:
            assert isinstance(words, list), 'words must be a list!'
            assert all(isinstance(w, str) 
                       for w in words), 'every word in words must be a str!'
            self.words = words
        else:
            assert exists(words_path), "wordle_wl.txt does not exist." \
            + "Please specify a path to wordle word list or other word list" \
            + " stored in txt format where every line corresponds to a word."
            self.words = self._get_words(words_path)
        
        self._check_len()
        self._cands = None
    
    @staticmethod
    def _get_words(fpath):
        return [w.strip() for w in open(fpath)]
    
    def _check_len(self):
        all_len = [len(w) for w in self.words]
        all_len_set = set(all_len)
        if len(all_len_set) != 1:
            print("The word list you gave is not equally long inside. " \
                 + f"{len(all_len_set)} types of length are found: {all_len_set}")
            
            while True:
                length = input("\nPlease specify the word length for your game.")
                
                try:
                    length = int(length)
                    if length not in all_len_set:
                        print("\nThe word length you gave is not available in the word list.")
                    else:
                        print(f"\nTrimming your word list...\nBefore: {len(self.words)}")
                        self.words = list(filter(lambda x: len(x) == length, self.words))
                        print(f"Now: {len(self.words)}")
                        print("Your word list has been trimmed!")
                        break
                except:
                    print("\nWord length must be an integer!")
    
    @staticmethod
    def _find(char, pool, incl=True):
        if isinstance(char, str):
            cond = lambda x: char in x if incl else char not in x
            
        elif isinstance(char, tuple):
            assert len(char) == 2, "The condition as a tuple must have only two items!"
            assert isinstance(char[0], str) and isinstance(char[1], int), "The condition" \
            + "tuple must be (char, index) where char is a str and index is an integer."
            char, idx = char
            cond = lambda x: x[idx] == char if incl else x[idx] != char
            
        else:
            what = "inclusion" if incl else "exclusion"
            raise TypeError(f"The {what} condition must be either a str or a tuple.")
            
        return filter(cond, pool)
    
    def find_candidates(self, include=None, exclude=None):
        '''Finds candidate words given certain inclusion or/and exclusion conditions.
        
        Args:
            - include (str, tuple, or list): Inclusion conditions. When given str, finds any 
                words that include the str. When given tuple, the tuple must be (str, integer), 
                which allows the program to find any words that include the str at the given position 
                (starts from 0). When given list, the item in the list can be either a str or a tuple.
            
            - exclude (str, tuple, or list): Enclusion conditions. When given str, finds any 
                words that exclude the str. When given tuple, the tuple must be (str, integer), 
                which allows the program to find any words that exclude the str at the given position
                (starts from 0). When given list, the item in the list can be either a str or a tuple.
                
        Returns:
            Candidate words. 
        '''
        
        def do(cond, incl):            
            if isinstance(cond, (str, tuple)):
                cond = [cond]
            elif isinstance(cond, list):
                pass
            else:
                what = "include" if incl else "exclude"
                raise TypeError(f"{what} must be a str or a list of str")
            
            for c in cond:
                self._cands = self._find(c, self._cands, incl)
        
        assert any((include, exclude)), "No inclusion or exclusion conditions were given!"
        self._cands = self.words.copy()
        
        if include:
            do(include, True)
        if exclude:
            do(exclude, False)
        
        self._cands = list(self._cands)
        return self._cands
    
    def exclusive(self, words=None):
        if not words:
            words = self.words
        return list(filter(lambda x: len(x)==len(set(x)), words))
    
    def random_guess(self, out_num=1):
        pool = self.exclusive(self._cands)
        if out_num == 1:
            return sample(pool, out_num)[0]
        
        elif out_num > len(pool):
            return pool
        
        else:
            return sample(pool, out_num)
    
    def __call__(self, include=None, exclude=None):
        return self.find_candidates(include, exclude)
