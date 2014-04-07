import sublime, sublime_plugin


class Insert_py_docCommand(sublime_plugin.TextCommand):

    def run(self, edit, mode=None):
        print ("Here we are in run function")
        #self.view.insert(edit, 0, "Hello, World!")
