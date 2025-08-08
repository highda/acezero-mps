from setuptools import setup
from torch.utils.cpp_extension import CppExtension, BuildExtension
import os

opencv_inc_dir = ''
opencv_lib_dir = ''

conda_env = os.environ['CONDA_PREFIX']

if len(conda_env) > 0 and len(opencv_inc_dir) == 0 and len(opencv_lib_dir) == 0:
    print("Detected active conda environment:", conda_env)

    opencv_inc_dir = conda_env + '/include/opencv4'
    opencv_lib_dir = conda_env + '/lib'

    # Add the include and library paths for llvm-openmp from the conda environment
    llvm_openmp_inc_dir = conda_env + '/include'
    llvm_openmp_lib_dir = conda_env + '/lib'

    print("Assuming OpenCV and OpenMP dependencies in:")
    print(opencv_inc_dir)
    print(opencv_lib_dir)

if len(opencv_inc_dir) == 0:
    print("Error: You have to provide an OpenCV include directory. Edit this file.")
    exit()
if len(opencv_lib_dir) == 0:
    print("Error: You have to provide an OpenCV library directory. Edit this file.")
    exit()

setup(
    name='dsacstar',
    ext_modules=[CppExtension(
        name='dsacstar',
        sources=['dsacstar.cpp', 'thread_rand.cpp'],
        include_dirs=[opencv_inc_dir, llvm_openmp_inc_dir], # Add OpenMP include path
        library_dirs=[opencv_lib_dir, llvm_openmp_lib_dir],  # Add OpenMP library path
        libraries=['opencv_core', 'opencv_calib3d'],
        extra_compile_args=['-Xpreprocessor', '-fopenmp'],   # Clang-specific flags for OpenMP
        extra_link_args=['-lomp']                           # Linker flag for the OpenMP library
    )],
    cmdclass={'build_ext': BuildExtension})
