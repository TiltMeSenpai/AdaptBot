import adapt_skills
import inspect
import sys
import json
from adapt.intent import IntentBuilder
from adapt.engine import DomainIntentDeterminationEngine

engine = DomainIntentDeterminationEngine()

def split_optionals(function):
    args = inspect.getargspec(function)
    optionals = args.defaults
    return (args.args[:-len(optionals)], args.args[len(optionals)+1:])

def load_intent(skill):
    domain = getattr(skill[1], "domain", skill[0])
    engine.register_domain(domain)
    for key in skill[1].spec:
        key = key.strip('?')
        if not hasattr(skill[1], key):
            print("Vocab for "+key+" not found. Not loading")
            return
    intent = IntentBuilder(skill[0])
    for key in skill[1].spec:
        if key.endswith('?'):
            intent = intent.optionally(key.strip('?'))
        else:
            intent = intent.require(key)
        for keyword in getattr(skill[1], key.strip('?')):
            engine.register_entity(keyword, key, domain=domain)
    intent = intent.build()
    engine.register_intent_parser(intent, domain=domain)
    print("Successfully loaded "+skill[0])

def load_skill(skill):
    module = sys.modules[__name__]
    args = split_optionals(skill[1].parse)
    for arg in skill[1].spec:
        if arg.endswith('?'):
            arg = arg.strip('?')
            if arg in args[1]:
                args[1].remove(arg)
            else:
                print("Optional "+arg+" not found in "+module[0]+". Not loading.")
                return
        else:
            if arg in args[0]:
                args[0].remove(arg)
            else:
                print("Required "+arg+" not found in "+module[0]+". Not loading.")
                return
    if len(args[0]) == 0 and len(args[1]) == 0:
        setattr(module, skill[0], skill[1])
        load_intent(skill)
        return True
    if len(args[0]) > 0:
        print("Missing required "+str(args[0])+" from "+skill[0]+" spec. Not loading.")
    if len(args[1]) > 0:
        print("Missing optional "+str(args[1])+" from "+skill[0]+" spec. Not loading.")

def load_skills():
    [__import__('adapt_skills.'+skill) for skill in adapt_skills.__all__]
    skills = []
    for module in inspect.getmembers(adapt_skills, inspect.ismodule):
        if module[0].endswith("Skill"):
            load_skill(module)
