# https://www.cnblogs.com/Amd794/p/18924717

class Resource:
    resource_id: str
    resource_type: str = 'page|api'
    resource_name: str = 'BlogAPI'
    router_path: str
    router_method = 'GET'

class ResourcePermit:
    resource_id: str
    permit_code = ['create_post', 'delete_post']

# role 的 permit分组
class PermitRole:
    resource_name: str = '*'
    resource_permit: str = '*'
    role_name: str = 'root|admin'  # 自定义分组

# user额外赋予permit
class PermitUser:
    permit: str = 'create_post'
    user_id: int