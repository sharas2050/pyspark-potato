import argparse

CLI = argparse.ArgumentParser()
CLI.add_argument(
    "--customers",  # name on the CLI - drop the `--` for positional/required parameters
    nargs="*",  # 0 or more values expected => creates a list
    type=int,
    default=[1, 2, 3],  # default if nothing is provided
)
CLI.add_argument(
    "--counters",
    type=int
)


args = CLI.parse_args()

customer = args.customers
counters = args.counters


print("customers: %r" % args.customers)
print("counters: %r" % args.counters)


def computecheckouttime(customers, n):
    counters = [0] * n
    for i in customers:
        counters[0] += i
        # print(counters)
        counters.sort()
    return max(counters)


result = computecheckouttime(customer, counters)
print("Total time required to check out: %r" % result)

# print("computeCheckoutTime([5,3,4], 1)")
# print(computecheckouttime([5, 3, 4], 1))
#
# print("computeCheckoutTime([10,2,3,3], 2)")
# print(computecheckouttime([10, 2, 3, 3], 2))
#
# print("computeCheckoutTime([2,3,10], 2)")
# print(computecheckouttime([2, 3, 10], 2))
