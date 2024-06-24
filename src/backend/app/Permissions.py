from enum import Enum

class PERMISSIONS(Enum):
    cat_auth_group = 'Cat Auth Group'
    edit_auth_group = 'Edit Auth Group'


class AppAuthGroup(Enum):
    superuser = ('super user', 'have all system access, the highest level access')
    high_manager1 = ('high manager1', 'such as the department manager')
    high_manager2 = ('high manager2', 'such as the department manager')
    high_manager3 = ('high manager3', 'such as the department manager')
    high_manager4 = ('high manager4', 'such as the department manager')
    low_user1 = ('low user1', 'such as the on-site marketing employee, only cat the market plan')
    low_user2 = ('low user2', 'such as the on-site marketing employee, only cat the market plan')
    low_user4 = ('low user2', 'such as the on-site marketing employee, only cat the market plan')
    low_user5 = ('low user2', 'such as the on-site marketing employee, only cat the market plan')