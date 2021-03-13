"""
This file (test_user_creation.py) contains the unit tests for the models.py file.
"""
from sqlalchemy import func
from driversBlog.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the fullname, nickname, level_id, active and date_registration are defined correctly
    """

    new_user_nickname = 'test_user_nickname'
    new_user_fullname = 'test_user_fullname'
    new_user_level = 0
    new_user_active = True
    new_date_registration = func.now()

    user = User(nickname=new_user_nickname, fullname=new_user_fullname,
                active=new_user_active, level_id=new_user_level,
                date_registration=new_date_registration)

    assert user.fullname == new_user_fullname
    assert user.nickname == new_user_nickname
    assert user.level_id == new_user_level
    assert user.active == new_user_active
    assert user.date_registration == new_date_registration
