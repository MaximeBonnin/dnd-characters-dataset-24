import time

def parse_character(reponse_tuple:tuple) -> dict:

    char_id, status_code, data = reponse_tuple
    #print(f"Parsing {char_id}")

    # guard clause if fail
    if status_code != 200:
        failed_dict = {
            "char_id": char_id,
            "status_code": status_code
        }
        return failed_dict


    # status = 200
    response_data : dict = data["data"]
    out = {}

    out["char_id"] = char_id
    out["status_code"] = status_code
    out["name"] = response_data.get("name")

    out["baseHitPoints"] = response_data.get("baseHitPoints")
    out["bonusHitPoints"] = response_data.get("bonusHitPoints")
    out["overrideHitPoints"] = response_data.get("overrideHitPoints")

    out["currentXp"] = response_data.get("currentXp")
    out["alignmentId"] = response_data.get("alignmentId")

    for x in ["stats", "bonusStats", "overrideStats"]:
        out[x] = {}
        out[x]["STR"] = int(response_data.get(x)[0]["value"] or 0)
        out[x]["DEX"] = int(response_data.get(x)[1]["value"] or 0)
        out[x]["CON"] = int(response_data.get(x)[2]["value"] or 0)
        out[x]["INT"] = int(response_data.get(x)[3]["value"] or 0)
        out[x]["WIS"] = int(response_data.get(x)[4]["value"] or 0)
        out[x]["CHA"] = int(response_data.get(x)[5]["value"] or 0)

    # background 
    if response_data.get("background"):
        out["background"] = {
            "hasCustomBackground": response_data["background"].get("hasCustomBackground"),
            "backgroundFeatures": []
        }
        if response_data["background"].get("definition"):
            out["background"]["name"] = response_data["background"]["definition"].get("name")

        if response_data["background"].get("hasCustomBackground"):
            out["background"]["name"] = response_data["background"]["customBackground"].get("name")

        for bg_feature in response_data["modifiers"].get("background", []):
            values = {
                "name": bg_feature.get("subType", "") + " " + bg_feature.get("type", ""),
                "type": bg_feature.get("type"),
                "subType": bg_feature.get("subType")
            }
            out["background"]["backgroundFeatures"].append(values)

        if not  out["background"]["backgroundFeatures"]:
             out["background"].pop("backgroundFeatures")

        

    # race (should be renamed probably)
    if response_data.get("race"):
        out["race"] = {
            "isSubRace": response_data["race"].get("isSubRace"),
            "baseRaceName": response_data["race"].get("baseRaceName"),
            "subRaceShortName": response_data["race"].get("subRaceShortName"),
            "fullName": response_data["race"].get("fullName"),
            "isHomebrew": response_data["race"].get("isHomebrew"),
            "isLegacy": response_data["race"].get("isLegacy"),
            "racialTraits": []
        }

        for trait in response_data["race"].get("racialTraits", []):
            traint_def = {
                "id": trait["definition"].get("id"), 
                "name": trait["definition"].get("name"),
                "choices": []
            }

            for choice in response_data["modifiers"].get("race", []):
                if choice.get("componentId") == trait["definition"].get("id"):
                    choice_values = {
                            "name": choice.get("subType", "") + " " + choice.get("type", ""),
                            "type": choice.get("type"),
                            "subType": choice.get("subType")
                        }
                    traint_def["choices"].append(choice_values)

            if not traint_def["choices"]:
                traint_def.pop("choices")

            out["race"]["racialTraits"].append(traint_def)

    out["preferences"] = response_data.get("preferences")
    out["lifestyle"] = response_data.get("lifestyle")

    # inventory
    out["inventory"] = []
    for item in response_data.get("inventory", []):
        item_dict = {
            "magic": item["definition"].get("magic"),
            "name": item["definition"].get("name"),
            "type": item["definition"].get("type"),
            "rarity": item["definition"].get("rarity"),
            "isHomebrew": item["definition"].get("isHomebrew")
        }
        out["inventory"].append(item_dict)

    out["currencies"] = response_data.get("currencies")

    # classes
    out["classes"] = []
    for response_class in response_data.get("classes", []):
        parsed_class = {}
        parsed_class["level"] = response_class.get("level")
        parsed_class["isStartingClass"] = response_class.get("isStartingClass")
        parsed_class["name"] = response_class["definition"].get("name")
        parsed_class["isHomebrew"] = response_class["definition"].get("isHomebrew")

        if response_class.get("subclassDefinition"):
            parsed_class["subclassDefinition"] = {
                "name": response_class["subclassDefinition"].get("name"),
                "isHomebrew": response_class["subclassDefinition"].get("isHomebrew"),
                "classFeatures": []
            }


            for feature in response_class["subclassDefinition"].get("classFeatures", []):

                classFeatures_def = {
                    "id": feature.get("id"), 
                    "name": feature.get("name"),
                    "choices": []
                }

                choice_values = {}
                # check modifiers
                for choice in response_data["modifiers"].get("class", []):
                    if choice.get("componentId") == feature.get("id"):
                        choice_values = {
                            "name": choice.get("subType", "") + " " + choice.get("type", ""),
                            "type": choice.get("type"),
                            "subType": choice.get("subType")
                        }

                        classFeatures_def["choices"].append(choice_values)

                # check options ?
                for choice in response_data["options"].get("class", []):
                    if choice.get("componentId") == feature.get("id"):
                        choice_values = {
                            "name": choice["definition"].get("name")
                        }
                        classFeatures_def["choices"].append(choice_values)

                if not classFeatures_def["choices"]:
                    classFeatures_def.pop("choices")

                #TODO this is a bit late and could be done better
                if traint_def not in parsed_class["subclassDefinition"]["classFeatures"]:
                    parsed_class["subclassDefinition"]["classFeatures"].append(classFeatures_def)

        out["classes"].append(parsed_class)


    # feats
    out["feats"] = []
    for feat in response_data.get("feats", []):
        values = {
            "name": feat["definition"].get("name"),
            "isHomebrew": feat["definition"].get("isHomebrew")
        }
        out["feats"].append(values)


    out["activeSourceCategories"] = response_data.get("activeSourceCategories")

    # spells
    out["spells"] = []
    for source in ["race", "class", "background", "item", "feat"]:
        if not response_data["spells"].get(source):
            continue

        for spell in response_data["spells"].get(source, []):
            if not spell.get("definition"):
                continue
            values = {
                "name": spell["definition"].get("name"),
                "isHomebrew": spell["definition"].get("isHomebrew"),
                "prepared": spell["definition"].get("prepared"),
                "from": source
            }
            out["spells"].append(values)

    # out["customItems"] = [] #TODO maybe add this

    out["dateModified"] = response_data.get("dateModified")
    out["providedFrom"] = response_data.get("providedFrom")
    out["statusSlug"] = response_data.get("statusSlug")
    out["scrapeTime"] = time.time()


    return out

if __name__ == "__main__":
    print("wrong file")