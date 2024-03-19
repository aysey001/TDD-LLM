class tagHandler:

    text = ""

    def __init__(self, text):
        self.text = text
    
    #use these for custom tags
    def has_open_tag(self, tag):
        words = self.text.split()
        if len(words) > 0:
            return words[0] == tag
        else:
            return False

    def has_close_tag(self, tag):
        words = self.text.split()
        if len(words) > 0:
            return words[-1] == tag
        else:
            return False
    
    #will remove the tags, but leave the newline
    def remove_tags(self, open_tag,close_tag):
        if self.has_open_tag(open_tag) and self.has_close_tag(close_tag):
            return self.text.replace(open_tag, "").replace(close_tag, "")
        else:
            raise ValueError("Missing open or close tag")
    
    
    #use these for default tags
    python_open_tag, python_close_tag = "[PYTHON]", "[/PYTHON]" 
    tests_open_tag, tests_close_tag = "[TESTS]", "[/TESTS]"
    list_open_tag, list_close_tag = "[LIST]", "[/LIST]"
    
    def has_python_tags(self):
        return self.has_open_tag(self.python_open_tag) and self.has_close_tag(self.python_close_tag)
    
    def has_list_tags(self):
        return self.has_open_tag(self.list_open_tag) and self.has_close_tag(self.list_close_tag)
    
    def has_tests_tags(self):
        return self.has_open_tag(self.tests_open_tag) and self.has_close_tag(self.tests_close_tag)
    
    def remove_python_tags(self):
        if self.has_python_tags():
            return self.remove_tags(self.python_open_tag, self.python_close_tag)
        else:
            raise ValueError("Missing open or close python tag")
    
    def remove_list_tags(self):
        if self.has_list_tags():
            return self.remove_tags(self.list_open_tag, self.list_close_tag)
        else:
            raise ValueError("Missing open or close list tag")
    
    def remove_tests_tags(self):
        if self.has_tests_tags():
            return self.remove_tags(self.tests_open_tag, self.tests_close_tag)
        else:
            raise ValueError("Missing open or close tests tag")
    #--------------------------------------------------------------------------------
    