from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///data/football.db')
Base = declarative_base()

player_goals_scored = Table('goals_scored', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id')),
    Column('goals_scored', Integer))

player_shots_saved = Table('shots_saved', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id')),
    Column('shots_saved', Integer))

player_yellow_cards = Table('yellow_cards', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id')),
    Column('yellow_cards_count', Integer))

player_red_cards = Table('red_cards', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('match_id', Integer, ForeignKey('match.id')),
    Column('red_cards_count', Integer))

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
    match_team_1 = relationship('Match', back_populates='team_1')
    match_team_2 = relationship('Match', back_populates='team_2')

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
    match_goals = relationship('Match', secondary=player_goals_scored, back_populates='goals_scored')
    match_saves = relationship('Match', secondary=player_shots_saved, back_populates='shots_saved')
    match_yellow_cards = relationship('Match', secondary=player_yellow_cards, back_populates='yellow_cards_count')
    match_red_cards = relationship('Match', secondary=player_red_cards, back_populates='red_cards_count')

class Position(Base):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    name = Column(String)
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
    goals_scored = relationship('Player', secondary=player_goals_scored, back_populates='match_goals')
    shots_saved = relationship('Player', secondary=player_shots_saved, back_populates='match_saves')
    player_yellow_cards = relationship('Player', secondary=player_yellow_cards, back_populates='match_yellow_cards')
    player_red_cards = relationship('Player', secondary=player_red_cards, back_populates='match_red_cards')
    

if __name__ == '__main__':
    Base.metadata.create_all(engine)