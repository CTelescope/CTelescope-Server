from . query_data_base import init_routes_db
from . camera_control import init_routes_cmr
from . motors_config import init_routes_mtrs
from . telescope_control import init_routes_tls
from . query_gallery import init_routes_glr

def init_routes(app):
    init_routes_db(app)
    init_routes_cmr(app)
    init_routes_mtrs(app)
    init_routes_tls(app)
    init_routes_glr(app)