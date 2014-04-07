import sublime, sublime_plugin
import re


class Insert_py_docCommand(sublime_plugin.TextCommand):

    def read_line(self, view, point):
        if (point >= view.size()):
            return
        next_line = view.line(point)
        return view.substr(next_line)

    def write(self, view, string):
        view.run_command("insert_snippet", {"contents": string})

    ##
    def run(self, edit, mode=None):

        point = self.view.sel()[0].begin()
        max_lines = 25  # maximum amount of lines to parse functions with
        current_line = self.read_line(self.view, point)
        print ("current_line:"+str(current_line))
        if not current_line or current_line.find("##") == -1:
            self.write(self.view, "\n# ${0}\n#")
            return

        point += len(current_line) + 1  # move to parse the next line
        next_line = self.read_line(self.view, point)
        print ("next_line:"+str(next_line))
        if not next_line:
            self.write(self.view, "\n# ${0}\n#")
            return
        ##
        #if the next line is already a comment, no need to reparse
        if re.search(r"^\s#*", next_line):
            self.write(self.view, "\n# ")
            return
