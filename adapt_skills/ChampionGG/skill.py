from .. import Skill
from tabulate import tabulate
import requests
import secrets

class RoleSkill(Skill):
    async def parse(self, message, lane, best="best", number=5, question=None):
        if lane == "bot": lane = "adc"
        if lane == "mid": lane = "middle"
        if best in ["best", "top"]:
            url = "http://api.champion.gg/stats/role/{}/bestPerformance?api_key={}&page=1&limit={}".format(
                lane, secrets.champion_gg, number)
        else:
            url = "http://api.champion.gg/stats/role/{}/worstPerformance?api_key={}&page=1&limit={}".format(
                    lane, secrets.champion_gg, number)
        print(url)
        champs = requests.get(url).json()
        data = [["#", "Name", "Win Percent", "Play Percent", "Ban Rate"]]
        for i, champ in enumerate(champs["data"]):
            data.append([i, champ["name"], champ["general"]["winPercent"],
                champ["general"]["playPercent"], champ["general"]["banRate"]])
        return tabulate(data, headers="firstrow")
