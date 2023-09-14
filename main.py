from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
class Player(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    
    team_id: Optional[int] = Field(default=None, foreign_key='team.id')


url = "mysql://root@127.0.0.1:3306/teamplayerjoin"
engine = create_engine(url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_players():
    with Session(engine) as session:
        team_ind = Team(name='India')
        team_pak = Team(name='Pakistan')
        session.add(team_ind)
        session.add(team_pak)
        session.commit()
        
        player_sachin = Player(name='Sachin',age=40, team_id= team_ind.id)
        player_afridi = Player(name='Afirid', age=40, team_id= team_pak.id)
        
        session.add(player_sachin)
        session.add(player_afridi)
        session.commit()
        
        session.refresh(player_sachin)
        session.refresh(player_afridi)
        
        print("Created hero:", player_sachin)
        print("Created hero:", player_afridi)
        
        
def select_players():
    with Session(engine) as session:
        db_player = select(Player, Team).where(Player.team_id == Team.id)
        # db_player = select(Player, Team).join(Team)
        # db_player = select(Player, Team).join(Team, isouter=True)
        # db_player = select(Player).join(Team).where(Team.name == 'India')
        # db_player = select(Player, Team).join(Team).where(Team.name == 'India')
        res = session.exec(db_player)
        for player, team in res:
            print ("Player: ", player, "Team: ",team)
        # for player in res:
        #     print ("Player: ", player)

def main():
    create_db_and_tables()
    create_players()
    select_players()


if __name__ == "__main__":
    main()