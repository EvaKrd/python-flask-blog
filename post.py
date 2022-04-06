class Post:
    def __init__(self, id, created, title, content):
        self.id = id
        self.created = created
        self.title = title
        self.content = content
    
    def getId(self):
        return self.id

    def getCreated(self):
        return self.created
    
    def setTitle(self, title):
        self.title = title
    
    def getTitle(self):
        return self.title
    
    def setContent(self, content):
        self.content = content
    
    def getContent(self):
        return self.content