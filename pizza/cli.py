import argparse

desc = "Pizza - An HTML bulk email utility"

# Initialize parser
parser = argparse.ArgumentParser(description=desc)

# Adding optional argument
parser.add_argument("-i", "--interactive",
                    help="Lauch Pizza in interactive mode", action='store_true')
# parser.add_argument("-t", '--template', help="Load email template from file")
# parser.add_argument("-a", "--all", help="Send the email to all the contacts")

# Read arguments from command line
args = parser.parse_args()


def display():
    """
    CLI screen in interactive mode
    """
    display = """
1) Send mail
2) Add new mail template
3) Add recipients
4) Quit
    """
    print(display)


def handle_interactive():
    """
    Handles the cli in interactive mode.
    """
    display()
    user_in = input("-> ")


if args.interactive:
    handle_interactive()
