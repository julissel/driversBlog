from sqlalchemy import or_
from driversBlog import session
from driversBlog.models import User, Tag, WritersLevel, Post, tags_for_posts_table


def create_user(nickname, fullname):
    user = User(nickname=nickname, fullname=fullname)
    session.add(user)
    print("Создан новый пользователь:", nickname, fullname)
    session.commit()
    user_id = session.query(User.id).filter_by(nickname=nickname, fullname=fullname).first()[0]
    return user_id


def create_tag(tag_name):
    tag = Tag(tag_name=tag_name)
    session.add(tag)
    print(f"Тэг '{tag}' добавлен.")
    session.commit()
    tag_id = session.query(Tag.id).filter_by(tag_name=tag_name).first()[0]
    return tag_id


def create_writers_level(level_name):
    writers_level = WritersLevel(level_name=level_name)
    session.add(writers_level)
    print(f"Добавлен уровень писателя '{writers_level}'.")
    session.commit()
    writers_level_id = session.query(WritersLevel.id).filter_by(level_name=level_name)
    return writers_level_id


def get_writers_level_id_by_level_name(level_name):
    level_id = session.query(WritersLevel.id).filter_by(level_name=level_name).first()[0]
    return level_id


def get_current_user_level(user_id):
    user_level = session.query(User.level_id).filter_by(id=user_id).first()[0]
    return user_level


def get_post_count_by_user(user_id):
    user_posts_list = session.query(Post).filter_by(user_id=user_id).all()
    post_count = len(user_posts_list)
    return post_count


def get_user_level_by_post_count(post_count):
    # level = "Эксперт" если у пользователя более 4-х постов
    if post_count >= 4:
        level_id = session.query(WritersLevel.id).filter_by(level_name="Эксперт").first()[0]
        return level_id
    # level =  "Бывалый" если у пользователя от 2-х до 4-х постов включительно
    elif 2 <= post_count < 4:
        level_id = session.query(WritersLevel.id).filter_by(level_name="Бывалый").first()[0]
        return level_id
    else:
        return 0


def update_user_level(user_id, new_user_level):
    session.query(User).filter_by(id=user_id).update({User.level_id: new_user_level})
    session.commit()
    print(f"Обновлен уровень писателя у пользователя с id={user_id}")


def calculate_user_level(user_id):
    user_level = get_current_user_level(user_id)
    admin_level = get_writers_level_id_by_level_name("Админ")
    if user_level == admin_level:
        return
    post_count = get_post_count_by_user(user_id)
    new_user_level = get_user_level_by_post_count(post_count)
    if user_level == new_user_level:
        return
    update_user_level(user_id, new_user_level)


def get_user_id_by_nickname(nickname):
    user_id = session.query(User.id).filter_by(nickname=nickname).first()[0]
    return user_id


def get_user_info_by_id(user_id):
    user_info = session.query(User).filter_by(id=user_id).first()
    return user_info.fullname, user_info.nickname, user_info.level_id, user_info.date_registration, user_info.active


def get_post_id_by_post_title(post_title):
    post_id = session.query(Post.id).filter_by(post_title=post_title).first()[0]
    return post_id


def create_post(user_id, post_title, post_text, is_published):
    post = Post(user_id=user_id, post_title=post_title, post_text=post_text, is_published=is_published)
    session.add(post)
    print(f"Пост '{post_title}' добавлен.")
    session.commit()
    # вычисление уровня для пользователя, создавшего пост
    # если кол-во постов достигло новой отметки, то update_user_level обновит уровень
    calculate_user_level(user_id)
    post_id = get_post_id_by_post_title(post_title=post_title)
    return post_id


def post_extend_with_tags_list(post_id, tags_list):
    for tag_id in tags_list:
        session.execute(tags_for_posts_table.insert().values(tag_id=tag_id, post_id=post_id))
    session.commit()


def select_all_users():
    user_list = session.query(User).all()
    print("Список пользователей:")
    for user in user_list:
        print("ФИО: ", user.fullname, ", nickname:", user.nickname, "уровень писателя:", user.level_id)


def find_tag(tag_name_for_find):
    query_result = session.query(Tag).filter_by(tag_name=tag_name_for_find).first()
    if not query_result:
        print(f"Тэг '{tag_name_for_find}' отсутствует в таблице тэгов!")
    else:
        print(f"Тэг '{tag_name_for_find}' существует в таблице тэгов!")


