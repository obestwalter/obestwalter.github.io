from lektor.project import Project

project = Project.discover()
env = project.make_env()
pad = env.new_pad()
root_record = pad.root
print(root_record)
for c in root_record.children:
    print(c)
