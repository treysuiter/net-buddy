#Views imports

from .home import home
from .router.router_config_list import router_config_list
from .router.router_config_list_search import router_config_list_search
from .router.router_config_form import router_config_form, router_config_edit_form
from .router.router_config_details import router_config_details
from .router.router_current_info import router_current_info
from .router.router_commands import router_commands

from .auth.logout import logout_user
from .auth.register import register