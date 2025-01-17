from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.mysql import ENUM

from app.models.base import Base
from app.models.basemodel import BaseModel
from app.utils.helpers import has_required_keys
from app.utils.error_extensions import NotFound


class Module(BaseModel, Base):
    __tablename__ = "modules"

    title = mapped_column(String(60), nullable=False)
    description = mapped_column(String(300))
    status = mapped_column(ENUM("deleted", "draft", "published"), default="draft", nullable=False)
    
    next_module_id = mapped_column(ForeignKey("modules.id"), nullable=True)
    prev_module_id = mapped_column(ForeignKey("modules.id"), nullable=True)

    projects = relationship("Project", back_populates="module")

    next_module = relationship("Module", remote_side="Module.id", foreign_keys=[next_module_id])
    prev_module = relationship("Module", remote_side="Module.id", foreign_keys=[prev_module_id])

    def __init__(self, **kwargs):
        """
        """
        super().__init__()
        [setattr(self, key, value) for key, value in kwargs.items()]

        required_keys = {"title", "status"}
        accurate, missing = has_required_keys(kwargs, required_keys)
        if not accurate:
            raise ValueError(f"Missing required key(s): {', '.join(missing)}")
        
        # insert Module at the correct node
        if Module.count() == 0:
            # insert as head of the list
            self.prev_module_id = None
            self.next_module_id = None
            return
        
        self.save()
        self.refresh()

        prev_module_id = kwargs.get("prev_module_id")
        if not prev_module_id:
            # Make first module in list
            head_module = Module.search(prev_module_id=None)
            head_module.prev_module_id = self.id
            head_module.save()

            self.next_module_id = head_module.id
        else:
            prev_module = Module.search(id=prev_module_id)
            if prev_module is None:
                raise NotFound("Previous Module Not Found")
            next_m_id = prev_module.next_module_id
            prev_module.next_module_id = self.id
            prev_module.save()
            self.next_module_id = next_m_id

            # Check if the next module exists
            next_module = Module.search(id=next_m_id)
            if next_module:
                next_module.prev_module_id = self.id
                next_module.save()

    @classmethod
    def all(cls):
        """
        You need to intercept here because you need
            to sort the modules before you send them
            to the client calling the models API
        """
        modules = super().all()
        return cls.sort_modules(modules)

    @classmethod
    def search(cls, **filters: dict) -> list:
        """
        You need to intercept here because you need
            to sort the modules before you send them
            to the client calling the models API
        """
        modules = super().search(**filters)
        return cls.sort_modules(modules)
    
    def update(self, **kwargs: dict) -> None:
        """
            You need to intercept here to account for
            updates involving the arrangement of nodes
            in the linked list

            Update a set of attributes in an object.
            :params
                @kwargs: a dictionary of attributes
                        to update
        """
        if kwargs.get("prev_module_id") is not None:
            """
                Code for if the client is trying
                to update the order of the modules
                in the linked list.
            """
            prev_module_id = kwargs.get("prev_module_id")
            new_prev_module = Module.search(id=prev_module_id)
            if not new_prev_module:
                raise NotFound("Previous Module not found")
            
            new_prev_module.prev_module_id = self.prev_module_id
            self.next_module_id = new_prev_module.next_module_id

            if new_prev_module.next_module_id:
                new_prev_module.next_module.prev_module_id = self.id
            self.prev_module_id = new_prev_module.id
            new_prev_module.next_module_id = self.id

        super().update(**kwargs)

    def sort_modules(modules):
        if modules is None or modules == []: return modules
        if not isinstance(modules, list): return modules

        # Retrieve the head of the list
        head = None
        for module in modules:
            if module.prev_module_id is None:
                head = module
                break
        
        # sorting process
        tmp = head
        tmp_list = [head]
        while tmp is not None and tmp.next_module_id is not None:
            for module in modules:
                if module.id == tmp.next_module_id:
                    tmp_list.append(module)
                    tmp = module
                    break

        modules = tmp_list
        return modules