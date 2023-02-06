from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///data/football.db')
Base = declarative_base()

player_match = Table('player_match', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id')),
    Column('goals_scored', Integer),
    Column('shots_saved', Integer),
    Column('yellow_cards_count', Integer),
    Column('red_cards_count', Integer))

team_match = Table('team_match', Base.metadata,
    Column('team_id', Integer, ForeignKey('team.id')),
    Column('match_id', Integer, ForeignKey('match.id')))

class League(Base):
    __tablename__ = 'league'
    id = Column(Integer, primary_key=True)
    place = Column(Integer)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship('Team', back_populates='league')
    games_played = Column(Integer)
    goals_difference = Column(Integer)
    points = Column(Integer)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    won = Column(Integer)
    draw = Column(Integer)
    lost = Column(Integer)
    goals_scored = Column(Integer)
    goals_missed = Column(Integer)
    league = relationship('League', back_populates='team')
    player = relationship('Player', back_populates='team')
    match_info = relationship('Match', secondary=team_match, back_populates='team_info')

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    f_name = Column(String)
    l_name = Column(String)
    nationality = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship('Team', back_populates='player')
    number = Column(Integer)
    position_id = Column(Integer, ForeignKey('position.id'))
    position = relationship('Position', back_populates='player')
    goals_saves = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    match_info = relationship('Match', secondary=player_match, back_populates='player_info')

class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    position_name = Column(String)
    abbrev = Column(String)
    player = relationship('Player', back_populates='position')

class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    team_1_id = Column(Integer, ForeignKey('team.id'))
    team_1 = relationship('Team', back_populates='match_team_1')
    goals_team_1 = Column(Integer)
    team_2_id = Column(Integer, ForeignKey('team.id'))
    team_2 = relationship('Team', back_populates='match_team_2')
    goals_team_2 = Column(Integer)
    player_info = relationship('Player', secondary=player_match, back_populates='match_info')
    team_info = relationship('Team', secondary=team_match, back_populates='match_info')
    

if __name__ == '__main__':
    Base.metadata.create_all(engine)