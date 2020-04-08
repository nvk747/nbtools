from .basewidget import BaseWidget
from ipykernel.comm import Comm


class ToolManager(object):
    COMM_NAME = 'nbtools_comm'  # The name of the kernel <-> client comm
    _instance = None            # ToolManager singleton

    @staticmethod
    def instance():
        if ToolManager._instance is None:
            ToolManager._instance = ToolManager()
        return ToolManager._instance

    def __init__(self):
        self.tools = {}  # Initialize the tools map
        # Establish the comm with the client
        self.comm = Comm(target_name=ToolManager.COMM_NAME, data={})

    def send(self, message_type, tool_or_payload):
        """
        Send a message to the comm on the client

        :param func:
        :param payload:
        :return:
        """
        # Handle known message types
        if message_type == 'register':     payload = tool_or_payload.json_safe()
        elif message_type == 'unregister': payload = tool_or_payload.id
        else:                              payload = tool_or_payload

        # Send the message to the client
        self.comm.send({
            "func": message_type,
            "payload": payload
        })

    @classmethod
    def list(cls):
        """
        Get the list of registered tools

        :return: list of tools
        """
        return [t for t in [o for o in cls.instance().tools.values()]]

    @classmethod
    def register(cls, tool_or_widget):
        """Register a NBTool or UIBuilder object"""
        if isinstance(tool_or_widget, NBTool) or isinstance(tool_or_widget, BaseWidget):
            tools = cls.instance().tools
            if tool_or_widget.origin and tool_or_widget.id:
                # Lazily create the origin
                if tool_or_widget.origin not in tools:
                    tools[tool_or_widget.origin] = {}

                # Register the tool
                cls.instance().tools[tool_or_widget.origin][tool_or_widget.id] = tool_or_widget

                # Notify the client of the registration
                cls.instance().send('register', tool_or_widget)
            else:
                raise ValueError("register() must be passed a tool with an instantiated origin and id")
        else:
            raise ValueError("register() must be passed an NBTool or UIBuilder object")

    @classmethod
    def unregister(cls, origin, id):
        """Unregister the tool with the associated id"""
        if cls.exists(id, origin):
            del cls.instance().tools['origin']['id']
        else:
            print(f'Cannot find tool to unregister: {origin} | {id}')

    @classmethod
    def tool(cls, id, origin='Notebook'):
        """
        Return reference to tool widget given the id and origin
        """
        if cls.exists(id, origin):
            return cls.instance().tools['origin']['id']
        else:
            print(f'Cannot find tool: {origin} | {id}')
            return None

    @classmethod
    def exists(cls, id, origin):
        """Check if a tool for the provided id and origin exists"""
        tools = cls.instance().tools
        if 'origin' in tools:
            if id in tools['origin']:
                return True
            else: return False
        else: return False


class NBTool:
    """
    Tool class, used to register new tools with the manager
    """
    origin = None
    id = None
    name = None
    description = None
    tags = None
    version = None
    load = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def json_safe(self):
        return {
            'origin': self.origin,
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tags': self.tags,
            'version': self.version
        }