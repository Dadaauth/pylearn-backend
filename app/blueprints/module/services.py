from app.models.module import Module
from app.utils.helpers import extract_request_data
from app.utils.error_extensions import BadRequest, NotFound

def iupdate_module(module_id):
    data = extract_request_data("json")
    to_update =  {
        "title": data.get("title"),
        "description": data.get("description"),
        "status": data.get("status")
    }
    module = Module.search(id=module_id)
    if not module:
        raise NotFound(f"Module with ID {module_id} not found")
    module.update(**to_update)
    module.save()

def ifetch_modules():
    mds = Module.all()
    if not mds:
        raise NotFound("No Module Found")
    return [mod.to_dict() for mod in mds]

def icreate_module():
    data = extract_request_data("json")
    if not data.get("title"):
        raise BadRequest("Required field(s) not present: title")

    Module(**data).save()
