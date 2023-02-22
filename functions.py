import os

def get_mean():
    while True:
        try:
            mean = float(input('Enter the mean for the normal distribution:'))
            break
        except ValueError:
            print('Please insert a number.')
    return mean

def get_stddev():
    while True:
        try:
            stddev = float(input('Enter the standard deviation for the normal distribution:'))
            break
        except ValueError:
            print('Please insert a number.')
    return stddev
