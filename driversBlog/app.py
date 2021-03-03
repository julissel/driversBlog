from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Table, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

db_engine = create_engine("sqlite:///driversBlog.db", echo=False)
# echo=True create log with using module logging

Base = declarative_base(bind=db_engine)

# таблица ассоциаций для tags с posts (сообщаем классу модели Post и модели Tag с пом. secondary в relationship)
tags_for_posts_table = Table(
    "tags_for_posts",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)
)


class WritersLevel(Base):
    __tablename__ = "writerlevels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(35), nullable=False, unique=True)

    user = relationship("User", back_populates="level")

    def __str__(self):
        return str(self.level_name)

    def __repr__(self):
        return str(self)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(20), nullable=False)
    fullname = Column(String(50), nullable=False)
    level_id = Column(Integer, ForeignKey(WritersLevel.id), nullable=False, default=0, server_default="0")
    date_registration = Column(DateTime, nullable=False, default=func.now())
    # datetime.utcnow or func.now()
    active = Column(Boolean, nullable=False, default=True, server_default="1")

    posts = relationship("Post", back_populates="user")
    level = relationship(WritersLevel, back_populates="user")

    def __str__(self):
        return str(self.nickname)

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_title = Column(String(80), nullable=False)
    post_text = Column(Text, nullable=False)
    date_creation = Column(DateTime, nullable=False, default=func.now())
    is_published = Column(Boolean, nullable=False, default=False, server_default="0")

    user = relationship(User, back_populates="posts")
    tags = relationship("Tag", secondary=tags_for_posts_table, back_populates="posts")

    def __str__(self):
        return str(self.post_title)

    def __repr__(self):
        return str(self)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(20), nullable=False, unique=True)

    posts = relationship("Post", secondary=tags_for_posts_table, back_populates="tags")

    def __str__(self):
        return str(self.tag_name)

    def __repr__(self):
        return str(self)


def update_writers_levels_for_all_users(admin_level):
    con = db_engine.connect()

    # Обновление на уровень "Бывалый" всех у кого от 2-х до 4-х постов включительно, если пользователь не "Админ"
    new_level = 1
    number_of_posts_1 = 2
    number_of_posts_2 = 4
    con.execute("UPDATE users SET level_id = :new_level WHERE id in "
                "(select p.user_id from posts p join users u on p.user_id = u.id "
                "where u.level_id != :admin_level group by p.user_id "
                "having count(p.id) between :number_of_posts_1 and :number_of_posts_2)",
                {'new_level': new_level, 'admin_level': admin_level,
                 'number_of_posts_1': number_of_posts_1, 'number_of_posts_2': number_of_posts_2}
                )
    # Обновление на уровень "Эксперт" всех у кого более 4-х постов, если пользователь не "Админ"
    next_new_level = 2
    con.execute("UPDATE users SET level_id = :new_level WHERE id in "
                "(select p.user_id from posts p join users u on p.user_id = u.id "
                "where u.level_id != :admin_level group by p.user_id having count(p.id) > :number_of_posts)",
                {'new_level': next_new_level, 'admin_level': admin_level,
                 'number_of_posts': number_of_posts_2}
                )
    print("Обновлены уровни писателей у пользователей")


