import subprocess
import ue4paths
import projectParser


def start_proc(args):
    proc = subprocess.Popen(args)
    code = proc.wait()
    if code != 0:
        print(code)
        exit(1)


project = projectParser.BuildProjectInfo()
platform = project.platform()
configuration = project.configuration()
platform_name = '-platform=' + platform.name
configuration_name = '-configuration=' + configuration.name

uproject = '-project=' + projectParser.BuildProjectInfo().uproject()
build_platforms = '-Platforms=' + platform.name
build_args = [ue4paths.ubt(), uproject, '-projectfiles', '-game', '-rocket', 'progress', build_platforms,
              '-noSolutionSuffix']
start_proc(build_args)

platform_name_verb = '/p:Platform=' + platform.name
configuration_name_verb = '/p:Configuration=' + configuration.name
compile_args = [ue4paths.MSVC, project.solution(), r'/t:build', '-m', configuration_name_verb, platform_name_verb]
start_proc(compile_args)

build = '-archivedirectory=' + project.buildPath()

build_args = [ue4paths.uat(), 'BuildCookRun', uproject, '-noP4', '-cook', '-allmaps', '-build',
              '-stage', '-pak', '-archive', build, platform_name, configuration_name]
start_proc(build_args)

cook_args = [ue4paths.uat(), 'BuildCookRun', uproject, '-noP4', '-cook', '-allmaps', '-NoCompile', '-stage', '-pak',
             '-archive', build, platform_name]
start_proc(cook_args)
