import requests
from pprint import pprint
import json


"""
fetch("https://character-service.dndbeyond.com/character/v5/character/25755022?includeCustomItems=true", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjEwMTY4MTQ5MyIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiJ1c2VyLTEwMTY4MTQ5MyIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2VtYWlsYWRkcmVzcyI6Im1heGltZS5ib25uaW5AZ214LmRlIiwiZGlzcGxheU5hbWUiOiJUaGVCb3lzIiwiYXZhdGFyVXJsIjoiaHR0cHM6Ly93d3cuZG5kYmV5b25kLmNvbS9hdmF0YXJzL3RodW1ibmFpbHMvMzE1NDkvNzI0LzEwMC8xMDAvNjM4MDkyOTI5NDE2MDE2NTgzLnBuZyIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IlJlZ2lzdGVyZWQgVXNlcnMiLCJodHRwOi8vc2NoZW1hcy5kbmRiZXlvbmQuY29tL3dzLzIwMTkvMDgvaWRlbnRpdHkvY2xhaW1zL3N1YnNjcmliZXIiOiJUcnVlIiwiaHR0cDovL3NjaGVtYXMuZG5kYmV5b25kLmNvbS93cy8yMDE5LzA4L2lkZW50aXR5L2NsYWltcy9zdWJzY3JpcHRpb250aWVyIjoiTWFzdGVyIiwibmJmIjoxNzA1MzQzMDkyLCJleHAiOjE3MDUzNDMzOTIsImlzcyI6ImRuZGJleW9uZC5jb20iLCJhdWQiOiJkbmRiZXlvbmQuY29tIn0.Y3KYX6R5mEn-gof8JKfvCIq6Tuv5HzlPyPXTw6DnMVk",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Opera\";v=\"106\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://www.dndbeyond.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});
"""



def get_character(id):

    r = requests.get("https://character-service.dndbeyond.com/character/v5/character/" + id + "?includeCustomItems=true")
    

    print(r.status_code)
    data_dict = r.json()

    # pprint(data_dict)

    with open("sample_5.json", "w") as f:
        f.write(json.dumps(data_dict, indent=2))

    return data_dict



wanted = {
    "id": None,
    "name": None,
    "baseHitPoints": None,
    "alignmentId": None,
    "stats": {
        "STR": None,
        "DEX": None,
        "CON": None,
        "INT": None,
        "WIS": None,
        "CHA": None,
    },
    "bonusStats": {
        "STR": None,
        "DEX": None,
        "CON": None,
        "INT": None,
        "WIS": None,
        "CHA": None,
    },
    "overrideStats": None,
    "hasCustomBackground": None,
    "background": None,
    "race": {
        "isSubRace": None,
        "baseRaceName": None,
        "fullName": None,
        "isHomebrew": None,
        "isLegacy": None,
        "racialTraits": [
            {
                "id": None,
                "name": None,
                "choices": []
            }
        ]
    },
    "preferences": {
      "useHomebrewContent": None,
      "progressionType": None,
      "encumbranceType": None,
      "hitPointType": None,
      "privacyType": None,
      "sharingType": None,
      "abilityScoreDisplayType": None,
      "enforceFeatRules": None,
      "enforceMulticlassRules": None,
      "enableDarkMode": None,
      "startingEquipmentType": None,
      "abilityScoreType": None,
    },
    "lifestyle": None,
    "inventory": [
        {
          "magic": None,
          "name": None,
          "type": None,
          "rarity": None,
          "isHomebrew": None
        }
    ],
    "currencies": {
      "cp": None,
      "sp": None,
      "gp": None,
      "ep": None,
      "pp": None
    },
    "classes": [
        {
            "level": None, 
            "isStartingClass": None,
            "name": None,
            "isHomebrew": None,
            "subclassDefinition": {
                "name": None,
                "isHomebrew": None,
                "subclassTraits": [
                    {
                        "id": None,
                        "name": None,
                        "choices": [
                            None
                        ]
                    }
            ]
            },
            "classTraits": [
                {
                    "id": None,
                    "name": None,
                    "choices": [
                        None
                    ]
                }
            ]
        }
    ],
    "feats": [
        {
            "name": None,
            "isHomebrew": None
        }
    ],
    "activeSourceCategories": [],
    "spells": [],
    "customItems": [],
    "dateModified": None,
    "providedFrom": None,
    "statusSlug": None,
}



def main():
    print("Starting...")
    vlad = "25755022"
    char = get_character(vlad)
    pprint(char)








if __name__ == "__main__":
    main()