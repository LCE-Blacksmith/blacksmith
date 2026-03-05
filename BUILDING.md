# Setting up a Blacksmith Build

### Git Repo Setup

- Clone the Git repo. Do NOT download it as ZIP, that won't work.
    > You can run
    >
    > ```
    > git clone https://github.com/LCE-Blacksmith/blacksmith.git --recurse-submodules
    > ```
    >
    > You always need the `--recurse-submodules` flag!
- Setup the git hooks and build info as follows
    > ```
    > py tools/setup_git_hooks.py
    > py tools/update_git.py
    > ```

## Building from Source

- Ensure you have installed the following dependencies installed:
    - Python 3.10+
    - Meson 1.1+
    - LLVM 22.1+
    - Visual Studio Build Tools 2022

- Configure the project with meson
    > For 64-bit builds use meson_amd64.ini, other architectures will be here eventually
    >
    > Available flags include dev and protect, specified with -D[flagname]=true
    >
    > ```
    > meson setup --buildtype [release/debug] --native-file meson_amd64.ini [flags] build
    > ```
- Building a target
    > Specifify a target using the path to target plus the symbol name as follows:
    >
    > ```
    > meson compile -j [number of cpu threads] -C build [target path]/[target version]
    > ```
- Rebuilding a target
    > Cleaning out the previous build requires you to re-run the setup with --wipe before the builddir (ie. 'build')
    >
    > Afterwards the client can be recompiled as normal.

If you've added any new files, you must run `py tools/meson_poke.py [meson.build file]` to signal meson to refresh and add new files to the build.
