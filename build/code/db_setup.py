
from src.app import create_app
from src.db import *
import src.config as config


def create_roles():
    role1 = Role(name=Name("admin"))
    role1.save()

    role2 = Role(name=Name("user"))
    role2.save()

def create_admin_user():
    user = User(name=Name("Admin User"),
                email=Email("xyz@gmail.com"),
                role=Role.get_by_id(1))
    user.save()

if __name__ == "__main__":
    db.create_all(app=create_app(config))
    create_roles()
    create_admin_user()
