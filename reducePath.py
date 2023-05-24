import argparse
import string

CLI = argparse.ArgumentParser()
CLI.add_argument(
    "--path",
    nargs="*",
    type=str,
    default=["NORTH", "WEST"]
)

args = CLI.parse_args()

print("path: %r" % args.path)


def dirReduc(arr):
    if len(arr) <= 1:
        return arr

    len_old = len(arr)
    arr = checkDirection(arr)
    len_new = len(arr)

    if len_new == len_old:
        return arr
    else:
        arr = dirReduc(arr)

    return arr


def checkDirection(arr):
    if len(arr) <= 1:
        return arr
    for i in range(len(arr)):
        try:
            if (((arr[i] == 'NORTH' and arr[i + 1] == 'SOUTH') or (arr[i] == 'SOUTH' and arr[i + 1] == 'NORTH')) or
                    ((arr[i] == 'EAST' and arr[i + 1] == 'WEST') or (arr[i] == 'WEST' and arr[i + 1] == 'EAST'))):
                arr.remove(arr[i])
                arr.remove(arr[i])
                return arr
        except:
            return arr


# main_arr = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]
main_arr = args.path
main_arr = dirReduc(main_arr)
print('Final Result')
print(main_arr)
