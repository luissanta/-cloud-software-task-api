class GetTaskResponse:
    def __init__(**kwargs):
        self.id = kwargs['id']
        self.fileName = kwargs['fileName']
        self.originalExtension = kwargs['originalExtension']
        self.newExtension = kwargs['newExtension']
        self.status = kwargs['status']