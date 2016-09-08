import adapt_skills
import inspect
import sys
import json
import os
from adapt.intent import IntentBuilder
from adapt.engine import DomainIntentDeterminationEngine

engine = DomainIntentDeterminationEngine()
skills = {}

def load_skillset(filename, skillset):
    if "domain" not in skillset:
        skillset["domain"] = filename
    engine.register_domain(skillset["domain"])
    for regex in skillset["regexes"]:
        engine.register_regex_entity(regex, domain = skillset["domain"])
    for term, words in skillset["vocab"].items():
        for word in words:
            engine.register_entity(word, term, domain = skillset["domain"])
    for skill, syntax in skillset["skills"].items():
        intent = IntentBuilder(skill)
        for item, category in syntax.items():
            if category == "required":
                intent.require(item)
            elif category == "optional":
                intent.optionally(item)
            elif category == "one_of":
                intent.one_of(item)
        engine.register_intent_parser(intent.build(), domain = skillset["domain"])
        print("Intent {} loaded".format(skill))

async def load_skills():
    [__import__('adapt_skills.'+skill) for skill in adapt_skills.__all__]
    for filename, skillset in adapt_skills.skills.items():
        load_skillset(filename, skillset)
    for skill in adapt_skills.Skill.__subclasses__():
        skills[skill.__name__] = skill(engine)
        await skills[skill.__name__].on_load()
        print("Skill {} loaded".format(skill.__name__))
