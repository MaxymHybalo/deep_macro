class Process():

    def __init__(self, process) -> None:
        self.process = process
        print(self.process)
        self.map_props()

    def destroy(self):
        self.process = None
        self.name = None

    def map_props(self):
        proceses, cfg = self.process
        print('1p1',proceses)
        if type(proceses) == 'tuple' and len(proceses) == 2:
            sub1, sub2 = proceses
            self.sub1, self.sub2 = sub1, sub2
        else:
            task = proceses
            self.thread = task
            self.name = task.name
            self.pid = task.pid
            self.type = cfg['type']
    
    def stop(self):
        self.thread.terminate()
        return True

    def jsonify(self):
        return {
            'name': self.name,
            'pid': self.pid,
            'type': self.type
        }