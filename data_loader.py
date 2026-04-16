import xml.etree.ElementTree as ET
import pandas as pd                                                                                                                                                                                                      
                  
ALL_SKILLS = [
      "Shooting", "Melee", "Construction", "Mining", "Cooking",
      "Plants", "Animals", "Crafting", "Artistic", "Medicine",                                                                                                                                                             
      "Social", "Intellectual"                                                                                                                                                                                             
  ]                                                                                                                                                                                                                        
                                                                                                                                                                                                                           
                                                                                                                                                                                                                           
def load_colonist_data(rws_path: str):
    tree = ET.parse(rws_path)                                                                                                                                                                                            
    root = tree.getroot()
    things = root.find("game/maps/li/things")
    pawns = things.findall(".//thing[@Class='Pawn'][kindDef='Colonist']")                                                                                                                                                
  
    pawn_list = []                                                                                                                                                                                                       
    skill_list = []
    traits_list = []                                                                                                                                                                                                     

    for pawn_id, pawn in enumerate(pawns):                                                                                                                                                                               
        first = pawn.findtext("name/first")
        last = pawn.findtext("name/last")

        pawn_list.append({"pawn_id": pawn_id, "first": first, "last": last})                                                                                                                                             

        skills = {                                                                                                                                                                                                       
            s.findtext("def"): s.findtext("level") or 0
            for s in pawn.findall("skills/skills/li")                                                                                                                                                                    
        }
        for skill_name in ALL_SKILLS:                                                                                                                                                                                    
            skill_list.append({                                                                                                                                                                                          
                "pawn_id": pawn_id,
                "skill": skill_name,                                                                                                                                                                                     
                "level": skills.get(skill_name, 0)
            })

        traits = pawn.findall("story/traits/allTraits/li")
        if traits:
            for trait in traits:
                traits_list.append({                                                                                                                                                                                     
                    "pawn_id": pawn_id,
                    "first": first,                                                                                                                                                                                      
                    "last": last,
                    "trait": trait.findtext("def"),
                    "degree": int(trait.findtext("degree") or 0)
                })                                                                                                                                                                                                       
        else:
            traits_list.append({                                                                                                                                                                                         
                "pawn_id": pawn_id,
                "first": first,
                "last": last,
                "trait": "None",
                "degree": 0
            })
                                                                                                                                                                                                                        
    pawns_df = pd.DataFrame(pawn_list)
                                                                                                                                                                                                                        
    skills_df = pd.DataFrame(skill_list)
    skills_df["level"] = skills_df["level"].astype(int)

    merged_df = pd.merge(pawns_df, skills_df, on="pawn_id", how="inner")                                                                                                                                                 

    pivot_df = merged_df.pivot(index="first", columns="skill", values="level").astype(int)                                                                                                                               
                
    traits_df = pd.DataFrame(traits_list)                                                                                                                                                                                
                
    return pawns_df, skills_df, merged_df, pivot_df, traits_df