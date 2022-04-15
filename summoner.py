from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Summoner(Base):
    __tablename__ = 'summoners'
    id = Column(Integer, primary_key=True)
    sid = Column(Integer)  # 这里本来应该是sid作为主键。但是在demo中，不知何种问题会导致主键冲突，按说一个玩家对应一个sid应该是不会冲突的。
    name = Column(String(64), nullable=False, index=True)
    tier = Column(String(64), nullable=False)
    lp = Column(Integer)
    win = Column(Integer)
    lose = Column(Integer)
    ratio = Column(Float)

    def __init__(self, sid):
        self.sid = sid

    def info(self):
        res = '{name}\n({id_:<9}) {tier:<10} {lp} lp'.format(id_=self.sid, name=self.name, tier=self.tier, lp=self.lp)
        res += '\n'
        res += 'WIN/LOSE : {win:<4}/{lose:<4} {ratio}'.format(win=self.win, lose=self.lose,
                                                              ratio=self.win / (self.win + self.lose))
        return res

    def json(self) -> dict:
        return {
            'sid': self.sid,
            'name': self.name,
            'tier': self.tier,
            'lp': self.lp,
            'win': self.win,
            'lose': self.lose,
            'ratio': round(self.win / self.lose, 2)
        }


def init_summoners():
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/op", encoding='utf8', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_summoners()
