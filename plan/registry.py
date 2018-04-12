"""Member registry for events."""

# Package
from plan.serializable import Serializable
from plan.serializable import reference
from plan.member import Status
from plan.member import Member
from plan.requirement import Requirement


class Registry(Serializable):

    def __init__(self, members=None, requirement=None):
        super().__init__()
        self.__members = []
        self.__requirement = Requirement()

        if members is not None:
            self.members = members
        if requirement is not None:
            self.requirement = requirement

    @reference
    def members(self):
        return self.__members

    @members.setter
    def members(self, value):
        if not hasattr(value, '__iter__') or not all(isinstance(x, Member) for x in value):
            raise TypeError(f'{value} of type {type(value)} must be an iterable of Members!')

        self.__members = []
        for member in value:
            self.register(member.user, member.status)

    @reference
    def requirement(self):
        return self.__requirement

    @requirement.setter
    def requirement(self, value):
        if value is None:
            self.__requirement = Requirement()
            return

        participants = len(self.get(status=Status.PARTICIPATING))
        if isinstance(value, Requirement):
            if value < participants:
                raise ValueError(
                    f'The current number of participants: {participants} is greater than'
                    ' the new required range: {value}'
                )
            self.__requirement = value
        elif isinstance(value, int):
            self.__requirement = Requirement(value)
        else:
            raise TypeError(
                f'Invalid requirement: {value} of type: {type(value)}. Expected Requiremnt or int.'
            )

    @property
    def requirement_met(self):
        return len(self.get(status=Status.PARTICIPATING)) in self.requirement

    def register(self, user, status=Status.INVITED):
        for member in self.members:
            if user.name == member.name:
                member.user.data.update(user.data)
                member.status = status
                return member

        member = Member(user, status)
        self.__members.append(member)
        return member

    def de_register(self, user):
        if isinstance(user, Member):
            user = user.user

        for i, member in enumerate(reversed(self.members[:])):
            if member.user == user:
                self.members.remove(self.members[-i])

    def get(self, **kwargs):
        result = []
        for member in self.members:
            matches = True
            for key, value in kwargs.items():
                member_value = getattr(member, key)
                if member_value != value:
                    matches = False
                    break

            if matches:
                result.append(member)
        return result
