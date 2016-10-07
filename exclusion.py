from urllib.request import urlopen
from urllib.parse import urljoin
# https://github.com/seomoz/reppy
from reppy.cache import RobotsCache

# Check if robot txt allows access.
def check_robot_txt(url,agentname):
    try:
        #Access the Robot Cache
        robots = RobotsCache()
        # Check if the url is allowed to be accessed by the agent
        return robots.allowed(url, agentname)
    except:
        pass
