# removes html entities from the string
def drop_entities(input):
  return input.replace(u'\xa0', '')