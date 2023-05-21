from ebnflib.read_yaml.read import reads
from ebnflib.write_yaml.write import writes
# This has been moved to ebnflib.write_yaml.write


def main():
    import sys
    filename = sys.argv[1]
    with open(filename) as reader:
        source = reader.read()
    tree = reads(source)
    source2 = writes(tree)
    print(source2)


if __name__ == '__main__':
    main()
