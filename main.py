from sys import modules, getrecursionlimit
from inspect import getsourcelines

labelMap = {}
goto_count = 0  # Initialize a counter for goto calls

def label(l):
    # Get the source code of the current module
    sourceCode, _ = getsourcelines(modules['__main__'])

    # Possible variants for different types of string literals
    variants = [
        f"label('{l}')",  # single quotes
        f'label("{l}")',  # double quotes
        f"label(f'{l}')",  # f-string (single quotes)
        f'label(f"{l}")',  # f-string (double quotes)
        f"label(r'{l}')",  # raw string (single quotes)
        f'label(r"{l}")',  # raw string (double quotes)
    ]

    # Find the line that matches one of the label variants
    try:
        match = [item for item in sourceCode if any(variant in item for variant in variants)][0]
    except IndexError:
        print("You've not used the label function correctly :/")
        return

    # Get the line number of the matching label and store it in labelMap
    matchLine = sourceCode.index(match) + 1
    labelMap[l] = matchLine

def goto(l, i=0):
    global goto_count
    goto_count += 1  # Increment the goto counter

    # Check if the recursion limit is exceeded
    if goto_count > getrecursionlimit():
        print("Error: Recursion limit exceeded.")
        return

    try:
        labelLine = labelMap[l]
    except KeyError:
        print(f"Label {l} is not defined.")
        return

    # Get the source code of the current module
    sourceCode, _ = getsourcelines(modules['__main__'])

    # Possible variants for different types of string literals (spaces removed)
    variants = [
        f"goto('{l}',{i})".replace(" ", ""),  # single quotes
        f'goto("{l}",{i})'.replace(" ", ""),  # double quotes
        f"goto(f'{l}',{i})".replace(" ", ""),  # f-string (single quotes)
        f'goto(f"{l}",{i})'.replace(" ", ""),  # f-string (double quotes)
        f"goto(r'{l}',{i})".replace(" ", ""),  # raw string (single quotes)
        f'goto(r"{l}",{i})'.replace(" ", ""),  # raw string (double quotes)
        # Without {i}
        f"goto('{l}')".replace(" ", ""),  # single quotes
        f'goto("{l}")'.replace(" ", ""),  # double quotes
        f"goto(f'{l}')".replace(" ", ""),  # f-string (single quotes)
        f'goto(f"{l}")'.replace(" ", ""),  # f-string (double quotes)
        f"goto(r'{l}')".replace(" ", ""),  # raw string (single quotes)
        f'goto(r"{l}")'.replace(" ", ""),  # raw string (double quotes)
    ]

    # Normalize source lines by removing spaces
    normalized_source = [line.replace(" ", "") for line in sourceCode]
    # Find all matches
    try: 
        match = ([item for item in normalized_source if any(variant in item for variant in variants)][i]).replace(" ", "")
    except IndexError:
        print("You've not used the goto function correctly :/")
        return

    matchGotoLine = normalized_source.index(match) + 1


    # Check if goto is after the label
    if matchGotoLine <= labelLine:
        print("Error: Goto statement is before the label.")
        return

    # Execute all code from the label line to the matchGotoLine
    affectedLines = '\n'.join(sourceCode[labelLine - 1:matchGotoLine])
    exec(affectedLines, modules['__main__'].__dict__)




# Example usage
# The loopholes having to be jumped through in the example are also perfect evidence that structured programming is better.

doAgain = True # Do again statement must be set before the label to prevent from being run again, else would run into issues with infinite recursion.
label('Start first loop')
count = 0
label('Start second loop') 
count += 1

print('GOTO STATEMENTS ARE AWFUL')
if count < 3:
    goto('Start second loop')

if (doAgain == True):
    doAgain = False
    goto('Start first loop')

    print('Finished')