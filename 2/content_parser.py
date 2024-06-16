from html.parser import HTMLParser

class ContentParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.recorded_tag = False
    self.data = []
    self.links = []

  def handle_starttag(self, tag, attributes):
    if tag not in ['p', 'span', 'a', 'b', 'li', 'h2', 'h3', 'h4']:
      self.recorded_tag = False
    else:
      self.recorded_tag = True
    if tag not in ['div', 'a']:
      return
    if self.recording:
      if tag == 'a':
          link = attributes[0][1]
          if link.startswith('/wiki/'):
            self.links.append(f"https://en.wikipedia.org{link}")
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class' and value == 'mw-content-ltr mw-parser-output':
        break
    else:
      return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'div' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording and self.recorded_tag:
      self.data.append(data)

  def get_data(self):
    return ''.join(self.data)
  
  def get_links(self):
    return self.links