from abc import ABCMeta, abstractmethod

class Skill(object, metaclass=ABCMeta):
    """
    Superclass for AdaptBot skills. Any skill must DIRECTLY subclass this skill.
    E.g. `MySkill(Skill):`

    Attributes:
        engine: The active parser engine (from Adapt) that the skill is attached to

    Methods:
        async on_load(): Called when the bot loads the skill. The skill should
            add any programatic vocabulary at this point.
        async parse():
    """

    def __init__(self, engine):
        self.engine = engine # Store engine so skill can programatically load vocab
        super().__init__()

    async def on_load(self):
        pass

    @abstractmethod
    async def parse(self, message, *args, **kwargs):
        raise TypeError("Skill must override the parse method")
