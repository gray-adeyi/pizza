import argparse

desc = "Pizza - An HTML bulk email utility"

# Initialize parser
parser = argparse.ArgumentParser(description=desc)

# Adding optional argument
parser.add_argument("-i", "--interactive",
                    help="Lauch Pizza in interactive mode")
parser.add_argument("-t", '--template', help="Load email template from file")
parser.add_argument("-a", "--all", help="Send the email to all the contacts")

# Read arguments from command line
args = parser.parse_args()
