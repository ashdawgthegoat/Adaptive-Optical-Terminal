class Animus(QObject):

    app_launched = pyqtSignal(str)
    app_closed = pyqtSignal(str)

    workbench_created = pyqtSignal()
    workbench_closed = pyqtSignal()
    workbench_switched = pyqtSignal(str)

    module_connected = pyqtSignal(str)
    module_disconnected = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.applications = {}

        self.running_apps = {}

        self.modules = {}

        self.workbenches = {}

        self.active_workbench = None

    def register_application(self, app):

        if app["id"] in self.applications:
            return 

        self.applications[app["id"]] = app

    def discover_applications(self):
        pass

    def launch(self, app):

        if app not in self.applications:
            return

        if app in self.running_apps:
            return

        self.running_apps[app] = self.applications[app]

        self.app_launched.emit(app)

    def close(self, app):

        if app not in self.running_apps:
            return

        del self.running_apps[app]

        self.app_closed.emit(app)    

    def is_running(self, app):
        
        return app in self.running_apps

    def create_workbench(self):
        
        workbench_id = f"workbench_{len(self.workbenches) + 1}"

        self.workbenches[workbench_id] = {
            "applications": []
        }

        self.active_workbench = workbench_id

        self.workbench_created.emit()

    def close_workbench(self):
        
        if self.active_workbench is None:
            return

        del self.workbenches[self.active_workbench]

        self.active_workbench = None

        self.workbench_closed.emit()

    def register_module(self, module):
        
        if module["id"] in self.modules:
            return

        self.modules[module["id"]] = module

        self.module_connected.emit(module["id"])

    def unregister_module(self, module):
        
        if module["id"] not in self.modules:
            return

        del self.modules[module["id"]]

        self.module_disconnected.emit(module["id"])

    def list_applications(self):

        return list(self.applications.values())

    def list_modules(self):
        
        return list(self.modules.values())

    def switch_workbench(self, workbench):
        
        if workbench not in self.workbenches:
            return

        self.active_workbench = workbench

        self.workbench_switched.emit(workbench)

    def list_workbenches(self):
        
        return list(self.workbenches.keys())