def all_user_posts_with_2tags(user_nickname, tag1, tag2):
    user_id = get_user_id_by_nickname(nickname=user_nickname)
    posts_items = session.query(Post.post_title, Post.post_text).join(Post.tags).join(Post.user). \
        filter(or_(Tag.tag_name == tag1, Tag.tag_name == tag2)). \
        filter(User.id == user_id).distinct()

    print(f"Посты пользователя '{user_nickname}' с тэгами '{tag1}' и '{tag2}': ")
    for post_title, post_text in posts_items:
        print(f"Пост '{post_title}':")
        print(post_text)


def create_data():
    create_writers_level(level_name="Новичок")
    create_writers_level(level_name="Бывалый")
    create_writers_level(level_name="Эксперт")
    create_writers_level(level_name="Админ")

    user_1 = create_user(nickname="alex981", fullname="Алексей Алексеев")
    user_2 = create_user(nickname="tim0n", fullname="Тимофей Тимофеев")
    user_3 = create_user(nickname="sveta178", fullname="Светлана Светланова")

    tag_0 = create_tag(tag_name="спорт")
    tag_1 = create_tag(tag_name="дрифт")
    tag_2 = create_tag(tag_name="ралли")
    tag_3 = create_tag(tag_name="электрокары")
    tag_4 = create_tag(tag_name="статистика")
    tag_5 = create_tag(tag_name="авторынок РФ")
    tag_6 = create_tag(tag_name="производители авто")
    tag_7 = create_tag(tag_name="ТОП 10")
    tag_8 = create_tag(tag_name="семейный автомобиль")
    tag_9 = create_tag(tag_name="новинки")
    tag_10 = create_tag(tag_name="каршеринг")

    post_1 = create_post(user_id=user_1, post_title="Стали известны даты заездов в Кубке РАФ.",
                         post_text="Более подробная информация по ссылке: http://www.raf.su/drifting/tekushchij-sezon",
                         is_published=True)
    post_2 = create_post(user_id=user_2, post_title="Электрический купе-кроссовер Audi e-tron Sportbac в России.",
                         post_text="Новый Sportback оснащен двумя электродвигателями, которые в обычном режиме работы "
                                   "выдают 360 л.с. и 561 Нм крутящего момента."
                                   "Двигатели питаются от комплекта аккумуляторов на 95 кВт-ч, которые при помощи "
                                   "специальной быстрой системы на 150 кВт можно подзарядить на 80% за полчаса.",
                         is_published=False)
    post_3 = create_post(user_id=user_3, post_title="Следим за результатами на этапе 'Яккима' Сортавала, "
                                                    "респ. Карелия!",
                         post_text="Более подробная информация по ссылке: http://www.raf.su/rally/tekushchij-sezon",
                         is_published=True)
    post_4 = create_post(user_id=user_1, post_title="Самые продаваемые автомобили России. Итоги 2020 года.",
                         post_text="ТОП 10 производителей за 2020г: Лада (343512 шт.), "
                                   "Kia  (201727 шт.), Hyundai (163441 шт.), Renault (128408 шт.), "
                                   "Volkswagen (105785 шт.), Skoda (94632 шт.), Toyota (91598 шт.),"
                                   "Nissan (56352 шт.), ГАЗ (51169 шт.), BMW (42721 шт.)",
                         is_published=True)
    post_5 = create_post(user_id=user_1, post_title="Самые продаваемые автомобили России. Итоги 2019 года.",
                         post_text="Лада (362356 шт.), Kia (225901 шт.), Hyundai (179124 шт.), Renault (144989 шт.),"
                                   "Volkswagen (111989 шт.), Toyota (103597 шт.), Skoda (88609 шт.), "
                                   "Nissan (64974 шт.), ГАЗ (63910 шт.), Mercedes-Benz (43627 шт.)",
                         is_published=True)
    post_6 = create_post(user_id=user_2, post_title="Новые налоги для автопроизводства в России.",
                         post_text="Новые налоги",
                         is_published=True)
    post_7 = create_post(user_id=user_1, post_title="Post of user1", post_text="new post!!!", is_published=True)

    post_extend_with_tags_list(post_id=post_1, tags_list=[tag_0, tag_1])
    post_extend_with_tags_list(post_id=post_2, tags_list=[tag_3, ])
    post_extend_with_tags_list(post_id=post_3, tags_list=[tag_0, tag_2])
    post_extend_with_tags_list(post_id=post_4, tags_list=[tag_4, tag_5, tag_6, tag_7])
    post_extend_with_tags_list(post_id=post_5, tags_list=[tag_4, tag_5, tag_6, tag_7])
    post_extend_with_tags_list(post_id=post_6, tags_list=[tag_4, tag_5, tag_6, tag_7])
    post_extend_with_tags_list(post_id=post_7, tags_list=[tag_9, ])

    print("Добавление данных завершено.")
