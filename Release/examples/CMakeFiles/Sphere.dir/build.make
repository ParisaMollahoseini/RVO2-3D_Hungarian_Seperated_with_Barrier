# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /media/sf_orca_python_3d_final

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /media/sf_orca_python_3d_final/Release

# Include any dependencies generated for this target.
include examples/CMakeFiles/Sphere.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/Sphere.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/Sphere.dir/flags.make

examples/CMakeFiles/Sphere.dir/Sphere.cpp.o: examples/CMakeFiles/Sphere.dir/flags.make
examples/CMakeFiles/Sphere.dir/Sphere.cpp.o: ../examples/Sphere.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/media/sf_orca_python_3d_final/Release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/Sphere.dir/Sphere.cpp.o"
	cd /media/sf_orca_python_3d_final/Release/examples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/Sphere.dir/Sphere.cpp.o -c /media/sf_orca_python_3d_final/examples/Sphere.cpp

examples/CMakeFiles/Sphere.dir/Sphere.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Sphere.dir/Sphere.cpp.i"
	cd /media/sf_orca_python_3d_final/Release/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /media/sf_orca_python_3d_final/examples/Sphere.cpp > CMakeFiles/Sphere.dir/Sphere.cpp.i

examples/CMakeFiles/Sphere.dir/Sphere.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Sphere.dir/Sphere.cpp.s"
	cd /media/sf_orca_python_3d_final/Release/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /media/sf_orca_python_3d_final/examples/Sphere.cpp -o CMakeFiles/Sphere.dir/Sphere.cpp.s

# Object files for target Sphere
Sphere_OBJECTS = \
"CMakeFiles/Sphere.dir/Sphere.cpp.o"

# External object files for target Sphere
Sphere_EXTERNAL_OBJECTS =

examples/Sphere: examples/CMakeFiles/Sphere.dir/Sphere.cpp.o
examples/Sphere: examples/CMakeFiles/Sphere.dir/build.make
examples/Sphere: src/libRVO.a
examples/Sphere: examples/CMakeFiles/Sphere.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/media/sf_orca_python_3d_final/Release/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable Sphere"
	cd /media/sf_orca_python_3d_final/Release/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Sphere.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/Sphere.dir/build: examples/Sphere

.PHONY : examples/CMakeFiles/Sphere.dir/build

examples/CMakeFiles/Sphere.dir/clean:
	cd /media/sf_orca_python_3d_final/Release/examples && $(CMAKE_COMMAND) -P CMakeFiles/Sphere.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/Sphere.dir/clean

examples/CMakeFiles/Sphere.dir/depend:
	cd /media/sf_orca_python_3d_final/Release && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /media/sf_orca_python_3d_final /media/sf_orca_python_3d_final/examples /media/sf_orca_python_3d_final/Release /media/sf_orca_python_3d_final/Release/examples /media/sf_orca_python_3d_final/Release/examples/CMakeFiles/Sphere.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/Sphere.dir/depend

