import sys

class Context:
  def __init__(self):
    self.stack = []
    self.line_number = 0
    self.pos = 0
  
  def getc(self):
    # print(str(self))
    # print("getc : {}".format(self.line[self.pos]))
    return self.line[self.pos]

  def __str__(self):
    return "line : {} pos : {}".format(self.line_number, self.pos)
  
  def next(self):
    self.pos += 1

  def is_endl(self):
    return len(self.line) <= self.pos
    
class ParserError(TypeError): pass

class Parser:
  def __init__(self):
    self.ctx = Context()
  
  def parse(self, line):
    self.ctx.line = line
    self.ctx.pos = 0
    while not self.endl():
      self.skip_whitespace()
      if self.endl():
        return

      self.parse_string_literal()
  
  def getc(self):
    return self.ctx.getc()

  def next(self):
    return self.ctx.next()

  def endl(self):
    return self.ctx.is_endl()

  def skip_whitespace(self):
    while self.getc() == ' ' or self.getc() == '\r' or self.getc() == '\n':
      self.next()
      if self.endl():
        break

  def parse_string_literal(self):
    start_line_number = self.ctx.line_number
    start_pos = self.ctx.pos

    if self.getc() != '"':
      return
      # self.abort("No String literal")

    self.next()
    if self.endl():
      self.abort("Matched double quoatation was not found")

    s = ""
    while self.getc() != '"':
      c = self.parse_char()
      if c is None:
        self.next()
        break
      s += c
      self.next()
      if self.endl():
        self.abort("Matched double quoatation was not found")

    if self.endl() or self.getc() != '"':
      self.abort("Matched double quoatation was not found")

    print("String : {}".format(s))
    self.next()

  def parse_char(self):
    c = self.parse_escape()
    if not c:
      c = self.getc()
    return c

  def parse_escape(self):
    c = self.getc()
    if c == '\\':
      self.next()
      if self.endl():
        self.abort("No character after '\\'")
      return self.getc()

  def abort(self, message):
    print("Error on : " + str(self.ctx))
    raise ParserError(message)

if __name__ == '__main__':
  input = sys.stdin
  if len(sys.argv) > 1:
    print("argv: {}".format(sys.argv))
    input = open(sys.argv[1])

  parser = Parser()
  line_number = 0
  for line in input:
    parser.ctx.line_number = line_number
    parser.parse(line)
