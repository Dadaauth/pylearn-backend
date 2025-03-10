from app.models.module import Module
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound

def iupdate_module(module_id):
    data = extract_request_data("json")
    module = Module.search(id=module_id)
    if not module:
        raise NotFound(f"Module with ID {module_id} not found")

    if data.get("id"):
        del data['id']

    module.update(**data)
    module.save()

def ifetch_modules(course_id):
    mds = Module.search(course_id=course_id)
    if not mds:
        raise NotFound("No Module Found")

    if isinstance(mds, Module): return [mds.to_dict()]
    return [mod.to_dict() for mod in mds]

def icreate_module():
    data = extract_request_data("json")
    if not data.get("title"):
        raise BadRequest("Required field(s) not present: title")

    Module(**data).save()
