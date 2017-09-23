from plan.member import Status
from plan.member import Member
from plan.requirement import Requirement


class Registry:

    def __init__(self, members=None, requirement=None):
        self.__members = []
        self.__requirement = Requirement()

        if members is not None:
            self.members = members
        if requirement is not None:
            self.requirement = requirement

    @property
    def members(self):
        return self.__members

    @members.setter
    def members(self, value):
        if not hasattr(value, '__iter__') or not all(isinstance(x, Member) for x in value):
            raise TypeError('{} of type {} must be an iterable of Members!'.format(value, type(value)))

        self.__members = []
        for member in value:
            self.register(member.user, member.status)

    @property
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
                    'The current number of participants: {} is greater than the new required range: {}'
                    .format(participants, value)
                )
            self.__requirement = value
        elif isinstance(value, int):
            self.__requirement = Requirement(value)
        else:
            raise TypeError(
                'Invalid requirement: {} of type: {}. Expected Requiremnt or int.'.format(value, type(value))
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
