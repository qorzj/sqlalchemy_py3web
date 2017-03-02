import web
from web import config, ctx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["obase", "init", "processor"]


obase = declarative_base()


def init():
    dbconf = config.mysql
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
        dbconf.username,
        dbconf.password,
        dbconf.host,
        dbconf.port,
        dbconf.database,
    ), pool_recycle=3600)
    config.db_session_maker = sessionmaker(bind=engine)
    web.add_json_encoder(_encode_row_obj)


def processor(labor):
    ret = {'code': 500}
    try:
        ctx.db = config.db_session_maker()
        ret = labor()
    except Exception as e:
        logging.exception(e)
    finally:
        ctx.db.close()
    return ret


def _encode_row_obj(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        field_dct = obj.__dict__.copy()
        field_dct.pop('_sa_instance_state', None)
        return field_dct


def _encode_row_proxy(obj):
    pass

