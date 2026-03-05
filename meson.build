#
# 	-- Blacksmith --
#
#	Started development on 05/03/2025, 16:33 PM (+01:00)
#

project('Blacksmith', 'cpp', 'c'
	default_options: [
		'cpp_std=c++latest',
		'c_std=c17',
		'buildtype=release'
	]
)

run_command('py', 'tools/update_git.py')

add_project_arguments(
	'/permissive',
	'/clang:-masm=intel',
	'/clang:-mavx2',
	language: ['cpp', 'c']
)

if get_option('buildtype') == 'release'
	add_project_arguments('-DNDEBUG', language: ['cpp', 'c'])
	add_project_link_arguments('/IGNORE:4702', '/LTCG', language: ['cpp', 'c'])
else
	add_project_arguments('-DDEBUG', '-D_DEBUG', language: ['cpp', 'c'])
endif

if get_option('dev')
	add_project_arguments('-DCLIENT_PRERELEASE=1', language : ['cpp', 'c'])
endif

add_project_link_arguments('/INCREMENTAL:NO', '/SAFESEH:NO', language: ['cpp', 'c'])

subdir('vendor')
subdir('src')
