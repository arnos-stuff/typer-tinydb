from random import shuffle, seed
from ..utils import db, globals, where, Query, upsert_param, getKey, getValue

# use the db to find the user
# find the user in the globals table
# find the user in the users table
# add the user to the globals table
# add the user to the users table


class UpsertTest:
    
    def __init__(self, salt = 3.3, seedv=0) -> None:
        self.salt = salt
        self.txtsalt = str(salt)
        self.seed = seedv
        
        
    
    def truncate(self):
        globals.truncate()
        
    def upset_floats_clear(self):
        seed(self.seed)
        keys = list('aghwes')
        keys = [k+self.txtsalt for k in keys]
        shuffle(keys)
        values = [3.33+self.salt, 2.2+self.salt, 1.0+self.salt, -2243.221+self.salt, -2.2222222+self.salt, 4.4+self.salt]
        for k,v in zip(keys,values):
            upsert_param(param=k, value=v, obfuscate=False)
            
        assert len(globals.all()) == 6
        
    def upsert_param_avoid_duplicates(self):
        seed(self.seed)
        keys = list('aes')
        keys = [k+self.txtsalt for k in keys]
        shuffle(keys)
        values = [999+self.salt, 7777+self.salt, 2222+self.salt]
        
        for k,v in zip(keys,values):
            upsert_param(param=k, value=v, obfuscate=False)
            
        assert len(globals.all()) == 6
        
    def get_keys(self):
        seed(self.seed)
        keys = list('aes')
        keys = [k+self.txtsalt for k in keys]
        shuffle(keys)
        values = [999+self.salt, 7777+self.salt, 2222+self.salt]
        for k,v in zip(keys,values):
            assert getValue(param=k) == str(v)
    
    def add_obfuscation(self):
        prefix = 'secret-key-number-'
        words = ['one', 'two', 'three', 'BOOM']
        keys = [prefix+w for w in words]
        
        values = ['wfwef890fwe0w', 'w98w89e0789bf78', '098880988', 31243434.311278766]
        
        for k,v in zip(keys,values):
            upsert_param(param=k, value=v, obfuscate=True)
            
        for k in keys:
            assert not len(globals.search(where('param') == k)) # all keys are encrypted
        
    def decode_obfuscation(self):
        prefix = 'secret-key-number-'
        words = ['one', 'two', 'three', 'BOOM']
        keys = [prefix+w for w in words]
        
        values = ['wfwef890fwe0w', 'w98w89e0789bf78', '098880988', 31243434.311278766]
        for k,v in zip(keys,values):
            assert getValue(param=k) == str(v)

    def reset(self):
        globals.truncate()
        assert not len(globals.all())

def random_upserts(salt:float ,seedv:float):     
    test = UpsertTest(salt=salt, seedv=seedv)
    
    test.truncate()
    test.upset_floats_clear()
    test.upsert_param_avoid_duplicates()
    test.get_keys()
    test.add_obfuscation()
    test.decode_obfuscation()
    test.reset()
    
salts = [1, 6, -3, 4]
seeds = [12, 0, 232]

# for i,salt in enumerate(salts):
#     for j,seedv in enumerate(seeds):
#         print(f'def test_random_upserts_num{i}x{j}():\n    random_upserts(salt={salt}, seedv={seedv})')
        
def test_random_upserts_num0x0():
    random_upserts(salt=1, seedv=12)
def test_random_upserts_num0x1():
    random_upserts(salt=1, seedv=0)
def test_random_upserts_num0x2():
    random_upserts(salt=1, seedv=232)
def test_random_upserts_num1x0():
    random_upserts(salt=6, seedv=12)
def test_random_upserts_num1x1():
    random_upserts(salt=6, seedv=0)
def test_random_upserts_num1x2():
    random_upserts(salt=6, seedv=232)
def test_random_upserts_num2x0():
    random_upserts(salt=-3, seedv=12)
def test_random_upserts_num2x1():
    random_upserts(salt=-3, seedv=0)
def test_random_upserts_num2x2():
    random_upserts(salt=-3, seedv=232)
def test_random_upserts_num3x0():
    random_upserts(salt=4, seedv=12)
def test_random_upserts_num3x1():
    random_upserts(salt=4, seedv=0)
def test_random_upserts_num3x2():
    random_upserts(salt=4, seedv=232)
def test_random_upserts_num0x0():
    random_upserts(salt=1, seedv=12)
def test_random_upserts_num0x1():
    random_upserts(salt=1, seedv=0)
def test_random_upserts_num0x2():
    random_upserts(salt=1, seedv=232)
def test_random_upserts_num1x0():
    random_upserts(salt=6, seedv=12)
def test_random_upserts_num1x1():
    random_upserts(salt=6, seedv=0)
def test_random_upserts_num1x2():
    random_upserts(salt=6, seedv=232)
def test_random_upserts_num2x0():
    random_upserts(salt=-3, seedv=12)
def test_random_upserts_num2x1():
    random_upserts(salt=-3, seedv=0)
def test_random_upserts_num2x2():
    random_upserts(salt=-3, seedv=232)
def test_random_upserts_num3x0():
    random_upserts(salt=4, seedv=12)
def test_random_upserts_num3x1():
    random_upserts(salt=4, seedv=0)
def test_random_upserts_num3x2():
    random_upserts(salt=4, seedv=232)