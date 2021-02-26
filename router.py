import copy
import re

class Router:
    def __init__(self):
        self.actions = {}

    def performAction(self, route):
        return self.actions[route["action"]](route["data"])

    def applyMatches(self, route, path):
        routeCopy = copy.deepcopy(route)
        groups = re.compile(routeCopy["match"]).match(path)

        for i in range(1, re.compile(routeCopy["match"]).groups + 1):
            for key in routeCopy["data"]:
                routeCopy["data"][key] = re.sub(
                    re.compile("\\{" + str(i) + "\\}"),
                    groups[i],
                    routeCopy["data"][key]
                )

        return routeCopy

    def resolve(self, routes, path, default):
        for route in routes:
            if re.match(re.compile(route["match"]), path):
                return self.performAction(self.applyMatches(route.copy(), path))

        for route in routes:
            if re.match(re.compile(route["match"]), default):
                return self.performAction(self.applyMatches(route.copy(), path))