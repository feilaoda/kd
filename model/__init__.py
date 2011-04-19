import sqlalchemy as sa
from sqlalchemy import orm
from kd.model import meta
from kd.model.member import Member, Role, Permission
from kd.model.software import Software

def init_model(engine):
    #Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)

    # We are using SQLAlchemy 0.5 so transactional=True is replaced by
    # autocommit=False
    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine    
    meta.Session = orm.scoped_session(sm)
    
   
