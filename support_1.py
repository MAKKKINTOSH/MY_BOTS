array = [1,2,3,4,5]
id = 3

array_of_numbers = [1,2,3,4,5]

def admin(func):
    def test(*args, **kwargs):
        print(args, kwargs, sep='\n')
        if args[0] in array:
            return func(*args, **kwargs)
        else:
            print("no")
    return test
@admin
def true(id_argument):
    print("congrats")

true(id)

