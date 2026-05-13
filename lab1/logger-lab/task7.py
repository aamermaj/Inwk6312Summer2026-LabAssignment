class Error(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooSmallError(Error):
    """Raised when the input value is too small"""
    pass

class ValueTooLargeError(Error):
    """Raised when the input value is too large"""
    pass

number = 10

while True:
    try:
        guess = int(input("Enter a number: "))
        if guess == number:
            break
        elif guess < number:
            raise ValueTooSmallError
        elif guess > number:
            raise ValueTooLargeError
    except ValueTooSmallError:
        print("This value is too small, try again!\n")
    except ValueTooLargeError:
        print("This value is too large, try again!\n")

print("Congratulations! You guessed it correctly.")
     
