import web
from web import config, ctx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["obase", "init", "processor"]


obase = declarative_base()


def init():
    dbconf = config.database
    engine = create_engine('{}://{}:{}@{}:{}/{}'.format(
        dbconf.protocol,  # mysql+mysqlconnector
        dbconf.username,
        dbconf.password,
        dbconf.host,
        dbconf.port,
        dbconf.database,
    ), pool_recycle=3600)
    engine.echo = dbconf.get('echo', False)
    web.g.db_session_maker = sessionmaker(bind=engine)
    if dbconf.get('create_db', False): obase.metadata.create_all(engine)
    web.add_json_encoder(_encode_row_obj)


def processor(f):
    try:
        ctx.db = web.g.db_session_maker()
        ret = f()
    except Exception as e:
        ctx.db.rollback()
        raise e
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


class helper:
    """
    from sqlalchemy_plugin import plugin
    plugin.init()
    app.add_processor(plugin.processor)
    """
    def config(self):
        """
        database:
            protocol: 'mysql+mysqlconnector'
            username: 'root'
            password: 'the_password'
            host: 'localhost'
            port: 3306
            database: 'database_name'

        """
        pass
