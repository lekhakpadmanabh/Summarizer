

class Formatter:

   def __init__(self, key_points,fmt):

        if not hasattr(self, fmt):
            raise ValueError("invalid option: use 'md', 'json' or None")

        self._fmt = fmt
        self._kp = key_points
        self._options = {'md'  : self.md,
                         'json': self.json}

   def frmt(self):
         return self._options[self._fmt]()

   def md(self):
        fs = u""
        for i in xrange(len(self._kp)):
            fs += ">* {{{}}}\n".format(i)
        return fs.format(*[k[2] for k in self._kp])

   def json(self):
      raise NotImplementedError
