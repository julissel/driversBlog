from driversBlog import Base, session
from driversBlog.models_interaction import select_all_users, find_tag, all_user_posts_with_2tags, create_data


if __name__ == "__main__":
    try:
        # create_all() создание всех таблиц в бд
        Base.metadata.create_all()
        # заполнение данными
        create_data()
        # выбор списка всех пользователей
        select_all_users()
        # поиск тэга в таблице тэгов по названию
        find_tag("каршеринг")
        find_tag("трейд-ин")
        # поиск всех постов заданного пользователя, имеющих два заданных тэга
        all_user_posts_with_2tags("alex981", tag1='статистика', tag2='производители авто')

        session.close()

    except Exception as e:
        print("Возникла ошибка:", e)
