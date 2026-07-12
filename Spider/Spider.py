import argparse


def spider():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url from the website you want to extract images")
    parser.add_argument("-r", help="recursively downloads the images", action="store_true")
    parser.add_argument("-l", "--level", type=int, default=None)
    parser.add_argument("-p", "--path", type=str, default="./data/")
    args = parser.parse_args()
    if args.level is not None and not args.r:
        parser.error("-l need to be used with -r")
    elif args.r and args.level is None:
        args.level = 5
    print(vars(args))


if __name__ == "__main__":
    spider()
