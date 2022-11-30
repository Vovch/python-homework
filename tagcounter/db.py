from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine("sqlite:///sqlite.db", echo=False, future=True)


class Homework(Base):
    __tablename__ = "homework"

    siteName = Column(String)
    url = Column(String)
    date = Column(String, primary_key=True)
    tags = Column(String)

    def __repr__(self):
        return f"Homework(date={self.date}, siteName={self.siteName}, url={self.url}, tags={self.tags})"


Base.metadata.create_all(engine)


def add_info(site_name: str, url: str, date: str, tags: str):
    with Session(engine) as session:
        record = Homework(siteName=site_name, url=url, date=date, tags=tags)
        session.add_all([record])
        session.commit()


def view_info(site):
    with Session(engine) as session:
        print(session.query(Homework).where(Homework.siteName.contains(site)).order_by(Homework.date.desc()).first())
