#Views imports

from .home import home
from .router.router_config_list import router_config_list
from .router.router_config_form import router_config_form, router_config_edit_form
from .router.router_config_details import router_config_details
from .router.router_current_info import router_current_info

from .auth.logout import logout_user
from .auth.register import register