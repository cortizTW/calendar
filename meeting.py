class Meeting:

    def __init__(self, start, end, summary, location):
        self.start = start['dateTime']
        self.end = end['dateTime']
        self.summary = summary
        self.location = location

    def __str__(self):
        return 'Inicio: ' + self.start + '\n' + 'Fin: ' + self.end + '\n' + 'Resumen: ' + self.summary + '\n' + 'Ubicación: ' + self.location
