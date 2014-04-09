import sublime, sublime_plugin
import re


class Insert_py_docCommand(sublime_plugin.TextCommand):

    ## read_line
    # @brief : read a line at specific point
    # @param self : self object
    # @param view : current view
    # @param point : specific a point
    #
    # @return string of line
    #
    def read_line(self, view, point):
        if (point >= view.size()):
            return
        next_line = view.line(point)
        return view.substr(next_line)

    ## write
    # @brief : insert specific string to current view
    # @param self :
    # @param view : current view
    # @param string : the string to be inserted
    #
    # @return None
    #
    def write(self, view, string):
        view.run_command("insert_snippet", {"contents": string})

    ## run
    # @brief : Main function of command.
    # @param self :
    # @param edit : current edit
    # @param mode default None :
    #
    # @return None
    #
    def run(self, edit, mode=None):
        point = self.view.sel()[0].begin()
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

        # if the next line is already a comment, no need to reparse
        if re.match(r"^\s*#", next_line):
            print ("next line is already a comment, no need to reparse")
            self.write(self.view, "\n# ")
            return

        # if the next line starts with 'def', then parse it as function
        if re.match(r"^\s*def\s+\w+\s*\(", next_line):
            print ("next line starts with 'def', parse it as function")
            snippet = self.parse_function(next_line)
            self.write(self.view, snippet)
            return

    ## parse_function
    # @brief : parse the line as a function
    # @param self :
    # @param line : the line to be parsed
    #
    # @return the snippet to be inserted
    #
    def parse_function(self, line):
        function_name = ""
        params = []  # store params as tuple:(name, default_value).
        snippet = " "

        # parse funciton name
        start_index = line.find('def')
        end_index = line.find('(')
        if start_index != -1 and end_index != -1 and end_index > start_index:
            function_name = line[start_index+4: end_index].strip()
            snippet += function_name
        snippet += "\n# @brief : ${1:[brief description]}"

        #parse params
        start_index = line.find('(')
        end_index = line.rfind(')')
        param_str = line[start_index+1: end_index]

        if len(param_str.strip()) > 0:
            print ("param_str[%s]" % param_str)
            for param in param_str.split(','):
                if '=' in param:
                    param_name = param.split('=')[0].strip()
                    default_value = param.split('=')[1].strip()
                else:
                    param_name = param.strip()
                    default_value = None
                params.append((param_name, default_value))
            print ("param_list[%s]" % params)

            for i in range(0, len(params)):
                param = params[i]
                if not param[1]:
                    snippet += "\n# @param {0} : ${{{1}:[description]}}".format(param[0], i+2)
                else:
                    snippet += "\n# @param {0} default {1} : ${{{2}:[description]}}".format(param[0], param[1], i+2)
            snippet += "\n#"

        snippet += "\n# @return ${{{0}:[return description]}}\n#".format(len(params)+2)
        return snippet
