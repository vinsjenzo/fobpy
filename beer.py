class beer(object):
     def __init__(self, name, style, abv, info):
         self.name = name
         self.style = style
         self.abv = abv
         self.info = info

     def __lt__(self, other):
         return self.abv < other.abv