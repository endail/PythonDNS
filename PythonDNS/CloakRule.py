import re

class CloakRule():

    def __init__(self, regex, target):
        self.regex = regex
        self.target = target

    def search(self, test):
        return bool(self.regex.search(test))

    @classmethod
    def importRules(self, file):

        rules = []

        with open(file, 'r') as rdr:
            for line in rdr:

                line = line.strip()

                if len(line) == 0 or line[0] == "#":
                    continue

                parts = line.split(None, 2)

                if len(parts) != 2:
                    continue

                try:
                    rule = self(re.compile(parts[0]), parts[1])
                except re.error:
                    continue

                rules.append(rule)

        return rules