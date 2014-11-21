# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys
reload(sys)

sys.setdefaultencoding('utf8')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PillarsCGSystem.settings")

    # #运行渲染系统提交终端
    # from RenderManSys.admintoolserver import AdminToolSvr
    # from PillarsCGSystem import globalvar
    # globalvar.ats = AdminToolSvr()
    # globalvar.ats.start()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
