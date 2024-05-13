from manim.utils.file_ops import open_file as open_media_file 
from manim import config
from manim import *
from MoveTargetvsAlfaFunc import *
from z_indexTesting import * 

import time

config.max_files_cached = 300
config.disable_caching = True
config.disable_caching_warning = True
#config.quality = "low_quality"
config.quality = "medium_quality"
#config.quality = "high_quality"
#config.quality = "production_quality"
#config.quality = "fourk_quality"

def MoveToTargetvsAlphaFunctionTest(file):
    #Testing MoveToTarget vs AlphaFunction
    MoveToTargetTime: float
    AlphaFuncTime: float

    start_time = time.time()
    for _ in range(50):
        scene = MoveToTargetExample()
        scene.render()
    MoveToTargetTime = (time.time() - start_time)
    start_time = None
    #open_media_file(scene.renderer.file_writer.movie_file_path)

    start_time = time.time()
    for _ in range(50):
        scene = AlfaFuncExample()
        scene.render()
    AlphaFuncTime = (time.time() - start_time)
    start_time = None
    #open_media_file(scene.renderer.file_writer.movie_file_path)


    file.write("--- Testing speed in rendering: MoveToTarget vs AlphaFunciton ---\n")
    if MoveToTargetTime > AlphaFuncTime:
        file.write("--- AlphaFunc is fastst with %s seconds, " % (AlphaFuncTime))
        file.write("then MoveToTarget which is %s seconds slower---\n\n" % (MoveToTargetTime - AlphaFuncTime))
    elif MoveToTargetTime < AlphaFuncTime:
        file.write("--- MoveToTarget is fastst with %s seconds, " % (MoveToTargetTime))
        file.write("then AlphaFunc which is %s seconds slower---\n\n" % (AlphaFuncTime - MoveToTargetTime))
    else:
        file.write("--- They are the same speed. ---\n\n") #Not Gonna Happen
    AlphaFuncTime = None; MoveToTargetTime = None

def z_index_vs_z_axes_vs_none(file):
    zNoneTime: float
    zAxesTime: float
    zIndexTime: float

    start_time = time.time()
    for _ in range(20):
        scene = zNone()
        scene.render()
    zNoneTime = (time.time() - start_time)
    start_time = None

    start_time = time.time()
    for _ in range(20):
        scene = zAxes()
        scene.render()
    zAxesTime = (time.time() - start_time)
    start_time = None

    start_time = time.time()
    for _ in range(20):
        scene = zIndex()
        scene.render()
    zIndexTime = (time.time() - start_time)
    start_time = None

    file.write("--- Testing speed in rendering: No Z vs z-axes vs z-indexs ---\n")
    if zNoneTime < zAxesTime and zNoneTime < zIndexTime:
        file.write("--- No z fastest with %s seconds, " % (zNoneTime))
        if zAxesTime < zIndexTime: 
            file.write("then z-axes %s seconds slower, " % (zAxesTime-zNoneTime))
            file.write("and last z-index %s seconds slower than No z ---\n\n" % (zIndexTime-zNoneTime))
        else:
            file.write("then z-indexs %s seconds slower, " % (zIndexTime-zNoneTime))
            file.write("and last z-axes %s seconds slower than No z ---\n\n" % (zAxesTime-zNoneTime))

    if zAxesTime < zNoneTime and zAxesTime < zIndexTime:
        file.write("--- z-axes fastest with %s seconds, " % (zAxesTime))
        if zNoneTime < zIndexTime: 
            file.write("then no z %s seconds slower, " % (zNoneTime-zAxesTime))
            file.write("and last z-index %s seconds slower than z-axes ---\n\n" % (zIndexTime-zAxesTime))
        else:
            file.write("then z-indexs %s seconds slower, " % (zIndexTime-zAxesTime))
            file.write("and last no z %s seconds slower than z-axes ---\n\n" % (zNoneTime-zAxesTime))

    if zIndexTime < zNoneTime and zIndexTime < zAxesTime:
        file.write("--- z-indexs fastest with %s seconds, " % (zIndexTime))
        if zNoneTime < zAxesTime: 
            file.write("then no z %s seconds slower, " % (zNoneTime-zIndexTime))
            file.write("and last z-axes %s seconds slower than z-index ---\n\n" % (zAxesTime-zIndexTime))
        else:
            file.write("then z-axes %s seconds slower, " % (zAxesTime-zIndexTime))
            file.write("and last no z %s seconds slower than z-index ---\n\n" % (zNoneTime-zIndexTime))
    zNoneTime = None; zAxesTime = None; zIndexTime = None

    
def run():
    #SETUP 
    f = open(".\ManimTesting\Test_results.txt", "w") 
    f.write("########### Testing results ###########\n\n")

    MoveToTargetvsAlphaFunctionTest(f)

    z_index_vs_z_axes_vs_none(f)

    f.close()
run()