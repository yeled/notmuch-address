import sublime
import sublime_plugin
import subprocess

class PromptNotmuchAddressCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Email to search within notmuch corpus:", "", self.on_done, None, None)

    def on_done(self, text):
        if self.window.active_view():
            self.window.active_view().run_command("notmuch_address", {"query": text})


class NotmuchAddressCommand(sublime_plugin.TextCommand):

    def run(self, edit, query):
        proc1 = subprocess.Popen(['/usr/local/bin/notmuch', 'address', '--deduplicate=address', query],
                    stdout=subprocess.PIPE, universal_newlines=True)
        proc2 = subprocess.Popen(['/usr/bin/grep', '-i', query], stdin=proc1.stdout,
                    stdout=subprocess.PIPE, universal_newlines=True)
        items = proc2.communicate()[0].split('\n')

        def callback(i):
            if i == -1:
                    return
            item = items[i]
            self.view.run_command("notmuch_edit", {"text": item.rstrip('\n')})

        self.view.window().show_quick_panel(items, callback)


class NotmuchEditCommand(sublime_plugin.TextCommand):
    """
    https://stackoverflow.com/questions/20466014/save-the-edit-when-running-a-sublime-text-3-plugin
    we need to run a second process to pass the result from the search to, else the 'edit' magic
    has disappeared by the time we want to insert
    """

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
