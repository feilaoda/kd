"""Software App model"""

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, UnicodeText, Integer, Date,Numeric, CHAR,Text,DateTime
from sqlalchemy import orm
from kd.model.meta import Session as session 
from kd.model.meta import metadata
from kd.model.member import Member



software_table = Table('software', metadata,
    Column('id', Integer(), primary_key=True),
    Column('guid', Unicode(128)),
    Column('name', Unicode(255)),
    Column('ename', Unicode(255)),
    Column('member_id', Integer(), default=0),
    Column('author', Unicode(255)),
    Column('description', Text),
    Column('version', Unicode(32)),    
    Column('price', Numeric, default=0),
    Column('size', Numeric, default=0),
    Column('rating', Numeric, default=0),
    Column('kind', Integer(), default=0), #Game 0, Application 1, 
    Column('category',  Unicode(32)),
    Column('type', Integer(), default=0), #unkonwn 0, android 1, iphone 2, ipad 3, winphone 4
    Column('logo_url', Unicode(255)),
    Column('seller_id', Integer, default=0),
    Column('seller_name', Unicode(100)),    
    Column('download_count',Integer()),
    Column('download_url', Unicode(255)),
    Column('review_count', Integer(), default=0),
    Column('likeit_count', Integer(), default=0),
    Column('follower_count', Integer(), default=0),
    Column('tags', Text), 
    Column('screenshot', Text),    
    Column('create_time', DateTime),
    Column('publish_time', DateTime),
    Column('update_time', DateTime)
)


# This is the association table for the many-to-many relationship between
# groups and members
software_follower_table = Table('software_follower', metadata,
    Column('id', Integer(), primary_key=True),
    Column('software_id', Integer(), ForeignKey('software.id')),
    Column('member_id', Integer(), ForeignKey('member.id'))    
)

software_likeit_table = Table('software_likeit', metadata,
    Column('id', Integer(), primary_key=True),
    Column('software_id', Integer(), ForeignKey('software.id')),
    Column('member_id', Integer(), default=0),
    Column('ip', Unicode(100)), #max 255 char 
)

software_version_table = Table('software_version', metadata,
    Column('id', Integer(), primary_key=True),
    Column('software_id', Integer(), ForeignKey('software.id')),
    Column('download_url', Unicode(255)),
    Column('version', Unicode(32)),
    Column('action', Unicode(100)),#new,update
    Column('release_date', DateTime),
)

software_seller_table = Table('software_seller', metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', Unicode(255)),      
    Column('url', Unicode(255))
)

software_review_table = Table('software_review', metadata,
    Column('id', Integer(), primary_key=True),
    Column('software_id', Integer(), ForeignKey('software.id')),  
    Column('version', Unicode(32)),
    Column('member_id', Integer(), default=0), #default 0 is 
    Column('review', Unicode(255)), #max 255 char
    Column('rating', Integer(), default=0), #default 0 , 1-5
    Column('downs', Integer(), default=0),
    Column('ups', Integer(), default=0),
)




software_review_digger_table = Table('software_review_digger', metadata,
    Column('id', Integer(), primary_key=True),
    Column('review_id', Integer(), ForeignKey('software_review.id')),      
    Column('member_id', Integer(), default=0), #default 0
    Column('ip', Unicode(100)), #max 255 char
)

class SoftwareVersion(object):
    pass

class SoftwareFollower(object):
    pass

class SoftwareReview(object):
    pass

class SoftwareReviewDigger(object):
    pass

class SoftwareSeller(object):
    pass       
    
orm.mapper(SoftwareVersion, software_version_table)
orm.mapper(SoftwareFollower, software_follower_table)
orm.mapper(SoftwareReviewDigger, software_review_digger_table
#, properties={        
#    'member': orm.relation(Member),
#}
)

orm.mapper(SoftwareReview, software_review_table, properties={        
    'diggers': orm.relation(SoftwareReviewDigger),
#    'member': orm.relation(Member),
})




class Software(object):
    def __init__(self, name=''):
        self.name = name
        
    def get_android_apps(self):
        return session.query(Software).filter(Software.type == '1')
        
    def get_followers(self, limit=20):
        fs = session.query(SoftwareFollower).filter(SoftwareFollower.software_id == self.id)
        return fs

    def get_versions(self):
        vs = session.query(SoftwareVersion).filter(SoftwareVersion.software_id == self.id)
        return vs
     
    def get_reviews(self):
        rs = session.query(SoftwareReview).filter(SoftwareReview.software_id == self.id)
        return rs        
        

 
        

orm.mapper(SoftwareSeller, software_seller_table
# , properties={        
# 'softwares': orm.relation(Software),
#}
)

orm.mapper(Software, software_table, properties={    
    'followers': orm.relation(Member, secondary=software_follower_table),
    'versions': orm.relation(SoftwareVersion),
    'reviews': orm.relation(SoftwareReview),
})





