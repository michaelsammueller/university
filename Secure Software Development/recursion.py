# Recursion Problem - The Towers of Hanoi
def solve_towers(n):
    # If only one disk is left to be moved, record one move.
    if n == 1:
        return 1
    # Otherwise, try to solve the problem for 'n-1' disks.
    # Multiply it by to to account for the move to an intermediary rod.
    # Increment by one to account for moving the largest disk.
    else:
        return 2 * solve_towers(n - 1) + 1


print(solve_towers(987))

# The theoretical maximum of disks that can be moved without an error is 1000,
# due to the maximum recursion depth of Python.
# The practical maximum turned out to be 987, which is when the interpreter returned
# a RecursionError.

# To ensure security, the input to the function should be limited to a maximum of 987 or lower,
# to avoid a system crash due to a stack overflow. For example:

def solve_towers_secure(n):
    # Check input size
    if n > 987:
        return "Error: Input too large."
    elif n == 1:
        return 1
    else:
        return 2 * solve_towers_secure(n - 1) + 1
    
print(solve_towers_secure(1000))
# Output: Error: Input too large.

# Alternatively, we can ignore user input if it exceeds the maximum allowed value.
def solve_towers_ignore(n):
    # Limit the input size:
    n = min(n, 987)

    if n == 1:
        return 1
    else:
        return 2 * solve_towers_ignore(n - 1) + 1

print(solve_towers_ignore(1000))
# If the input value exceeds the maximum allowed value, the function will ignore it and
# use the maximum allowed value instead.