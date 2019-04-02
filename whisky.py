class Whisky:

    def __init__(self, name, distillery, region, age=None, abv=None, notes=None):
        if not len(name) < 256:
            raise ValueError("Length of name exceeds 255 chars")
        if not len(distillery) < 256:
            raise ValueError("Length of distillery exceeds 255 chars")
        if not len(region) < 256:
            raise ValueError("Length of region exceeds 255 chars")
        if not len(notes) < 256:
            raise ValueError("Length of notes exceeds 255 chars")

        self._name = name
        self._distillery = distillery
        self._region = region
        self._age = age
        self._abv = abv
        self._notes = notes

    def name(self):
        """Returns name of bottle"""
        return self._name
    def region(self):
        """Returns the region of the bottle"""
        return self._region
    def distillery(self):
        """Returns the distillery of the bottle"""
        return self._distillery
    def age(self):
        """Returns the age statement of the bottle"""
        return self._age
    def abv(self):
        """Returns the ABV of the bottle"""
        return self._abv
    def notes(self):
        """Returns the tasting notes of the bottle"""
        return self._notes
