from sys import exit


def parseArgs(argv):
    if len(argv) > 3:
        print("Too many arguments")
        exit(1)

    if len(argv) == 1 or not argv[1]:
        workMins = 25
        print("Note: Using default Pomodoro work duration of 25 minutes")
    else:
        workMins = float(argv[1])
        print(f"Note: Using work duration of {workMins} minutes")

    if len(argv) == 2 or not argv[2]:
        breakMins = 5
        print("Note: Using default Pomodoro break duration of 5 minutes")
    else:
        breakMins = float(argv[2])
        print(f"Note: Using break duration of {breakMins} minutes")

    return workMins, breakMins
