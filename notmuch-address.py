import sublime
import sublime_plugin
import subprocess

class NotmuchaddressCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        text = None

        proc = subprocess.Popen(['/usr/local/bin/notmuch', 'address', '--deduplicate=address', 'email.com'], stdout=subprocess.PIPE, universal_newlines=True)
        items = proc.stdout.readlines()
        print(items)

        def callback(i):
            if i == -1:
                    return
            item = items[i]
            #self.view.run_command("insert", {"characters": item})
            self.view.run_command("notmuchedit", {"text": item.rstrip('\n')})
            print(item)
            #self.view.insert(edit, self.view.sel()[0].begin(), item)

        self.view.window().show_quick_panel(items, callback)


class NotmucheditCommand(sublime_plugin.TextCommand):
    # https://stackoverflow.com/questions/20466014/save-the-edit-when-running-a-sublime-text-3-plugin
    # we need to run a second process to pass the result from the search to, else the 'edit' magic
    # has disappeared by the time we want to insert

    def run(self, edit, text):
        sel = self.view.sel()
        selected = None
        args = []
        if len(sel) > 0:
            selected = sel
        for region in sel:
            if region.size() == 0:
                self.view.insert(edit, region.end(), text)
            else:
                self.view.replace(edit, region, text)