def create_data():
    session = Session()

    user1 = User(nickname="alex981", fullname="Алексей Алексеев")
    session.add(user1)
    session.flush()
    print("Новый пользователь:", user1)

    user2 = User(nickname="tim0n", fullname="Тимофей Тимофеев")
    session.add(user2)
    session.flush()
    print("Новый пользователь:", user2)

    user3 = User(nickname="sveta178", fullname="Светлана Светланова")
    session.add(user3)
    session.flush()
    print("Новый пользователь:", user3)

    post1 = Post(user_id=user1.id, post_title="Стали известны даты заездов в Кубке РАФ.",
                 post_text="Более подробная информация по ссылке: http://www.raf.su/drifting/tekushchij-sezon",
                 is_published=True)
    post2 = Post(user_id=user2.id, post_title="Электрический купе-кроссовер Audi e-tron Sportbac в России.",
                 post_text="Новый Sportback оснащен двумя электродвигателями, которые в обычном режиме работы "
                      "выдают 360 л.с. и 561 Нм крутящего момента."
                      "Двигатели питаются от комплекта аккумуляторов на 95 кВт-ч, которые при помощи специальной "
                      "быстрой системы на 150 кВт можно подзарядить на 80% за полчаса.",
                 is_published=False)
    post3 = Post(user_id=user3.id, post_title="Следим за результатами на этапе 'Яккима' Сортавала, респ. Карелия!",
                 post_text="Более подробная информация по ссылке: http://www.raf.su/rally/tekushchij-sezon",
                 is_published=True)
    post4 = Post(user_id=user1.id, post_title="Самые продаваемые автомобили России. Итоги 2020 года.",
                 post_text="ТОП 10 производителей за 2020г: Лада (343512 шт.), Kia  (201727 шт.), Hyundai (163441 шт.),"
                      "Renault (128408 шт.), Volkswagen (105785 шт.), Skoda (94632 шт.), Toyota (91598 шт.),"
                      "Nissan (56352 шт.), ГАЗ (51169 шт.), BMW (42721 шт.)",
                 is_published=True)
    post5 = Post(user_id=user1.id, post_title="Самые продаваемые автомобили России. Итоги 2019 года.",
                 post_text="Лада (362356 шт.), Kia (225901 шт.), Hyundai (179124 шт.), Renault (144989 шт.),	"
                      "Volkswagen (111989 шт.), Toyota (103597 шт.), Skoda (88609 шт.), Nissan (64974 шт.),"
                      "ГАЗ (63910 шт.), Mercedes-Benz (43627 шт.)",
                 is_published=True)
    post6 = Post(user_id=user2.id, post_title="Новые налоги для автопроизводства в России.",
                 post_text="Новые налоги",
                 is_published=True)
    post7 = Post(user_id=user1.id, post_title="Post of user1",
                 post_text="new post!!!",
                 is_published=True)
    session.add_all([post1, post2, post3, post4, post5, post6, post7])
    session.flush()
    print("Посты добавлены")

    tags_list = [Tag(tag_name="спорт"), Tag(tag_name="дрифт"), Tag(tag_name="ралли"), Tag(tag_name="электрокары"),
                 Tag(tag_name="статистика"), Tag(tag_name="авторынок РФ"), Tag(tag_name="производители авто"),
                 Tag(tag_name="ТОП 10"), Tag(tag_name="семейный автомобиль"), Tag(tag_name="новинки"),
                 Tag(tag_name="каршеринг")]
    session.add_all(tags_list)
    session.flush()
    print("Тэги добавлены")

    post1.tags.extend((tags_list[0], tags_list[1]))
    post2.tags.append(tags_list[3])
    post3.tags.extend((tags_list[0], tags_list[2]))
    post4.tags.extend((tags_list[4], tags_list[5], tags_list[6], tags_list[7]))
    post5.tags.extend((tags_list[4], tags_list[5], tags_list[6], tags_list[7]))
    post6.tags.extend((tags_list[4], tags_list[5], tags_list[6], tags_list[7]))
    post7.tags.append(tags_list[9])
    print("Добавлены связи тэгов и постов")

    writers_levels_list = [WritersLevel(level_name="Новичок"), WritersLevel(level_name="Бывалый"),
                           WritersLevel(level_name="Эксперт"), WritersLevel(level_name="Админ")]
    session.add_all(writers_levels_list)
    session.flush()
    print("Уровни писателя добавлены")

    session.commit()
    print("Добавление данных завершено.")
    session.close()


def select_all_users():
    session = Session()
    user_list = session.query(User).all()
    print("Список пользователей:")
    for user in user_list:
        print("ФИО: ", user.fullname, ", nickname:", user.nickname, "уровень писателя:", user.level_id)
    session.close()


def find_tag(tag_name_for_find):
    session = Session()
    query_result = session.query(Tag).filter_by(tag_name=tag_name_for_find).first()
    session.close()
    if not query_result:
        print(f"Тэг '{tag_name_for_find}' отсутствует в таблице тэгов!")
    else:
        print(f"Тэг '{tag_name_for_find}' существует в таблице тэгов!")


def all_user_posts_with_2tags(user_nickname, tag1, tag2):
    session = Session()
    user_id = session.query(User.id).filter_by(nickname=user_nickname).first()
    posts_items = session.query(Post.post_title, Post.post_text).join(Post.tags).join(Post.user).\
        filter(or_(Tag.tag_name == tag1, Tag.tag_name == tag2)).\
        filter(User.id == user_id[0]).distinct()

    print(f"Посты пользователя '{user_nickname}' с тэгами '{tag1}' и '{tag2}': ")
    for post_title, post_text in posts_items:
        print(f"Пост '{post_title}':")
        print(post_text)

    session.close()


if __name__ == "__main__":
    try:
        # create_all()/drop_all() создание/удаление всех таблиц в бд
        Base.metadata.create_all()
        # заполнение данными
        create_data()
        # обновление уровня писателя в зависимости от количства постов пользователя
        update_writers_levels_for_all_users(admin_level=3)
        # выбор списка всех пользователей
        select_all_users()
        # поиск тэга в таблице тэгов по названию
        find_tag("каршеринг")
        find_tag("трейд-ин")
        # поиск всех постов заданного пользователя, имеющих два заданных тэга
        all_user_posts_with_2tags("alex981", tag1='статистика', tag2='производители авто')
    except Exception as e:
        print("Возникла ошибка:", e)